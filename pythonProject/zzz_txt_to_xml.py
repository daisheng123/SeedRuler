# -*- coding: utf-8 -*-
import os, shutil
import cv2
import torch
import numpy as np
from lxml.etree import Element, SubElement, tostring


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
    class_names = ['yes', 'no', 'un']
    img = cv2.imread(os.path.join(img_path, img_name))
    imh, imw = img.shape[0:2]
    # print(txt_path)
    # print(img_txt)
    txt_img = os.path.join(txt_path, img_txt)
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
    file_object = open(img_newxml, 'wb')
    file_object.write(xml)
    file_object.close()


if __name__ == "__main__":
    # 图像文件夹所在位置
    img_path = r"inference//images"
    # 标注文件夹所在位置
    txt_path = r"inference//output//exp0//labelTxt"
    # txt转化成xml格式后存放的文件夹
    xml_path = r"inference//output//exp0//xml"
    if os.path.exists(xml_path):  # output dir
        shutil.rmtree(xml_path)  # delete dir
    os.makedirs(xml_path)  # make new dir
    for img_name in os.listdir(img_path):
        # print(img_name)
        img_xml = img_name.split(".")[0] + ".xml"
        # print(img_xml)
        img_txt = img_name.split(".")[0] + ".txt"
        txt_xml(img_path, img_name, txt_path, img_txt, xml_path, img_xml)
