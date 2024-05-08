# coding=utf-8
import argparse
import os
import shutil
import time
from pathlib import Path
import os.path as osp

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random
import numpy
import xlwt
import xlrd
from xlutils.copy import copy
import glob
import re

import numpy as np
from lxml.etree import Element, SubElement, tostring
from shutil import copyfile

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import (
    check_img_size, non_max_suppression, apply_classifier,
    xyxy2xywh, plot_one_box, strip_optimizer, set_logging, increment_dir)
from utils.torch_utils import select_device, load_classifier, time_synchronized


# 限制目标框的范围（不能超过图片尺寸）
def clip_coords_rice(boxes, img_shape):
    # Clip bounding xyxy bounding boxes to image shape (height, width)
    # clamp_有下划线表示修改并赋值给自身(in_place操作)
    # boxes[:, 0].clamp_(0, img_shape[1])  # x1
    # xc=boxes[:, 0]>60 & boxes[:, 0]<img_shape[1]-60
    boxes = boxes[boxes[:, 0] > 60]
    boxes = boxes[boxes[:, 1] < img_shape[0] - 60]
    boxes = boxes[boxes[:, 2] < img_shape[1] - 60]
    boxes = boxes[boxes[:, 3] > 60]

    # boxes[:, 1].clamp_(0, img_shape[0])  # y1
    # boxes[:, 2].clamp_(0, img_shape[1])  # x2
    # boxes[:, 3].clamp_(0, img_shape[0])  # y2
    return boxes


# 用于将预测框的坐标调整到基于其原本宽高的坐标
def scale_coords_rice(img1_shape, coords, img0_shape, ratio_pad=None):
    # Rescale coords (xyxy) from img1_shape to img0_shape
    if ratio_pad is None:  # calculate from img0_shape
        gain = min(img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1])  # gain  = old / new
        pad = (img1_shape[1] - img0_shape[1] * gain) / 2, (img1_shape[0] - img0_shape[0] * gain) / 2  # wh padding
    else:
        gain = ratio_pad[0][0]
        pad = ratio_pad[1]

    coords[:, [0, 2]] -= pad[0]  # x padding
    coords[:, [1, 3]] -= pad[1]  # y padding
    coords[:, :4] /= gain
    coords_rice = clip_coords_rice(coords, img0_shape)  # 限制目标框的范围（不能超过图片尺寸）
    return coords_rice


def move_files(source_path, aim_dir):
    # if os.path.exists(aim_dir):
    #     shutil.rmtree(aim_dir)
    # os.makedirs(aim_dir)
    source_list = os.listdir(source_path)
    files = [os.path.join(source_path, _) for _ in source_list]
    for index, source_file in enumerate(files):
        (nameWithoutExtention, extention) = os.path.splitext(os.path.basename(source_file))
        label_name = nameWithoutExtention + extention
        copyfile(source_file, aim_dir + os.sep + label_name)


def rice_xywh2xyxy(x):
    # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    y = torch.zeros_like(x) if isinstance(x, torch.Tensor) else np.zeros_like(x)
    y[0] = x[0] - x[2] / 2  # top left x
    y[1] = x[1] - x[3] / 2  # top left y
    y[2] = x[0] + x[2] / 2  # bottom right x
    y[3] = x[1] + x[3] / 2  # bottom right y
    return y


def txt_xml(img_path, img_name, txt_path, img_txt, xml_path, img_xml):
    # 读取txt的信息
    clas = []
    class_names = ['yes', 'no']
    img = cv2.imread(os.path.join(img_path, img_name))
    imh, imw = img.shape[0:2]
    # print(img_txt)
    # print(txt_path)
    txt_img = os.path.join(txt_path, img_txt)
    if os.path.exists(txt_img):
        with open(txt_img, "r") as f:
            next(f)
            for line in f.readlines():
                line = line.strip('\n')
                list = line.split(" ")
                # print(list)
                # print(clas)
                clas.append(list)
        node_root = Element('annotation')
        node_folder = SubElement(node_root, 'folder')
        node_folder.text = '1'
        node_filename = SubElement(node_root, 'filename')
        # 图像名称
        node_filename.text = img_name
        node_size = SubElement(node_root, 'size')
        node_width = SubElement(node_size, 'width')
        node_width.text = str(imw)
        node_height = SubElement(node_size, 'height')
        node_height.text = str(imh)
        node_depth = SubElement(node_size, 'depth')
        node_depth.text = '3'
        for i in range(len(clas)):
            x1 = float(clas[i][1]) * imw
            y1 = float(clas[i][2]) * imh
            w1 = float(clas[i][3]) * imw
            h1 = float(clas[i][4]) * imh
            box_xywh = [x1, y1, w1, h1]
            box_xyxy = rice_xywh2xyxy(box_xywh)

            node_object = SubElement(node_root, 'object')
            node_name = SubElement(node_object, 'name')
            node_name.text = str(class_names[int(clas[i][0])])
            node_pose = SubElement(node_object, 'pose')
            node_pose.text = "Unspecified"
            node_truncated = SubElement(node_object, 'truncated')
            node_truncated.text = "truncated"
            node_difficult = SubElement(node_object, 'difficult')
            node_difficult.text = '0'
            node_bndbox = SubElement(node_object, 'bndbox')
            node_xmin = SubElement(node_bndbox, 'xmin')
            node_xmin.text = str(int(box_xyxy[0]))
            node_ymin = SubElement(node_bndbox, 'ymin')
            node_ymin.text = str(int(box_xyxy[1]))
            node_xmax = SubElement(node_bndbox, 'xmax')
            node_xmax.text = str(int(box_xyxy[2]))
            node_ymax = SubElement(node_bndbox, 'ymax')
            node_ymax.text = str(int(box_xyxy[3]))
        xml = tostring(node_root, pretty_print=True)  # 格式化显示，该换行的换行
        img_newxml = os.path.join(xml_path, img_xml)
        # 服务器xml存储
        serve_xml=r"/root/tomcat/apache-tomcat-8.5.96/webapps/IMSFGM/resource/images/xml/"
        if not os.path.exists(serve_xml):
            os.makedirs(serve_xml)
        file_object_serve=open(os.path.join(serve_xml,img_xml), 'wb')
        file_object_serve.write(xml)
        file_object_serve.close()

        file_object = open(img_newxml, 'wb')
        file_object.write(xml)
        file_object.close()
    # else:


    #     print(txt_img + ' not exist!')


def detect(file_path, save_img=False):
    out, source, weights, view_img, save_txt, imgsz = \
        increment_dir(Path(opt.save_dir) / 'exp'), file_path, opt.weights, opt.view_img, opt.save_txt, opt.img_size
    webcam = source.isnumeric() or source.startswith(('rtsp://', 'rtmp://', 'http://')) or source.endswith('.txt')

    # Initialize
    set_logging()
    device = select_device(opt.device)
    if os.path.exists(out):  # output dir
        shutil.rmtree(out)  # delete dir
    os.makedirs(out)  # make new dir
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    imgsz = check_img_size(imgsz, s=model.stride.max())  # check img_size
    if half:
        model.half()  # to FP16

    # Second-stage classifier
    classify = False
    if classify:
        modelc = load_classifier(name='resnet101', n=2)  # initialize
        modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model'])  # load weights
        modelc.to(device).eval()

    # Set Dataloader
    vid_path, vid_writer = None, None
    if webcam:
        view_img = True
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz)
    else:
        save_img = True
        dataset = LoadImages(source, img_size=imgsz)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = numpy.zeros((len(names), 3))
    # colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]
    for indexx in range(len(names)):
        colors[indexx][indexx] = 255

    # Run inference
    t0 = time.time()
    img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
    _ = model(img.half() if half else img) if device.type != 'cpu' else None  # run once

    save_dir = str(Path(out) / 'images')
    svae_txt_dir = str(Path(out) / 'labelTxt')

    if os.path.exists(save_dir):  # output dir
        shutil.rmtree(save_dir)  # delete dir
    os.makedirs(save_dir)  # make new dir
    if os.path.exists(svae_txt_dir):  # output dir
        shutil.rmtree(svae_txt_dir)  # delete dir
    os.makedirs(svae_txt_dir)  # make new dir
    xlspath = str(Path(out) / 'meng_result0.xls')
    xls_name = ['name_index', 'yes_number', 'no_number', 'total_number', 'rate']
    # 创建excel文件, 如果已有就会覆盖
    workbook = xlwt.Workbook(encoding='utf-8')
    workbook.add_sheet('L0')
    workbook.save(xlspath)
    # 写入数据:
    wb = xlrd.open_workbook(xlspath)
    nrows = wb.sheet_by_index(0).nrows  # 当前行数
    copywb = copy(wb)
    targetsheet = copywb.get_sheet(0)
    ncols = 1  # 写第一行名字
    for celldata in xls_name:
        targetsheet.write(nrows, ncols, celldata)
        ncols += 1
    nrows += 1

    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        t1 = time_synchronized()
        pred = model(img, augment=opt.augment)[0]

        # Apply NMS
        pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, classes=opt.classes, agnostic=opt.agnostic_nms)

        t2 = time_synchronized()

        # Apply Classifier
        if classify:
            pred = apply_classifier(pred, modelc, img, im0s)

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            if webcam:  # batch_size >= 1
                p, s, im0 = path[i], '%g: ' % i, im0s[i].copy()
            else:
                p, s, im0 = path, '', im0s

            save_path = str(Path(save_dir) / Path(p).name)
            txt_path = str(Path(svae_txt_dir) / Path(p).stem) + (
                '_%g' % dataset.frame if dataset.mode == 'video' else '')
            s += '%gx%g ' % img.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            yes_number = ''
            yes_count = 0
            no_number = ''
            no_count = 0
            total_number = 0
            rate = 0
            meng_results = []
            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det = scale_coords_rice(img.shape[2:], det, im0.shape).round()  # zzzzzzzzzzz

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum().item()  # detections per class
                    s += '%g %ss, ' % (n, names[int(c)])  # add to string
                    if c == 0:
                        yes_count = n

                    elif c == 1:
                        no_count = n

                # Write results
                det_index = 0
                for *xyxy, conf, cls in reversed(det):
                    det_index = det_index + 1
                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        line = (cls, conf, *xywh) if opt.save_conf else (cls, *xywh)  # label format
                        with open(txt_path + '.txt', 'a') as f:
                            f.write(('%g ' * len(line) + '\n') % line)

                    if save_img or view_img:  # Add bbox to image
                        # label = '%s %.2f' % (names[int(cls)], conf)
                        # label = '%s  %d' % (names[int(cls)], det_index)
                        label = '%s' % (names[int(cls)])
                        # label = '%s %.2f' % (names[int(cls)], conf)
                        plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=1)

            # Print time (inference + NMS)
            print('%sDone. (%.3fs)' % (s, t2 - t1))

            color = [0, 255, 0]
            c1, c2 = (int(im0.shape[1] - 500), int(im0.shape[0]) - 300), (int(im0.shape[1] - 1), int(im0.shape[0] - 1))
            tl = 4
            tf = max(tl - 1, 1)
            # cv2.rectangle(im0, c1, c2, color, -1, cv2.LINE_AA)  # filled
            cv2.rectangle(im0, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
            if det is not None and len(det):
                total_number = len(det)
                # rate = torch.true_divide(yes_count, total_number)
                rate = yes_count / total_number

            label_total = 'total:' + str(total_number)
            rate_numer = 'rate: ' + '%.4f' % (rate)

            yes_number += '%s: %g ' % (names[int(0)], yes_count)
            no_number += '%s: %g ' % (names[int(1)], no_count)
            meng_results.append(yes_count)
            meng_results.append(no_count)
            meng_results.append(total_number)
            meng_results.append(rate)

            t_size = cv2.getTextSize(label_total, 0, fontScale=tl / 3, thickness=tf)[0]

            cv2.putText(im0, yes_number, (c1[0] + 24, c1[1] + t_size[1] + 30), 0, tl / 3, [225, 255, 255],
                        thickness=tf,
                        lineType=cv2.LINE_AA)
            cv2.putText(im0, no_number, (c1[0] + 24, c1[1] + 2 * t_size[1] + 60), 0, tl / 3, [225, 255, 255],
                        thickness=tf,
                        lineType=cv2.LINE_AA)
            # cv2.putText(im0, un_number, (c1[0] + 24, c1[1] + 3*t_size[1] + 60), 0, tl / 3, [225, 255, 255],
            #             thickness=tf,
            #             lineType=cv2.LINE_AA)
            cv2.putText(im0, label_total, (c1[0] + 24, c1[1] + 3 * t_size[1] + 90), 0, tl / 3, [225, 255, 255],
                        thickness=tf, lineType=cv2.LINE_AA)
            cv2.putText(im0, rate_numer, (c1[0] + 24, c1[1] + 4 * t_size[1] + 120), 0, tl / 3, [225, 255, 255],
                        thickness=tf,
                        lineType=cv2.LINE_AA)

            # cv2.putText(im0, total_del_un_number, (c1[0] + 24, c1[1] + 6 * t_size[1] + 120), 0, tl / 3, [225, 255, 255],
            #             thickness=tf, lineType=cv2.LINE_AA)
            # cv2.putText(im0, rate_del_un_number, (c1[0] + 24, c1[1] + 7 * t_size[1] + 140), 0, tl / 3, [225, 255, 255],
            #             thickness=tf,
            #             lineType=cv2.LINE_AA)

            # 写数据
            dict_list = {}
            ncols = 0
            targetsheet.write(nrows, ncols, nrows)
            ncols += 1
            targetsheet.write(nrows, ncols, str(osp.splitext(osp.split(Path(p))[-1])[0]))
            dict_list[nrows] = [osp.split(Path(p))[-1], yes_count, no_count, total_number, rate]
            print(dict_list)
            ncols += 1
            for celldata in meng_results:
                result_data = celldata.item() if isinstance(celldata, torch.Tensor) else celldata
                result_data = round(result_data, 4) if isinstance(result_data, float) else result_data
                targetsheet.write(nrows, ncols, result_data)
                ncols += 1
            # print('write success --- line is {}, data is : {}'.format(nrows + 1, rowdata))
            nrows += 1

            # Stream results
            if view_img:

                # print('1111111111111111111111111')
                # print(im0.shape)
                cv2.namedWindow(p, 0)
                cv2.resizeWindow(p, 1200, 800)

                cv2.imshow(p, im0)
                if cv2.waitKey(1) == ord('q'):  # q to quit
                    raise StopIteration

            # Save results (image with detections)
            #本地
            # save_path_serve = r"E:\yjs\myeclipse\.metadata\.me_tcat85\webapps\IMSFGM\resource\images\measure"
            #服务器
            save_path_serve = r"/root/tomcat/apache-tomcat-8.5.96/webapps/IMSFGM/resource/images/measure/"
            if save_img:
                if dataset.mode == 'images':
                    cv2.imwrite(save_path, im0)
                    if os.path.exists(save_path_serve):
                        cv2.imwrite(str(Path(save_path_serve) / Path(p).name), im0)
                else:
                    if vid_path != save_path:  # new video
                        vid_path = save_path
                        if isinstance(vid_writer, cv2.VideoWriter):
                            vid_writer.release()  # release previous video writer

                        fourcc = 'mp4v'  # output video codec
                        fps = vid_cap.get(cv2.CAP_PROP_FPS)
                        w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*fourcc), fps, (w, h))
                    vid_writer.write(im0)

    copywb.save(xlspath)  # 保存修改

    # 图像文件夹所在位置
    img_path = source
    # 标注文件夹所在位置
    txt_path = svae_txt_dir
    # txt转化成xml格式后存放的文件夹
    xml_path = str(Path(out) / 'xml')
    images_xml_path = str(Path(out) / 'images_xml')
    if os.path.exists(xml_path):  # output dir
        shutil.rmtree(xml_path)  # delete dir
    os.makedirs(xml_path)  # make new dir
    if os.path.exists(images_xml_path):  # output dir
        shutil.rmtree(images_xml_path)  # delete dir
    os.makedirs(images_xml_path)  # make new dir
    if os.path.isfile(img_path):
        img_path= osp.split(img_path)[0];
    for img_name in os.listdir(img_path):
        # img_name = osp.split(img_path)[1];
        img_xml = img_name.split(".")[0] + ".xml"
        # print(img_xml)
        img_txt = img_name.split(".")[0] + ".txt"
        txt_xml(img_path, img_name, txt_path, img_txt, xml_path, img_xml)



    if save_txt or save_img:
        print('Results saved to %s' % Path(out))

    print('Done. (%.3fs)' % (time.time() - t0))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='yolov5s.pt', help='model.pt path(s)')
    parser.add_argument('--source', nargs='+', type=str, default='inference/images',
                        help='source')  # file/folder, 0 for webcam
    parser.add_argument('--img-size', type=int, default=1024, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='display results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--save-dir', type=str, default='inference/output', help='directory to save results')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--update', action='store_true', help='update all models')

    opt = parser.parse_args()
    print(opt)

    with torch.no_grad():
        if opt.update:  # update all models (to fix SourceChangeWarning)
            for opt.weights in ['yolov5s.pt', 'yolov5m.pt', 'yolov5l.pt', 'yolov5x.pt']:
                for file_path in opt.source:
                    detect(file_path)
                strip_optimizer(opt.weights)
        else:
            for file_path in opt.source:
                detect(file_path)
