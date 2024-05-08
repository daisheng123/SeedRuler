# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 19:39:03 2023

@author: 15959
"""
import numpy as np
from skimage.measure import label, regionprops
import grainSegmentation_1
import getOptimalSingleGrainArea
import cv2
import oneSegProcess
from skimage import img_as_ubyte
import scipy.ndimage as ndimage
from skimage.feature import canny
import FitEllip
import matplotlib.pyplot as plt
import scipy.ndimage


def grainTypeParameter(filePath):
    #一、椭圆拟合分割粘连谷粒
    global bw_s1,touchedBW,opt_perimeter,one_grain_area

    grain_bw1,labeled,opt_grain_index,numObjects,each_grain_area,one_grain_area,totalNum=getOptimalSingleGrainArea.getOptimalSingleGrainArea(filePath)
    
    image_part = np.uint8(labeled == (opt_grain_index+1))
    
    #girth = regionprops(image_part, 'Perimeter') 
    image_part = label(image_part)  # 获取标记图像
    girth = regionprops(image_part)
    girth = np.array([prop.perimeter for prop in girth])
    opt_perimeter = girth[0]  # 最佳单个谷粒的周长
    # print("opt_perimeter",opt_perimeter)
    # print("one_grain_area",one_grain_area)
    
    bw_s1 = grain_bw1.copy()
    touchedBW = grain_bw1.copy()

    for i in range(numObjects):
        if each_grain_area[i] > 0.5 * one_grain_area and each_grain_area[i] < 1.4 * one_grain_area:
            touchedBW[labeled == (i+1)] = 0  # 去掉单个谷粒后的二值图像

    common_part = np.logical_and(bw_s1, touchedBW).astype(int)
    bw_s1 = bw_s1 - common_part

    #touchedBW=imfill(touchedBW,'holes');
    touchedBW = touchedBW.astype(np.uint8)
    contours, _ = cv2.findContours(touchedBW, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        cv2.drawContours(touchedBW, [contour], 0, 255, cv2.FILLED)
 
    se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    touchedBW = cv2.morphologyEx(touchedBW, cv2.MORPH_OPEN, se)
    
    #count = np.sum(touchedBW == 255)  # 统计值为1的元素数量
    #print(count)  # 显示结果
    touchedBW[touchedBW == 255] = 1
    
    #[labeled1,numObjects1]=bwlabel(touchedBW,4); 
    numObjects1, labeled1 = cv2.connectedComponents(touchedBW, connectivity=4)    
    numObjects1 = np.max(labeled1)# 获取最大连通组件数

    #touchedBW[touchedBW == 1] = 255
    image = touchedBW.copy()  # 只包含粘连谷粒
    I6 = np.zeros(image.shape)  # 用来汇总每次处理得到的单独谷粒图像
    s_labeled = np.zeros(image.shape)  # 用来标记单独谷粒图像
    flag = 1  # 控制while循环是否终止
    
    # while flag == 1:
    #     image, I5, flag, s_labeled = oneSegProcess.oneSegProcess(image, one_grain_area, opt_perimeter, s_labeled)
    #     I6 = np.logical_or(I6, I5)
    # grain_bw2 = I6 + bw_s1
    # grain_bw2 = grain_bw2.astype(np.uint8)

    # resized_image = cv2.resize(grain_bw2 * 255, (0, 0), fx=0.5, fy=0.5)
    # cv2.imshow("grain_bw2", resized_image)
    # cv2.waitKey(0)
    
# =============================================================================参照物的检测有变动！！！
#     # 二、统计谷粒各性状参数
#     global length_width_data  #谷粒粒型参数
#     global I1
#     
#     # 1、灰度图像
#     I1 = cv2.imread("D:\B_GENERAL\coding transform\project\matlabGUI\\d2.jpg")
#     # 将图像从BGR转换为RGB颜色通道顺序
#     I1 = cv2.cvtColor(I1, cv2.COLOR_BGR2RGB)
#     I_tmp=I1;
#     gray = I_tmp[:,:,0] # 提取红色通道的图像数据
#     
#     # 2、二值图像
#     thr = 20 # 阈值设为15 12-21
#     gray[gray < thr] = 0 # 将小于阈值的像素设为0
#     gray[gray >= thr] = 1 # 将大于等于阈值的像素设为1
#     BW1 = gray # 将处理后的二值化图像赋值给BW1
#     count = np.sum(BW1 == 1)  # 统计值为1的元素数量
#     
#     #cv2.imshow('22', BW1.astype(np.uint8)*255 )
#     #cv2.waitKey(0)
#     #cv2.destroyAllWindows()
#     
#     # [ll,num]=bwlabel(BW1,8);
#     num, ll = cv2.connectedComponents(BW1, connectivity=8)    
#     
#     # a = regionprops(ll, 'Area'); #统计每个谷粒连通区域面积
#     ll = label(ll)  # 获取标记图像
#     a = regionprops(ll)
#     
#     #print(each_grain_area)
#     a = np.array([prop.area for prop in a])
#     sa = np.sort(a)
#     #print(a)
#     #print(sa)
#     indx = np.argsort(a)+1
#     #print(indx)
#     BW1[ll != indx[-1]] = 0
#     #print(ll)
#     #print(BW1)
# 
#     # 3、填充 BW1=imfill(BW1,'holes');
#     BW1=BW1.astype(np.uint8) 
#     contours, _ = cv2.findContours(BW1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     for contour in contours:
#        cv2.drawContours(BW1, [contour], 0, 255, cv2.FILLED)
#     
#     BW1 = BW1.astype(np.uint8)
#     #cv2.imshow('gray', BW1)
#     #cv2.waitKey(0)
#     #cv2.destroyAllWindows()
#     
#     # 4、轮廓 BW1 = canny(BW1) #边缘检测
#     BW1 = cv2.Canny(BW1, 200, 400)
#     BW1 = BW1.astype(np.uint8)
#     #cv2.imshow('out',BW1)
#     #cv2.waitKey(0)
# 
#     
#     #BW1 = cv2.Canny(BW1, 50, 150)
#     #BW1 = BW1.astype(np.uint8) 
#     count = np.sum(BW1 == 255)  # 统计值为1的元素数量
#     #print(count)  # 显示结果
# 
#     row, col = np.where(BW1 > 0)
#     #print(col.shape)
#     #print(row.shape)
#     newX, newY, v = FitEllip.FitEllip(col,row, row.shape[0]);
#     
#     R1 = v[0]
#     R2 = v[1]
#     R = 2 * min(R1, R2) - 70
#     ref = 135.9 / R  # 每像素单位代表的实际长度值，单位：mm/pixel
#     
#     #[labeled2,numObjects2]=bwlabel(grain_bw2,4); 
#     numObjects2, labeled2 = cv2.connectedComponents(grain_bw2, connectivity=4)    
#     numObjects2 = np.max(labeled2)# 获取最大连通组件数
#     
#     #A=cell2mat(struct2cell(regionprops(labeled2,'Area')));%结构体->元组->矩阵
#     labeled2 = label(labeled2)  # 获取标记图像
#     A = regionprops(labeled2)
#     A = np.array([prop.area for prop in A])
#     
#     for i in range(1, numObjects2+1):
#         if A[i-1] > 1.2 * one_grain_area or A[i-1] < 0.5 * one_grain_area:
#             grain_bw2[labeled2 == i] = 0
#     
#     #[labeled2,numObjects2]=bwlabel(grain_bw2,4); 
#     numObjects2, labeled2 = cv2.connectedComponents(grain_bw2, connectivity=4)    
#     numObjects2 = np.max(labeled2)# 获取最大连通组件数
#     
#     #centroid = regionprops(labeled2,'Centroid');
#     labeled2 = label(labeled2)  # 获取标记图像
#     centroid = regionprops(labeled2)
#     centroid = np.array([prop.centroid for prop in centroid])
#     
#     plt.imshow(grain_bw2.astype(np.uint8) * 255 , cmap='gray')
# 
#     # 循环绘制区域编号
#     for v in range(numObjects2):
#         # 获取当前区域的中心点坐标
#         centroid_y = centroid[v][0]
#         centroid_x = centroid[v][1]
# 
#         # 绘制文本，表示当前区域的编号
#         #plt.text(centroid_x - 6, centroid_y, str(v+1), color='r', fontsize=5)
# 
#     # 显示图像
#     #plt.show()
#     
#     #stats = regionprops(labeled2, 'MajorAxisLength', 'MinorAxisLength', 'Perimeter')
#     #LW = np.array([x['MajorAxisLength', 'MinorAxisLength'] for x in stats]) * ref
# 
#     props = regionprops(labeled2)
#     LW = np.array([[prop.major_axis_length, prop.minor_axis_length] for prop in props]) * ref
# 
#     #LW = LW.T
#     LWR = LW[:, 0] / LW[:, 1]
#     
#     #stats2 = regionprops(labeled2,'Area');    
#     labeled2 = label(labeled2)  # 获取标记图像
#     stats2 = regionprops(labeled2)
#     Area = np.array([prop.area for prop in stats2])
#     
#     Area = Area.T * ref * ref
#     Perim = 2 * 3.14 * LW[:, 1] / 2 + 4 * (LW[:, 0] - LW[:, 1]) / 2
#     
#     result = np.column_stack((LW, LWR, Area, Perim))
#     length_width_data = result
#     
#     trait = ['粒长', '粒宽', '长宽比', '面积', '周长']
#    
#     L_max_min_ave_std = [np.max(result[:, 0]), np.min(result[:, 0]), np.mean(result[:, 0]), np.std(result[:, 0])]
#     W_max_min_ave_std = [np.max(result[:, 1]), np.min(result[:, 1]), np.mean(result[:, 1]), np.std(result[:, 1])]
#     LWR_max_min_ave_std = [np.max(result[:, 2]), np.min(result[:, 2]), np.mean(result[:, 2]), np.std(result[:, 2])]
#     Area_max_min_ave_std = [np.max(result[:, 3]), np.min(result[:, 3]), np.mean(result[:, 3]), np.std(result[:, 3])]
#     Perim_max_min_ave_std = [np.max(result[:, 4]), np.min(result[:, 4]), np.mean(result[:, 4]), np.std(result[:, 4])]
# 
#     result1 = np.vstack((L_max_min_ave_std, W_max_min_ave_std, LWR_max_min_ave_std, Area_max_min_ave_std, Perim_max_min_ave_std))
#     traitAnalyseResult = np.column_stack((trait, result1))
#     #typeResult = np.column_stack((trait, result))
#     #print(traitAnalyseResult)
#     #print(result)
# =============================================================================
    return labeled , one_grain_area , totalNum , grain_bw1, grain_bw1
# grainTypeParameter()