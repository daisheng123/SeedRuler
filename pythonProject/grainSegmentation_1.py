# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 13:23:42 2023

@author: 15959
"""

import cv2
import numpy as np
from sklearn.cluster import KMeans
from scipy.ndimage import label
from scipy.ndimage.measurements import label
from skimage.measure import regionprops
from skimage.morphology import remove_small_objects
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from scipy.signal import find_peaks
import scipy.ndimage as ndimage
from scipy.ndimage import gaussian_filter1d
from scipy.signal import convolve2d
from scipy.ndimage import convolve
from scipy.ndimage import correlate
import pandas as pd
import xlrd  # 读取excel的库
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from skimage import morphology
from skimage.measure import label, regionprops


def grainSegmentation(filePath):
    global grain_bw

    # 一、基于 k-me ans 聚类算法的谷粒粗分割

    # 读取图像，支持 bmp、jpg、png、tiff 等常用格式
    I = cv2.imread(filePath)

    # I = cv2.imread("D:\B_GENERAL\coding transform\project\matlabGUI\\d5.jpg")
    # 将图像从BGR转换为RGB颜色通道顺序
    I = cv2.cvtColor(I, cv2.COLOR_BGR2RGB)
    # gray = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
    # 创建窗口并显示图像

    # 释放窗口
    I = np.double(I)
    I_gray = I[:, :, 0]
    size1 = I.shape
    I_column = np.reshape(I, (size1[0] * size1[1], 3))

    thr1 = 60
    thr2 = 60
    I1 = I_column[:, 0] - I_column[:, 2]
    I1[I1 >= thr1] = 30
    I2 = I_column[:, 1] - I_column[:, 2]
    I2[I2 >= thr2] = 30
    I4 = np.sum(I_column, axis=1)
    I1 = np.column_stack((I1, I2))
    np.set_printoptions(threshold=np.inf)

    matrix1 = np.array([[40, 40], [0, 0]])
    kmeans = KMeans(n_clusters=2, init=matrix1)
    kmeans.fit(I1)
    idx = kmeans.labels_
    # idx = kmeans.fit_predict(I1)

    idx = idx.astype(int) - 1
    temp1 = np.nanmean(I4[idx == 0])
    temp2 = np.mean(I4[idx == 1])
    if temp1 > temp2:
        idx = ~idx
    idx_reshape = np.reshape(idx, (size1[0], size1[1]))
    idx_reshape = np.uint8(idx_reshape)
    # cv2.namedWindow("Image_k-means")
    # cv2.imshow("Image_k-means",idx_reshape)
    # cv2.waitKey(0)

    # 二、基于高斯滤波的谷粒精细分割
    # 1、I1 = bwareaopen(I1, 80, 4)  # 删除较小面积的连通图
    I1 = idx_reshape
    num, labels, stats, _ = cv2.connectedComponentsWithStats(I1.astype(np.uint8), 4)

    # 根据面积阈值p，删除较小的连通组件
    for i in range(1, num):
        if stats[i, cv2.CC_STAT_AREA] < 80:
            labels[labels == i] = 0

    # 将删除较小连通组件后的图像返回
    I1 = labels.astype(bool)
    I1 = I1.astype(np.uint8)

    # 2、使用轮廓填充孔洞:I1=imfill(I1,'holes');
    contours, _ = cv2.findContours(I1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        cv2.drawContours(I1, [contour], 0, 255, cv2.FILLED)

    # 显示图像
    # cv2.imshow('Filled',I1)
    # cv2.waitKey(0)

    I1 = I1.astype(np.uint8)

    # 3、使用连通组件标记函数进行标记，确定图像中的连通区域个数I1=idx_reshape
    #  [labeled,numObjects]=bwlabel(I1,4); labeled 是标记后的图像，numObjects 是连通区域的个数

    # test1:使用 ndimage.label 函数进行标记
    # labeled, numObjects = ndimage.label(I1, structure=[[0, 1, 0], [1, 1, 1], [0, 1, 0]])

    # test2:
    numObjects, labeled = cv2.connectedComponents(I1, connectivity=4)

    numObjects = np.max(labeled)  # 获取最大连通组件数
    # print(labeled.shape)
    # print(numObjects)

    # 读取Excel文件
    # df = pd.read_csv(r'D:\B_GENERAL\coding transform\project\matlabGUI\test.csv', header=None)

    # 将数据转换为二维数组
    # labeled = np.array(df.values)
    # labeled = labeled.astype(np.double)

    # num_nonzero = np.count_nonzero(labeled)
    # print("矩阵中非零元素的数量为：", num_nonzero)

    # 将DataFrame对象导出为Excel文件
    # df.to_csv(r'D:\B_GENERAL\coding transform\project\matlabGUI\test1.csv', index=False,  header=None)

    # 4、缩小每个连通区域的谷粒
    # 统计连通区域红色分量直方图

    each_grain_area_histogram = np.zeros((numObjects, 256))  # 统计连通区域红色分量直方图
    for i in range(size1[0]):
        for j in range(size1[1]):
            temp = labeled[i, j]
            if temp != 0:
                temp1 = I_gray[i, j]
                # temp1 = temp1 + 1
                each_grain_area_histogram[temp - 1, int(temp1)] = each_grain_area_histogram[temp - 1, int(temp1)] + 1

    # print(each_grain_area_histogram.tolist())
    # print(temp)
    # print(temp1)

    each_grain_area_histogram_inflection_position = np.zeros((numObjects, 1))

    x = np.arange(1, 257)
    d = 5
    initial1 = 150

    # 一维高斯滤波对直方图进行平滑+多项式拟合
    for i in range(numObjects):
        h = np.multiply(cv2.getGaussianKernel(1, 7.5), (cv2.getGaussianKernel(100, 7.5)).T).flatten()
        arr_2d = np.zeros((100, 100))
        arr_2d[:h.size] = h.reshape((h.size, 1))
        # each_grain_area_histogram[i, :] = cv2.filter2D(each_grain_area_histogram[i, :].astype('float32'), -1, h, borderType=cv2.BORDER_CONSTANT).reshape(1, -1)
        # each_grain_area_histogram[i, :] = scipy.ndimage.filters.convolve(each_grain_area_histogram[i, :], arr_2d, mode='nearest')  # Python命令
        each_grain_area_histogram[i, :] = correlate(each_grain_area_histogram[i, :].astype(np.float64), h,
                                                    mode='reflect')
        # each_grain_area_histogram[i, :] = np.correlate(each_grain_area_histogram[i, :].astype('float64'), h, mode='valid')
        # each_grain_area_histogram[i, :] = cv2.filter2D(each_grain_area_histogram[i, :].flatten(), -1, h).reshape(1, -1)
        y = each_grain_area_histogram[i, :].astype(np.double)

        r = np.polyfit(x, y, d)
        # yv = r[0]*x**5 + r[1]*x**4 + r[2]*x**3 + r[3]*x**2 + r[4]*x + r[5]

        # max1 = np.max(yv[initial1-1:255])
        # indx1 = np.argmax(yv[initial1-1:255]) + initial1 - 2

        # #peaks, _ = find_peaks(yv[initial1:256])
        # #if len(peaks) == 0:
        # #     continue
        # #indx1 = np.argmax(yv[initial1:256]) + initial1 - 2

        # for k in range(indx1, 1, -1):
        #     temp1 = yv[k]  # 沿最大值向左下角找第一个谷点
        #     temp2 = yv[k-1] if k > 0 else np.inf # 防止索引超出范围
        #     temp3 = yv[k+1] if k < len(yv)-1 else np.inf # 防止索引超出范围
        #     if temp1 <= temp2 and temp1 <= temp3:
        #         break
        yvals = np.polyval(r, range(initial1, 256))
        # yv = r[1] * x^ 5 + r[2] * x^ 4 + r[3] * x^ 3 + r[4] * x^ 2 + r[5] * x + r[6]; #直方图的趋势线
        indx1 = np.argmax(yvals)
        indx1 = indx1 + initial1 - 2
        for k in reversed(list(range(2, indx1 + 1))):
            temp1 = r[0] * k ** 5 + r[1] * k ** 4 + r[2] * k ** 3 + r[3] * k ** 2 + r[4] * k + r[5]
            temp2 = r[0] * (k - 1) ** 5 + r[1] * (k - 1) ** 4 + r[2] * (k - 1) ** 3 + r[3] * (k - 1) ** 2 + r[4] * (
                    k - 1) + r[5]
            temp3 = r[0] * (k + 1) ** 5 + r[1] * (k + 1) ** 4 + r[2] * (k + 1) ** 3 + r[3] * (k + 1) ** 2 + r[4] * (
                    k + 1) + r[5]
            if (temp1 <= temp2 and temp1 <= temp3):
                break

        each_grain_area_histogram_inflection_position[i, 0] = k

    # print(h.tolist())
    # print(y.tolist())
    # print(r.tolist())
    # print(yvals.tolist())
    # print(temp1)
    # print(temp2)
    # print(temp3)
    # print(each_grain_area_histogram_inflection_position)

    # 5、删除阴影部分
    for i in range(size1[0]):
        for j in range(size1[1]):
            temp = labeled[i, j]
            if temp != 0:
                if each_grain_area_histogram_inflection_position[temp - 1, 0] != 0 \
                        and I_gray[i, j] < each_grain_area_histogram_inflection_position[temp - 1, 0]:
                    I1[i, j] = 0
                    labeled[i, j] = 0

                    # 三、I1 = bwareaopen(I1, 80, 4)  # 删除较小面积的连通图
    num, labels, stats, _ = cv2.connectedComponentsWithStats(I1.astype(np.uint8), 4)

    # 根据面积阈值p，删除较小的连通组件
    for i in range(1, num):
        if stats[i, cv2.CC_STAT_AREA] < 80:
            labels[labels == i] = 0

    # 将删除较小连通组件后的图像返回
    grain_bw = labels.astype(bool)
    # shared.grain_bw=grain_bw
    # 显示图像
    # cv2.imshow('finished', grain_bw.astype(np.uint8) * 255)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return grain_bw


# grainSegmentation()
