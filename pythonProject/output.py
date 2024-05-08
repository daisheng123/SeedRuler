import argparse
from pathlib import Path

import cv2
import os
from lxml.etree import Element, SubElement, tostring
from ultralytics import YOLO
import shutil
import pandas as pd
from zjf_eage import count_pixel

# 本地
#save_path_serve = r"E:\yjs\myeclipse\.metadata\.me_tcat85\webapps\IMSFGM\resource\images\measure"


# 服务器
save_path_serve = r"/root/tomcat/apache-tomcat-8.5.96/webapps/IMSFGM/resource/images/measure/"
def main(src, outDir="output/"):
    # init model by loading pretrained weight
    model = YOLO(
        "weights/YOLOrot2.0.pt",
    )
    # predice
    results = model.predict(
        src,
        conf=0.6,
        line_width=1,
    )

    # make sure target output directory exists
    imgDir = outDir + "images/"
    imgExcDir = outDir + "excel_files/"
    os.makedirs(imgDir, exist_ok=True)
    os.makedirs(imgExcDir, exist_ok=True)

    # excel file data for all images
    dfAll = {
        "index": [],
        "image name": [],
        "average width": [],
        "average height": [],
    }
    for i, result in enumerate(results):
        # excel file data for one image
        dfOne = {
            "index": [],
            "width": [],
            "height": [],
        }

        imgPath = result.path
        imgName = imgPath.split("/")[-1]

        # XXX: The detection of A4 paper may fail if the paper is not surrounded by black background
        # When failure occurs, the px2mm would be set to zero, and there would be some output on the
        # console.
        px2mm = count_pixel(imgPath)

        # read width and height/length from the result and store them
        avgW, avgH = 0.0, 0.0
        xywhr = result.obb.xywhr.cpu().tolist()
        per_dict_list = {}
        dict_list = {}
        for j, (x, y, w, h, r) in enumerate(xywhr):
            dfOne["index"].append(j + 1)
            dfOne["width"].append(w * px2mm)
            dfOne["height"].append(h * px2mm)
            per_dict_list[j + 1] = [w * px2mm, h * px2mm]
            avgW += w * px2mm
            avgH += h * px2mm

        avgW /= len(dfOne['index'])
        avgH /= len(dfOne['index'])

        # add a line of averages

        dfOne["index"].append(-1)
        dfOne["width"].append(avgW)
        dfOne["height"].append(avgH)
        dfOne = pd.DataFrame(dfOne)
        dfOne.to_excel(imgExcDir + imgName.split(".")[0] + ".xlsx", index=False)  # save excel file

        # add average width and height/length to the excel file of all images
        dfAll['average height'].append(avgH)
        dfAll['average width'].append(avgW)
        dfAll['image name'].append(imgName.split(".")[0])
        dfAll['index'].append(i + 1)
        dict_list[i + 1] = [imgName.split(".")[0], avgW, avgH,]

        # draw bounding boxes on the image
        img = cv2.imread(imgPath)
        xyxyxyxy = result.obb.xyxyxyxy.to(int).cpu().tolist()
        for j, ((x1, y1), (x2, y2), (x3, y3), (x4, y4)) in enumerate(xyxyxyxy):
            # draw rectangle
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.line(img, (x2, y2), (x3, y3), (0, 0, 255), 2)
            cv2.line(img, (x3, y3), (x4, y4), (0, 0, 255), 2)
            cv2.line(img, (x4, y4), (x1, y1), (0, 0, 255), 2)

            # calculate the position to put the text to put index in the center of rectangle
            x = (x1 + x2 + x3 + x4) // 4
            y = (y1 + y2 + y3 + y4) // 4
            (text_width, text_height), _ = cv2.getTextSize(str(j + 1),
                                                           cv2.FONT_HERSHEY_SIMPLEX,
                                                           0.5,
                                                           2)
            x = x - text_width // 2
            y = y + text_height // 2
            cv2.putText(img, str(j + 1), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 2)

        cv2.imwrite(imgDir + imgName, img)
        cv2.imwrite(str(Path(save_path_serve) / Path(imgName)), img)

    # add the line of averages and save the excel file
    dfAll["index"].append("-1")
    dfAll['image name'].append("average")
    dfAll['average height'].append(sum(dfAll['average height']) / len(dfAll['average height']))
    dfAll['average width'].append(sum(dfAll['average width']) / len(dfAll['average width']))
    dfAll = pd.DataFrame(dfAll)
    dfAll.to_excel(outDir + "hwResults.xlsx", index=False)
    print(per_dict_list)
    print(dict_list)


if __name__ == "__main__":
    # the src could be 
    #   1. path to folder
    #   2. path to image
    #   3. list of path to images
    #   and there many other options, see
    #   https://docs.ultralytics.com/modes/predict/#inference-sources for more imformation

    # pip which con I put a requirements.txt exported bytains a very very very long list of
    # packages. I don't think they are all necessary, so if the codes won't work because of packages
    # lack, try just install the one cause the failure.
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', nargs='+', type=str, help='source')  # file/folder, 0 for webcam
    opt = parser.parse_args()
    # src = "testImgs"
    outDir = "output/"  # remember to add the slash
    for src in opt.source:
        main(src, outDir)
