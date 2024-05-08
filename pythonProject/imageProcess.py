# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 15:49:16 2023

@author: 15959
"""
import json
from pathlib import Path
import argparse
import numpy as np
import cv2
import grainTypeParameter
from skimage import morphology
from scipy import ndimage as ndi
from numba import jit
import matplotlib.pyplot as plt  # plt 用于显示图片
from skimage.measure import label, regionprops
from scipy import ndimage
from skimage.morphology import skeletonize
import scipy.ndimage as ndimage
from skimage.measure import label, regionprops
import math
from skimage.morphology import thin
from skimage.morphology import medial_axis
from skimage.morphology import binary_dilation
from skimage.morphology import dilation, disk
from skimage.measure import regionprops
from skimage.measure import label
from PIL import Image
import os


def getRateofseeds(filePath,size):
    # 一、预处理
    labeled_image, one_grain_area, totalNum, finalGrainBw, finalGrainBw_1 = grainTypeParameter.grainTypeParameter(
        filePath)

    totalNum_1, finalGrainBw_labeled = cv2.connectedComponents(finalGrainBw, connectivity=4)

    # 1、灰度图像
    # I2 = cv2.imread("D:\B_GENERAL\coding transform\project\matlabGUI\Luyou 911\\30.jpg")
    I2 = cv2.imread(filePath)

    # I2 = cv2.imread("D:\B_GENERAL\coding transform\project\matlabGUI\\d5.jpg")
    # 将图像从BGR转换为RGB颜色通道顺序
    I2 = cv2.cvtColor(I2, cv2.COLOR_BGR2RGB)
    I_gray = I2[:, :, 0]
    I_gray1 = I2[:, :, 1]
    size1 = I_gray.shape
    # resized_image = cv2.resize(I_gray1 * 255, (0, 0), fx=0.5, fy=0.5)
    # cv2.imshow("I_gray1", resized_image)
    # cv2.waitKey(0)
    # 创建PIL图像对象
    pil_img = Image.fromarray(I_gray1)

    # 保存图像为PNG格式
    # 本地
    # save_dir = r"E:\yjs\myeclipse\.metadata\.me_tcat85\webapps\IMSFGM\resource\images\measure"
    # 服务器
    save_dir = r"/root/tomcat/apache-tomcat-8.5.96/webapps/IMSFGM/resource/images/measure/"
    if not os.path.exists(save_dir):
        # If it doesn't exist, create the directory
        os.makedirs(save_dir)
    counter = 1
    # gray_filename = "I_gray{}.png"
    # while os.path.exists(os.path.join(save_dir, gray_filename.format(counter))):
    #     counter += 1
    # gray_new_file_path = os.path.join(save_dir, gray_filename.format(counter))
    # pil_img.save(gray_new_file_path)
    # 2、阈值分割
    white_threshold = 160  # 定义白色的阈值，灰度大于160

    @jit(parallel=True)
    def getWhiteConnected(height, width):
        white_connected = np.zeros((size1[0], size1[1]))
        for i in range(height):
            for j in range(width):
                if (labeled_image[i, j] == 0 and I_gray[i, j] > white_threshold and I_gray1[i, j] > white_threshold):
                    white_connected[i, j] = 1
                else:
                    white_connected[i, j] = 0
        return white_connected

    white_connected = getWhiteConnected(size1[0], size1[1])

    # 3、删除较小和较大的胚芽
    min_bud_area = int(one_grain_area / 50)  # 确定最小胚芽面积
    max_bud_area = int(1.5 * one_grain_area)  # 确定最大胚芽面积
    white_connected = white_connected > 0
    white_connected = morphology.remove_small_objects(white_connected, min_bud_area, connectivity=1)

    def remove_max_objects(ar, max_size, connectivity=1, in_place=False):

        # Raising type error if not int or bool
        if in_place:
            out = ar
        else:
            out = ar.copy()

        if max_size == 0:  # shortcut for efficiency
            return out

        if out.dtype == bool:
            selem = ndi.generate_binary_structure(ar.ndim, connectivity)
            ccs = np.zeros_like(ar, dtype=np.int32)
            ndi.label(ar, selem, output=ccs)
        else:
            ccs = out

        try:
            component_sizes = np.bincount(ccs.ravel())
        except ValueError:
            raise ValueError("Negative value labels are not supported. Try "
                             "relabeling the input with `scipy.ndimage.label` or "
                             "`skimage.morphology.label`.")

        if len(component_sizes) == 2 and out.dtype != bool:
            print("Only one label was provided to `remove_small_objects`. "
                  "Did you mean to use a boolean array?")

        too_max = component_sizes > max_size
        too_max_mask = too_max[ccs]
        out[too_max_mask] = 0

        return out

    white_connected_1 = remove_max_objects(white_connected, max_bud_area)
    white_connected_1 = white_connected_1.astype(np.uint8)
    # resized_image = cv2.resize(white_connected_1 * 255, (0, 0), fx=0.5, fy=0.5)
    # cv2.imshow("white_connected_1", resized_image)
    # cv2.waitKey(0)

    I2 = I2.astype(np.uint8)

    # 二、统计胚芽数目
    # 1、标记白色连通区域是否与谷粒连通区域相连
    white_numObjects, white_labeled = cv2.connectedComponents(white_connected_1, connectivity=4)
    white_numObjects = np.max(white_labeled)  # 获取最大连通组件数

    isWhiteConnectGrain = np.zeros(white_numObjects)  # 标记白色连通区域是否与谷粒连通区域相连
    for i in range(1, size1[0] - 1):
        for j in range(1, size1[1] - 1):
            temp1 = white_labeled[i, j]
            if temp1 == 0:
                continue
            if isWhiteConnectGrain[temp1 - 1] == 1:
                continue
            if temp1 > 0 and (
                    labeled_image[i - 1, j] > 0 or labeled_image[i + 1, j] > 0 or labeled_image[i, j - 1] > 0 or
                    labeled_image[i, j + 1] > 0):
                isWhiteConnectGrain[temp1 - 1] = 1

    # 2、与谷粒相连的白色区域
    new_white_connected = np.zeros((size1[0], size1[1]))  # 与谷粒相连的白色区域
    for i in range(1, size1[0] - 1):
        for j in range(1, size1[1] - 1):
            temp1 = white_labeled[i, j]
            if temp1 == 0:
                continue
            if isWhiteConnectGrain[temp1 - 1] == 1:
                new_white_connected[i, j] = 1

    new_white_labeled, _ = label(new_white_connected, connectivity=2, return_num=True)
    new_white_numObjects = np.max(new_white_labeled)

    new_white_connected_perimeter = regionprops(new_white_labeled)
    new_white_connected_perimeter = np.array([prop.perimeter for prop in new_white_connected_perimeter])

    mark_touch_area = np.zeros(new_white_numObjects)
    touchPixelsNum = np.zeros(new_white_numObjects)
    isTouchPixels = np.zeros((size1[0], size1[1]))

    for i in range(1, size1[0] - 1):
        for j in range(1, size1[1] - 1):
            temp1 = new_white_labeled[i, j]

            if temp1 == 0:
                continue

            if temp1 > 0 and (
                    labeled_image[i - 1, j] > 0 or labeled_image[i + 1, j] > 0 or labeled_image[i, j - 1] > 0 or
                    labeled_image[i, j + 1] > 0):
                if labeled_image[i - 1, j] > 0:
                    mark_touch_area[temp1 - 1] = labeled_image[i - 1, j]
                    touchPixelsNum[temp1 - 1] += 1
                    isTouchPixels[i, j] = temp1
                    continue
                elif labeled_image[i + 1, j] > 0:
                    mark_touch_area[temp1 - 1] = labeled_image[i + 1, j]
                    touchPixelsNum[temp1 - 1] += 1
                    isTouchPixels[i, j] = temp1
                    continue
                elif labeled_image[i, j - 1] > 0:
                    mark_touch_area[temp1 - 1] = labeled_image[i, j - 1]
                    touchPixelsNum[temp1 - 1] += 1
                    isTouchPixels[i, j] = temp1
                    continue
                else:
                    mark_touch_area[temp1 - 1] = labeled_image[i, j + 1]
                    touchPixelsNum[temp1 - 1] += 1
                    isTouchPixels[i, j] = temp1

    div1 = np.zeros(new_white_numObjects)
    mark_whiteRegion_isValid = np.zeros(new_white_numObjects)
    for i in range(new_white_numObjects):
        div1[i] = touchPixelsNum[i] / new_white_connected_perimeter[i]
        if div1[i] < size:
            mark_whiteRegion_isValid[i] = 1

    new_white_connected3 = np.zeros((size1[0], size1[1]))
    for i in range(size1[0]):
        for j in range(size1[1]):
            l = new_white_labeled[i, j]
            if l == 0:
                continue
            if mark_whiteRegion_isValid[l - 1] == 0:
                new_white_connected3[i, j] = 0
            if mark_whiteRegion_isValid[l - 1] == 1:
                new_white_connected3[i, j] = 1

    new_white_labeled3, _ = label(new_white_connected3, connectivity=2, return_num=True)
    new_white_numObjects3 = np.max(new_white_labeled3)

    print("new_white_numObjects3", new_white_numObjects3)
    # resized_image = cv2.resize(new_white_connected3 * 255, (0, 0), fx=0.5, fy=0.5)
    # cv2.imshow("new_white_connected3", resized_image)
    # cv2.waitKey(0)

    # 5、萌发率计算
    threshold2 = 0.5
    threshold1 = 0.5

    def cnt_process(grain_area):
        contain = 0
        temp1 = int((grain_area / one_grain_area))  # 取整数部分
        temp2 = grain_area / one_grain_area - temp1  # 取小数部分

        if temp1 == 0 and temp2 > threshold2:
            contain = 1
        elif temp1 > 0 and temp2 > threshold1:
            contain = temp1 + 1
        elif temp1 > 0 and temp2 < threshold1:
            contain = temp1
        return contain

    def count_connected_grains_1(labeled_1, labeled_2):
        # 连通区域分析

        labeled_grain = label(labeled_1)
        labeled_bud = label(labeled_2)

        # 获取谷粒和芽的连通区域属性
        grain_props = regionprops(labeled_grain)
        bud_props = regionprops(labeled_bud)

        # 初始化谷粒计数
        bud_count_1 = 0
        # 芽是否已经被分配给谷粒的列表
        bud_assigned = [False] * len(bud_props)
        # 遍历每个谷粒
        for grain in grain_props:
            # 创建一个半径为3的圆形结构元素
            selem = disk(3)
            # 进行膨胀操作
            dilated_grain = dilation(labeled_grain == grain.label, selem)
            # resized_image = cv2.resize(dilated_grain.astype(np.uint8) * 255, (0, 0), fx=0.5, fy=0.5)
            # cv2.imshow("dilated_grain", resized_image)
            # cv2.waitKey(0)

            # 膨胀谷粒连通区域
            # dilated_grain = binary_dilation(labeled_grain == grain.label)
            # 初始化是否与芽相连的标志
            connected_buds_1 = 0
            # 遍历每个芽
            for i, bud in enumerate(bud_props):
                if bud_assigned[i]:
                    continue
                selem = disk(1)
                dilated_buds = dilation(labeled_bud == bud.label, selem)

                # 膨胀谷粒芽连通区域
                # dilated_buds = binary_dilation(labeled_bud == bud.label)
                # 判断连通区域是否重叠
                intersection = np.logical_and(dilated_grain, dilated_buds)
                if np.any(intersection):
                    # resized_image = cv2.resize(dilated_buds.astype(np.uint8) * 255, (0, 0), fx=0.5, fy=0.5)
                    # cv2.imshow("dilated_buds", resized_image)
                    # cv2.waitKey(0)
                    bud_assigned[i] = True
                    connected_buds_1 += 1

            cnt = cnt_process(grain.area)
            # print("connected_buds_1", connected_buds_1)
            # print("cnt", cnt)
            if connected_buds_1:
                if connected_buds_1 > cnt:
                    connected_buds_1 = cnt
            # 如果与芽相连，则谷粒计数加一
            bud_count_1 += connected_buds_1
        return bud_count_1

    bud_count_1 = count_connected_grains_1(finalGrainBw_1, new_white_connected3)

    # 6、显示芽
    # 假设I2是另一个图像，获取其大小
    height, width, channels = I2.shape

    # 创建一个与I2大小相同的全为0的三通道矩阵
    I_tmp = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(size1[0]):
        for j in range(size1[1]):
            if finalGrainBw_1[i, j] == 1:
                I_tmp[i, j, 0] = 255
                I_tmp[i, j, 1] = 255
                I_tmp[i, j, 2] = 0
            if new_white_connected3[i, j] == 1:
                I_tmp[i, j, 0] = 255
                I_tmp[i, j, 1] = 0
                I_tmp[i, j, 2] = 255
    # resized_image = cv2.resize(I_tmp.astype(np.uint8), (0, 0), fx=0.5, fy=0.5)
    # cv2.imshow("I_tmp", resized_image)
    # cv2.waitKey(0)
    # 创建PIL图像对象
    pil_img = Image.fromarray(I_tmp)

    # 保存图像为PNG格式
    # filename = "I_tmp{}.png"
    # while os.path.exists(os.path.join(save_dir, filename.format(counter))):
    #     counter += 1
    new_file_path = os.path.join(save_dir, Path(filePath).name)
    pil_img.save(new_file_path)
    # pil_img.save(save_path_serve)

    # 假设I2是另一个图像，获取其大小
    height, width, channels = I2.shape

    # 创建一个与I2大小相同的全为0的三通道矩阵
    I_tmp_0 = np.zeros((height, width, 3), dtype=np.uint8)

    # 将矩阵中的所有像素设置为黑色
    I_tmp_0[:, :, 0] = 0  # 设置红色通道为0
    I_tmp_0[:, :, 1] = 0  # 设置绿色通道为0
    I_tmp_0[:, :, 2] = 0  # 设置蓝色通道为0
    for i in range(size1[0]):
        for j in range(size1[1]):
            if finalGrainBw_1[i, j] == 1:
                I_tmp_0[i, j, 0] = 255
                I_tmp_0[i, j, 1] = 255
                I_tmp_0[i, j, 2] = 0
            if white_connected[i, j] == 1:
                I_tmp_0[i, j, 0] = 255
                I_tmp_0[i, j, 1] = 0
                I_tmp_0[i, j, 2] = 255
    # resized_image = cv2.resize(I_tmp_0.astype(np.uint8), (0, 0), fx=0.5, fy=0.5)
    # cv2.imshow("I_tmp_0", resized_image)
    # cv2.waitKey(0)
    # 创建PIL图像对象
    pil_img = Image.fromarray(I_tmp_0)

    # 保存图像为PNG格式
    # filename0 = "I_tmp{}_0.png"
    # while os.path.exists(os.path.join(save_dir, filename0.format(counter))):
    #     counter += 1
    # new_file_path0 = os.path.join(save_dir, filename0.format(counter))
    # pil_img.save(new_file_path0)
    # pil_img.save('I_tmp_0.png')

    # 假设I2是另一个图像，获取其大小
    height, width, channels = I2.shape

    # 创建一个与I2大小相同的全为0的三通道矩阵
    I_tmp_1 = np.zeros((height, width, 3), dtype=np.uint8)

    # 将矩阵中的所有像素设置为黑色
    I_tmp_1[:, :, 0] = 0  # 设置红色通道为0
    I_tmp_1[:, :, 1] = 0  # 设置绿色通道为0
    I_tmp_1[:, :, 2] = 0  # 设置蓝色通道为0
    for i in range(size1[0]):
        for j in range(size1[1]):
            if finalGrainBw_1[i, j] == 1:
                I_tmp_1[i, j, 0] = 255
                I_tmp_1[i, j, 1] = 255
                I_tmp_1[i, j, 2] = 0
            if white_connected_1[i, j] == 1:
                I_tmp_1[i, j, 0] = 255
                I_tmp_1[i, j, 1] = 0
                I_tmp_1[i, j, 2] = 255
    # resized_image = cv2.resize(I_tmp_1.astype(np.uint8), (0, 0), fx=0.5, fy=0.5)
    # cv2.imshow("I_tmp_1", resized_image)
    # cv2.waitKey(0)
    # 创建PIL图像对象
    pil_img = Image.fromarray(I_tmp_1)

    # 保存图像为PNG格式
    # filename1 = "I_tmp{}_1.png"
    # while os.path.exists(os.path.join(save_dir, filename1.format(counter))):
    #     counter += 1
    # new_file_path1 = os.path.join(save_dir, filename1.format(counter))
    # pil_img.save(new_file_path1)
    # pil_img.save('I_tmp_1.png')

    # 4、萌发率结果
    dict = {}
    print('谷粒总数：', totalNum)
    print("萌发谷粒数：", bud_count_1)
    print("萌发率：", bud_count_1 / totalNum)
    dict[1] = [totalNum, bud_count_1, bud_count_1 / totalNum, Path(filePath).name]
    print(dict)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', nargs='+', type=str, default=r'E:\yjs\yjs\research\Demo\301-304\1.jpg',
                        help='source')  # file/folder, 0 for webcam
    parser.add_argument('--range', type=float, default=0.4)
    opt = parser.parse_args()
    size = opt.range

    for filePath in opt.source:
        getRateofseeds(filePath, size)
