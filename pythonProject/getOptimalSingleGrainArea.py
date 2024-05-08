# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 14:56:49 2023

@author: 15959
"""

from skimage.measure import label, regionprops  
import numpy as np  
import cv2
import grainSegmentation_1

def getOptimalSingleGrainArea(filePath):
    global one_grain_area
    global each_grain_area
    
    #一、输入数据准备
    #1、[labeled,numObjects]=bwlabel(grain_bw,4)
    grain_bw=grainSegmentation_1.grainSegmentation(filePath)
    grain_bw = np.uint8(grain_bw)  # 将图像数据类型转换为 uint8
    
    # cv2.imshow('finished', grain_bw.astype(np.uint8) * 255)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    numObjects, labeled = cv2.connectedComponents(grain_bw, connectivity=4)

    # 获取最大连通组件数
    numObjects = np.max(labeled)
    #print(numObjects)
  
    #2、regionprops和cell2mat对应函数：each_grain_area所得结果不太对
    #each_grain_area = [prop.area for prop in regionprops(labeled)]  
   
    l = label(labeled)  # 获取标记图像
    each_grain_area = regionprops(l)
    #print(each_grain_area)
    each_grain_area = np.array([prop.area for prop in each_grain_area])
    #print(each_grain_area)
    
    
    #3、sort_each_grain_area和indx
    sort_each_grain_area = np.sort(each_grain_area)
    #print(sort_each_grain_area)
    indx = np.argsort(each_grain_area)
    #print(indx)    
    smooth_sort_each_grain_area = sort_each_grain_area  
    
    #4、sort_each_grain_area_grad2
    sort_each_grain_area_grad = np.gradient(smooth_sort_each_grain_area, 1)  
    sort_each_grain_area_grad2 = np.gradient(sort_each_grain_area_grad,1)

    
    #二、计算最优单个谷粒面积
    numObjects = len(sort_each_grain_area_grad2)
    start0 = 0
    end0 = 0

    for i in range(1, numObjects - 1):
        if sort_each_grain_area_grad2[i - 1] < 0 and sort_each_grain_area_grad2[i + 1] > 0:
            start0 = i
            break

    for i in range(start0 + 1, numObjects - 3):
        temp = (sort_each_grain_area[i + 3] - sort_each_grain_area[i]) / sort_each_grain_area[i]
        if temp > 0.2:
            end0 = i
            break

    if end0 == 0:  # 图像中的谷粒都是单个独立摆放的，无粘连
        end0 = numObjects

    #三、确定最优单个谷粒面积
    min_error = 1000000

    for i in range(start0, end0):
        total_error = 0
        total_number = 0
        for j in range(start0, end0):
            temp1 = int(sort_each_grain_area[j] / sort_each_grain_area[i])  # 取整数部分
            temp3 = sort_each_grain_area[j] / sort_each_grain_area[i]
            if temp1 == 0 or temp1 == 1:
                total_error += abs(1 - temp3)
                total_number += 1

        total_error /= total_number
        if total_error < min_error:
            min_error = total_error
            one_grain_area = sort_each_grain_area[i]
            opt_grain_index = indx[i]

    #print(one_grain_area)
    #print(opt_grain_index)

    numObjects = len(each_grain_area)
    threshold2 = 0.5
    threshold1 = 0.5
    contain = np.zeros((numObjects, 2))  # 记录每个谷粒连通区域包含的谷粒数

    for i in range(numObjects):
        temp1 = int((each_grain_area[i] / one_grain_area))  # 取整数部分

        temp2 = each_grain_area[i] / one_grain_area - temp1  # 取小数部分
        contain[i, 0] = i + 1

        if temp1 == 0 and temp2 > threshold2:
            contain[i, 1] = 1
        elif temp1 > 0 and temp2 > threshold1:
            contain[i, 1] = temp1 + 1
        elif temp1 > 0 and temp2 < threshold1:
            contain[i, 1] = temp1
    
    totalNum = np.sum(contain[:, 1])
    #print('result:')
    #print(contain)
    #print(totalNum)
    return grain_bw,labeled,opt_grain_index, numObjects,each_grain_area,one_grain_area,totalNum
# getOptimalSingleGrainArea()