# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 15:49:16 2023

@author: 15959
"""
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


def getRateofseeds():
    # 一、预处理
    labeled_image, one_grain_area, totalNum, finalGrainBw, finalGrainBw_1 = grainTypeParameter.grainTypeParameter()

    totalNum_1, finalGrainBw_labeled = cv2.connectedComponents(finalGrainBw, connectivity=4)

    # 1、灰度图像
    #I2 = cv2.imread("D:\B_GENERAL\coding transform\project\matlabGUI\Fuliangyou 534\\30.jpg")

    I2 = cv2.imread("D:\B_GENERAL\coding transform\project\matlabGUI\\d2.jpg")
    # 将图像从BGR转换为RGB颜色通道顺序
    I2 = cv2.cvtColor(I2, cv2.COLOR_BGR2RGB)
    I_gray = I2[:, :, 0]
    I_gray1 = I2[:, :, 1]
    size1 = I_gray.shape
    resized_image = cv2.resize(I_gray1 * 255, (0, 0), fx=0.5, fy=0.5)
    cv2.imshow("I_gray1", resized_image)
    cv2.waitKey(0)
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
    min_bud_area = int(one_grain_area / 45)  # 确定最小胚芽面积
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


    I2 = I2.astype(np.uint8)

    # 二、统计胚芽数目
    # 1、标记白色连通区域是否与谷粒连通区域相连
    white_numObjects, white_labeled = cv2.connectedComponents(white_connected_1, connectivity=4)
    white_numObjects = np.max(white_labeled)  # 获取最大连通组件数

    isWhiteConnectGrain = np.zeros(white_numObjects) #标记白色连通区域是否与谷粒连通区域相连
    for i in range(1, size1[0]-1):
        for j in range(1, size1[1]-1):
            temp1 = white_labeled[i, j]
            if temp1 == 0:
                continue
            if isWhiteConnectGrain[temp1-1] == 1:
                continue
            if temp1 > 0 and (labeled_image[i-1, j] > 0 or labeled_image[i+1, j] > 0 or labeled_image[i, j-1] > 0 or labeled_image[i, j+1] > 0):
                isWhiteConnectGrain[temp1-1] = 1

    # 2、与谷粒相连的白色区域
    new_white_connected = np.zeros((size1[0], size1[1])) # 与谷粒相连的白色区域
    for i in range(1, size1[0]-1):
        for j in range(1, size1[1]-1):
            temp1 = white_labeled[i, j]
            if temp1 == 0:
                continue
            if isWhiteConnectGrain[temp1-1] == 1:
                new_white_connected[i, j] = 1

    new_white_connected = new_white_connected.astype(np.uint8)
    new_white_numObjects, new_white_labeled = cv2.connectedComponents(new_white_connected, connectivity=8)
    new_white_numObjects = np.max(new_white_labeled)  # 获取最大连通组件数

    resized_image = cv2.resize(new_white_connected * 255, (0, 0), fx=0.5, fy=0.5)
    cv2.imshow("new_white_connected", resized_image)
    cv2.waitKey(0)

    new_white_labeled_1 = label(new_white_labeled)  # 获取标记图像
    new_white_connected_perimeter = regionprops(new_white_labeled_1)
    new_white_connected_perimeter = np.array([prop.perimeter for prop in new_white_connected_perimeter])

    # 3、标记
    mark_touch_area = np.zeros(new_white_numObjects)  # 标记每个胚芽所属的谷粒连通区域
    touchPixelsNum = np.zeros(new_white_numObjects)  # 标记每个白色连通区域与谷粒粘连处的像素点数目
    isTouchPixels = np.zeros((size1[0], size1[1]))  # 标记白色像素点是否点与谷粒粘连

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

    # 4、寻找骨架(筛除未完全发芽的谷粒）
    div1 = np.zeros(new_white_numObjects)
    mark_whiteRegion_isValid = np.zeros(new_white_numObjects)
    for i in range(new_white_numObjects):
        div1[i] = touchPixelsNum[i] / new_white_connected_perimeter[i]
        if div1[i] < 0.4:
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

    new_white_connected3 = new_white_connected3.astype(np.uint8)
    new_white_numObjects3, new_white_labeled3 = cv2.connectedComponents(new_white_connected3, connectivity=8)
    new_white_numObjects3 = np.max(new_white_labeled3)  # 获取最大连通组件数
    print("new_white_numObjects3", new_white_numObjects3)
    resized_image = cv2.resize(new_white_connected3 * 255, (0, 0), fx=0.5, fy=0.5)
    cv2.imshow("new_white_connected3", resized_image)
    cv2.waitKey(0)

    # 5、萌发率计算
    threshold2 = 0.4
    threshold1 = 0.4
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
            print("connected_buds_1", connected_buds_1)
            print("cnt", cnt)
            if connected_buds_1:
                if connected_buds_1 > cnt:
                    connected_buds_1 = cnt
            # 如果与芽相连，则谷粒计数加一
            bud_count_1 += connected_buds_1
        return bud_count_1

    bud_count_1 = count_connected_grains_1(finalGrainBw_1, new_white_connected3)

    def count_connected_grains_1(labeled_1, labeled_2):
        # 连通区域分析

        labeled_grain = label(labeled_1)
        labeled_bud = label(labeled_2)

        # 获取谷粒和芽的连通区域属性
        grain_props = regionprops(labeled_grain)
        bud_props = regionprops(labeled_bud)

        # 初始化谷粒计数
        bud_count_3 = 0
        bud_count_4 = 0
        # 芽是否已经被分配给谷粒的列表
        bud_assigned = [False] * len(bud_props)
        # 遍历每个谷粒
        for grain in grain_props:
            # 创建一个半径为3的圆形结构元素
            selem = disk(3)
            # 进行膨胀操作
            dilated_grain = dilation(labeled_grain == grain.label, selem)

            # 膨胀谷粒连通区域
            # dilated_grain = binary_dilation(labeled_grain == grain.label)
            # 初始化是否与芽相连的标志
            connected_buds_1 = 0
            # 遍历每个芽
            for i, bud in enumerate(bud_props):
                # 膨胀谷粒芽连通区域
                dilated_buds = binary_dilation(labeled_bud == bud.label)
                if bud_assigned[i]:
                    continue
                # 判断连通区域是否重叠
                if np.any(dilated_grain[bud.coords[:, 0], bud.coords[:, 1]]):
                    connected_buds_1 += 1
                    bud_assigned[i] = True

            cnt = cnt_process(grain.area)
            print("connected_buds_3", connected_buds_1)
            print("cnt", cnt)
            if connected_buds_1:
                if connected_buds_1 > cnt:
                    connected_buds_1 = cnt

            # 如果与芽相连，则谷粒计数加一
            bud_count_3 += connected_buds_1

        return bud_count_3

    bud_count_3= count_connected_grains_1(finalGrainBw_1, new_white_connected3)
    # 6、显示芽
    I_tmp = I2.copy()
    for i in range(size1[0]):
        for j in range(size1[1]):
            if finalGrainBw_1[i, j] == 1:
                I_tmp[i, j, 0] = 0
                I_tmp[i, j, 1] = 255
                I_tmp[i, j, 2] = 0
            if new_white_connected3[i, j] == 1:
                I_tmp[i, j, 0] = 0
                I_tmp[i, j, 1] = 0
                I_tmp[i, j, 2] = 255
    resized_image = cv2.resize(I_tmp.astype(np.uint8) , (0, 0), fx=0.5, fy=0.5)
    cv2.imshow("I_tmp", resized_image)
    cv2.waitKey(0)

    # 4、萌发率结果

    print('谷粒总数：', totalNum)
    print("萌发谷粒数_1", bud_count_1, bud_count_3)
    print("萌发率", bud_count_1/totalNum)


getRateofseeds()