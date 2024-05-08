import argparse
import os
import cv2
import sys
import torch
import numpy as np
import pandas as pd
from PIL import Image
from pathlib import Path
import xml.etree.ElementTree as ET
from segment_anything import sam_model_registry, SamPredictor

# output_dir = r"E:\yjs\data\test\image_xml"  # 保存目录
output_dir = r"/root/tomcat/apache-tomcat-8.5.96/webapps/IMSFGM/resource/images/image_xml/"  # 保存目录
# 本地
# save_path_serve = r"E:\yjs\myeclipse\.metadata\.me_tcat85\webapps\IMSFGM\resource\images\measure"
# 服务器
save_path_serve = r"/root/tomcat/apache-tomcat-8.5.96/webapps/IMSFGM/resource/images/measure/"
def show_mask(mask, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])

    h, w = mask.shape[-2:]
    mask_image = (mask.reshape(h, w, 1) * color.reshape(1, 1, -1) * 255).astype(np.uint8)
    mask_image = cv2.cvtColor(mask_image, cv2.COLOR_BGR2RGB)  # OpenCV uses BGR format
    return mask_image

    # ax.imshow(mask_image)


# def show_box(box, ax):
#     x0, y0 = box[0], box[1]
#     w, h = box[2] - box[0], box[3] - box[1]
#     ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0, 0, 0, 0), lw=2))

# RGB值计算
def rgb_calculate(image, filenum, save_path):
    # 将图片转换为NumPy数组
    image_array = np.array(image)
    # 计算 |R-B| + |G-B|
    result_array = (np.abs(image_array[:, :, 0] - image_array[:, :, 2]) +
                    np.abs(image_array[:, :, 1] - image_array[:, :, 2]))
    # 设置阈值
    threshold = 5  # 根据需要调整阈值
    # 阈值分割
    result_array[result_array >= threshold] = 0
    # 创建显示计算结果的图像
    binary_image = Image.fromarray(result_array.astype(np.uint8))
    binary_array = np.array(binary_image)

    # 膨胀操作，以填充胚芽中的空洞
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilated_image = cv2.dilate(binary_array, kernel)

    # 寻找轮廓
    try:
        contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 找到最大的轮廓
        max_contour = max(contours, key=cv2.contourArea)
        # 获取轮廓的矩形框
        rect = cv2.boundingRect(max_contour)
        # 获取胚芽区域
        embryo_image = image[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]
        embryo_area = dilated_image[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]
        # 保存胚芽区域图片
        embryo_img = filenum + "_embryo.png"
        output_path = os.path.join(save_path, embryo_img)
        cv2.imwrite(output_path, embryo_image)
        # 计算胚芽区域的周长和面积
        perimeter = cv2.arcLength(max_contour, True)
        area = cv2.contourArea(max_contour)
        pixel = cv2.countNonZero(embryo_area)
        txt_name = filenum + ".txt"
        txt_path = os.path.join(save_path, txt_name)
        # 使用 open 函数创建或打开文件，'w' 表示写入模式
        with open(txt_path, 'w') as file:
            # 写入内容
            file.write(f"周长: {perimeter}\n")
            file.write(f"面积: {area}\n")
            file.write(f"范围像素个数: {pixel}\n")
        return area
    except ValueError as e:
        print(f"Error processing {filenum}: {e}")
        return 0


# 从XML文件中读取标注信息
def read_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    filename = root.find('filename').text
    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)
    dict = {}
    dict[1] = [width, height]
    print(dict)

    objects = []
    for obj in root.findall('object'):
        obj_info = {}
        obj_info['name'] = obj.find('name').text
        bndbox = obj.find('bndbox')
        obj_info['xmin'] = int(bndbox.find('xmin').text)
        obj_info['ymin'] = int(bndbox.find('ymin').text)
        obj_info['xmax'] = int(bndbox.find('xmax').text)
        obj_info['ymax'] = int(bndbox.find('ymax').text)
        objects.append(obj_info)

    return filename, width, height, objects


# 精细分割
def segment_grain(path, xmlPath):
    # sam准备工作
    # 使用小模型
    sam_checkpoint = "../weights/sam_vit_b_01ec64.pth"
    model_type = "vit_b"
    device = "cpu"
    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    sam.to(device=device)

    # 设置图片参数
    img_total = []
    # output_dir = os.path.join(path, "grain_information")  # 保存目录

    os.makedirs(output_dir, exist_ok=True)
    # images_xml_dir = os.path.join(path, "images_xml")
    all_df_list = []  # 保存所有图片中所有谷粒数据

    # for file in os.listdir(images_xml_dir):
    #     if file.endswith(".xml"):
    #         img_total.append(file.split('.')[0])
    # for xml_name in img_total:
    #     xml_file = os.path.join(images_xml_dir, f"{xml_name}.xml")
    #     filename, width, height, objects = read_xml(xml_file)
    filename, width, height, objects = read_xml(xmlPath)
    # image = cv2.imread(os.path.join(images_xml_dir, filename))
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    predictor = SamPredictor(sam)
    predictor.set_image(image)
    folder_path = os.path.join(output_dir, os.path.basename(path).split('.')[0])  # 为每张图片创建文件夹
    os.makedirs(folder_path, exist_ok=True)
    # 创建一个空的DataFrame用于存储数据
    data_columns = ["名称", "面积"]
    df_list = []  # 保存单张图片中所有谷粒数据s
    box = []
    for obj_info in objects:
        x_center = (obj_info['xmin'] + obj_info['xmax']) / 2.0
        y_center = (obj_info['ymin'] + obj_info['ymax']) / 2.0
        width = obj_info['xmax'] - obj_info['xmin']
        height = obj_info['ymax'] - obj_info['ymin']
        lefttopx = int(x_center - width / 2.0)
        lefttopy = int(y_center - height / 2.0)
        box.append([int(lefttopx + 1), int(lefttopy + 1), int(lefttopx + width - 1), int(lefttopy + height - 1)])
        input_boxes = torch.tensor(box, device=predictor.device)
        transformed_boxes = predictor.transform.apply_boxes_torch(input_boxes, image.shape[:2])
        masks, _, _ = predictor.predict_torch(
            point_coords=None,
            point_labels=None,
            boxes=transformed_boxes,
            multimask_output=False,
        )

    for i, mask in enumerate(masks):
        mask = ~mask
        mask = mask + 255
        mask = np.repeat(mask.cpu()[0].numpy()[:, :, np.newaxis], 3, axis=2)
        mask = mask.astype(np.uint8)
        res = cv2.bitwise_and(image, mask)
        res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
        res = res[box[i][1]:box[i][3], box[i][0]:box[i][2]]
        filenum = os.path.basename(path).split('.')[0] + '_' + str(i + 1)  # 为每颗谷粒创建文件夹
        save_path = os.path.join(folder_path, filenum)
        os.makedirs(save_path, exist_ok=True)
        filename = filenum + '.png'
        cv2.imwrite(os.path.join(save_path, filename), res)  # 保存分割后的图片
        area = rgb_calculate(res, filenum, save_path)

        df_list.append({
            "名称": filenum,
            "面积": area,
            "左上坐标_x": box[i][0],
            "左上坐标_y": box[i][1],
            "右下坐标_x": box[i][2],
            "右下坐标_y": box[i][3],
        })
        all_df_list.append({
            "名称": os.path.basename(path).split('.')[0],
            "面积": area,
            "左上坐标_x": box[i][0],
            "左上坐标_y": box[i][1],
            "右下坐标_x": box[i][2],
            "右下坐标_y": box[i][3],
        })
        # 使用pandas.concat将DataFrame的列表合并为一个DataFrame
        df = pd.DataFrame(df_list)
        # 保存DataFrame到Excel文件
        excel_path = os.path.join(folder_path, "result_data.xlsx")
        df.to_excel(excel_path, index=False)
        print(f"Data saved to {excel_path}")

    # # 清除之前的图形
    # plt.clf()
    bask_mask = masks.cpu().numpy()[0][0]
    for mask in masks.cpu().numpy()[1:]:
        for i in range(len(bask_mask)):
            bask_mask[i] = np.add(bask_mask[i], mask[0][i])
    # plt.imshow(image)
    mask_image = show_mask(bask_mask, random_color=False)
    # for box in input_boxes:
    #     show_box(box.cpu().numpy(), plt.gca())
    # plt.axis('off')
    # plt.xticks([])
    # plt.yticks([])
    # 保存图像
    sam_path = output_dir
    os.makedirs(sam_path, exist_ok=True)
    # plt.savefig(os.path.join(sam_path, xml_name + '.png'), dpi=400, bbox_inches='tight')
    cv2.imwrite(os.path.join(sam_path, os.path.basename(path).split('.')[0] + '.png'), mask_image)
    print(f"SAM_image saved to {sam_path}")

    # #  关闭图形对象
    # plt.close()

    # 使用pandas.concat将DataFrame的列表合并为一个DataFrame
    all_df = pd.DataFrame(all_df_list)
    # 保存DataFrame到Excel文件
    excel_path = os.path.join(output_dir, "result_data.xlsx")
    all_df.to_excel(excel_path, index=False)
    # print(f"Data saved to {excel_path}")


# if __name__ == '__main__':
#     image_path = r"E:\yjs\data\test\N7-1-11B-3.jpg"  # 图片及YOLO分割文件
#     xmlPath = r"E:\yjs\data\test\N7-1-11B-3.xml"
#     segment_grain(image_path, xmlPath)
#     start(x,y,filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', nargs='+', type=str, help='source1')  # file/folder, 0 for webcam
    opt = parser.parse_args()

    file_paths = []
    for i in range(0, len(opt.source), 2):
        file_paths.append((opt.source[i], opt.source[i + 1]))

    for filePath, xmlPath in file_paths:
        segment_grain(filePath, xmlPath)
