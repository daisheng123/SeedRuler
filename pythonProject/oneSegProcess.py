# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 10:56:51 2023

@author: 15959
"""

import numpy as np
from skimage.measure import label, regionprops
from skimage.morphology import disk, binary_opening
from scipy.ndimage import binary_fill_holes
import getRegionConcavePoints
import regionSegments
import segmentsFitElip
import cv2
from skimage.morphology import remove_small_objects
import matplotlib.pyplot as plt
from scipy import ndimage

def oneSegProcess(image, one_grain_area, opt_perimeter, s_labeled):
    # 对粘连二值图像进行椭圆拟合分割
    # s_labeled是上一轮分割得到的单独谷粒的标记图像
    global numOfConcave,c_row,c_colum
    image_copy = np.copy(image)
    # [L,N]=bwlabel(image,4); 
    image = image.astype(np.uint8)
    num_labels, labeled_image = cv2.connectedComponents(image, connectivity=4)
    num_labels = np.max(labeled_image)# 获取最大连通组件数
    I4 = np.zeros_like(image)  # 存储椭圆拟合分割后的结果
    I5 = np.zeros_like(image)  # 只包含椭圆拟合分割后的单独谷粒
    #print(num_labels)
    for i in range(1, num_labels+1):
        print("i",i)
        image_part_i = (labeled_image == i)
        TF, length, x, y = getRegionConcavePoints.getRegionConcavePoints(image_part_i)
        #print(TF.shape)       
        #print(length)
        #print(x)
        #print(y)
       
        numOfConcave = int(np.sum(TF))
        ind = np.where(TF)[0]
        print("numOfConcave1",numOfConcave)
        for j in range(numOfConcave):
        
            index = ind[j]
            c_row = y[index]  # 当前凹点的行坐标
            c_colum = x[index]  # 当前凹点的列坐标
            print('c_row',c_row)
            print('c_colum',c_colum)
            # 对于检测到的凹点，判断其3x3的四邻域端点像素是否属于单独谷粒，如果是，则该凹点是由上轮过分割产生的假凹点
            if (s_labeled[c_row-3, c_colum] > 0 or s_labeled[c_row+3, c_colum] > 0 or
                s_labeled[c_row, c_colum-3] > 0 or s_labeled[c_row, c_colum+3] > 0):
                TF[index] = 0
            #plt.plot(c_colum,c_row , '.', markersize=1) #标记凹点
               
        
        numOfConcave =int( np.sum(TF))
        print("numOfConcave2",numOfConcave)
        if numOfConcave > 1:
            contour_segments = regionSegments.regionSegments(TF, x, y)
            newImage_part_i = segmentsFitElip.segmentsFitElip(image_part_i, contour_segments, one_grain_area, opt_perimeter)
                         
            num, labels, stats, _ = cv2.connectedComponentsWithStats(newImage_part_i.astype(np.uint8), 4)       
            # 根据面积阈值p，删除较小的连通组件
            for i in range(1, num):
                if stats[i, cv2.CC_STAT_AREA] < int(np.floor(one_grain_area/5)):
                    labels[labels == i] = 0
            # 将删除较小连通组件后的图像返回
            newImage_part_i=labels.astype(bool)
            newImage_part_i=newImage_part_i.astype(np.uint8)         
            
            # resized_image = cv2.resize(newImage_part_i.astype(np.uint8)*255, (0, 0), fx=0.5, fy=0.5)
            # cv2.imshow("I4_part",resized_image)
            # cv2.waitKey(0)
            I4 = np.logical_or(I4, newImage_part_i)
        else:
            I4 = np.logical_or(I4, image_part_i)  # 当前连通区域凹点数量小于1
        # 显示带有标记的图像
        plt.show()
 
    # resized_image = cv2.resize(I4.astype(np.uint8)*255, (0, 0), fx=0.5, fy=0.5)
    # cv2.imshow("I4",resized_image)
    # cv2.waitKey(0)
    
    # [tmp_labeled,tmp_numObjects]=bwlabel(I4,4);
    #print("numOfConcave3",numOfConcave)
    I4 = cv2.UMat(I4.astype(np.uint8))
    num_objects, labeled_I4 = cv2.connectedComponents(I4, connectivity=4)
    num_objects = np.max(labeled_I4)# 获取最大连通组件数

    labeled_I4 = labeled_I4.get()
    area_tmp = regionprops(labeled_I4)
    tmp_areas = [prop.area for prop in area_tmp]
    
    for k in range(len(tmp_areas)):
        if tmp_areas[k] < one_grain_area*1.3 and tmp_areas[k] > one_grain_area*0.5:
            s_grain = (labeled_I4 == k+1)  # 连通区域i中，某个单独谷粒
            I5 = np.logical_or(I5, s_grain)
    
    image = cv2.UMat.get(I4) - I5.astype(np.uint8)  # 粘连谷粒图像
    se = disk(3)
    image = binary_opening(image, selem=se)  # 形态学开操作，去除毛刺边缘
    
    if np.array_equal(image_copy, image):
        flag = 0  # 控制while循环是否终止
        I5 = image
    else:
        flag = 1  # 控制while循环是否终止
    
    
    # 计算最小面积阈值
    min_area_threshold = one_grain_area // 5

    # 删除小于最小面积阈值的连通区域
    I5 = remove_small_objects(I5, min_size=min_area_threshold, connectivity=1)
    #I5 = binary_opening(I5, selem=se)
    #I5 = binary_fill_holes(I5)
    # s_labeled=bwlabel(I5,4);
    I5 = I5.astype(np.uint8)
    num_objects, labeled_I5 = cv2.connectedComponents(I5, connectivity=4)
    
    return image, I5, flag, labeled_I5

    