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
import matplotlib.pyplot as plt # plt 用于显示图片
from skimage.measure import label,regionprops
from scipy import ndimage
from skimage.morphology import skeletonize
import scipy.ndimage as ndimage
from skimage.measure import label, regionprops
import math
from skimage.morphology import thin
from skimage.morphology import medial_axis

def getNumberOfGerminatedSeeds():
    
    # 一、预处理
    labeled_image,one_grain_area,totalNum,finalGrainBw,finalGrainBw_1=grainTypeParameter.grainTypeParameter()
    
    totalNum_1, finalGrainBw_labeled = cv2.connectedComponents(finalGrainBw, connectivity=4)    
    totalNum_1 = np.max(finalGrainBw_labeled)# 获取最大连通组件数
    # resized_image = cv2.resize(finalGrainBw_1.astype(np.uint8)*255, (0, 0), fx=0.5, fy=0.5)
    # cv2.imshow("origin",resized_image)
    # cv2.waitKey(0)
    # 1、灰度图像
    I2 = cv2.imread("D:\B_GENERAL\coding transform\project\matlabGUI\\d2.jpg")
    # 将图像从BGR转换为RGB颜色通道顺序
    I2 = cv2.cvtColor(I2, cv2.COLOR_BGR2RGB)
    I_gray = I2[:, :, 0]
    I_gray1 = I2[:, :, 1]
    size1 = I_gray.shape

    # 2、阈值分割
    white_threshold=160 #定义白色的阈值，灰度大于160
    @jit(parallel = True)
    def getWhiteConnected(height,width):
        white_connected = np.zeros((size1[0], size1[1]))
        for i in range(height):
            for j in range(width):
                if(labeled_image[i,j]==0 and I_gray[i,j]>white_threshold and  I_gray1[i,j]>white_threshold):
                    white_connected[i, j] = 1
                else:
                    white_connected[i, j] = 0
        return white_connected
    white_connected=getWhiteConnected(size1[0], size1[1])
    # resized_image = cv2.resize(white_connected, (0, 0), fx=0.5, fy=0.5)
    # cv2.imshow("origin",resized_image)
    # cv2.waitKey(0)
    # 3、删除较小和较大的胚芽
    min_bud_area = int(one_grain_area/44)#确定最小胚芽面积
    max_bud_area = int(1.5*one_grain_area)#确定最大胚芽面积
    white_connected = white_connected > 0
    white_connected = morphology.remove_small_objects(white_connected,min_bud_area,connectivity=1)
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
    white_connected=remove_max_objects(white_connected , max_bud_area)

    #resized_image = cv2.resize(white_connected, (0, 0), fx=0.5, fy=0.5)
    #cv2.imshow("Image_k-means",resized_image)
    #cv2.waitKey(0)
    
    I2 = I2.astype(np.uint8)
    # 4、显示胚芽I_bud
    @jit()
    def getIbud():
        I_bud = I2  
        for i in range(size1[0]):
            for j in range(size1[1]):
                if(labeled_image[i,j]>0):
                    I_bud[i,j,0]=0
                    I_bud[i,j,1] = 0
                    I_bud[i,j,2] = 255
                if(white_connected[i,j]==1):
                    I_bud[i, j, 0] = 255
                    I_bud[i, j, 1] = 0
                    I_bud[i, j, 2] = 0
        return I_bud
    I_bud=getIbud()
    #plt.imshow(I_bud/255,cmap='gray') # 显示图片
    #plt.axis('off') # 不显示坐标轴
    #plt.show()
    
    # 二、统计胚芽数目

    white_connected = white_connected.astype(np.uint8)
    white_numObjects, white_labeled = cv2.connectedComponents(white_connected, connectivity=4)    
    white_numObjects = np.max(white_labeled)# 获取最大连通组件数

    # 1、标记白色连通区域是否与谷粒连通区域相连
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

    # resized_image = cv2.resize(new_white_connected.astype(np.uint8) * 255, (0, 0), fx=0.5, fy=0.5)
    # cv2.imshow("new_white_connected", resized_image)
    # cv2.waitKey(0)

    new_white_connected = new_white_connected.astype(np.uint8)
    new_white_numObjects, new_white_labeled = cv2.connectedComponents(new_white_connected, connectivity=8)    
    new_white_numObjects = np.max(new_white_labeled)# 获取最大连通组件数

    new_white_labeled_1 = label(new_white_labeled)  # 获取标记图像
    new_white_connected_perimeter = regionprops(new_white_labeled_1)
    new_white_connected_perimeter = np.array([prop.perimeter for prop in new_white_connected_perimeter])

    # 3、标记
    mark_touch_area = np.zeros(new_white_numObjects)    # 标记每个胚芽所属的谷粒连通区域
    touchPixelsNum = np.zeros(new_white_numObjects)    # 标记每个白色连通区域与谷粒粘连处的像素点数目
    isTouchPixels = np.zeros((size1[0], size1[1]))    # 标记白色像素点是否点与谷粒粘连

    for i in range(1, size1[0] - 1):
        for j in range(1, size1[1] - 1):
            temp1 = new_white_labeled[i, j]
            
            if temp1 == 0:
                continue
            
            if temp1 > 0 and (labeled_image[i-1, j] > 0 or labeled_image[i+1, j] > 0 or labeled_image[i, j-1] > 0 or labeled_image[i, j+1] > 0):
                
                if labeled_image[i-1, j] > 0:
                    mark_touch_area[temp1-1] = labeled_image[i-1, j]
                    touchPixelsNum[temp1-1] += 1
                    isTouchPixels[i, j] = temp1
                    continue
                elif labeled_image[i+1, j] > 0:
                    mark_touch_area[temp1-1] = labeled_image[i+1, j]
                    touchPixelsNum[temp1-1] += 1
                    isTouchPixels[i, j] = temp1
                    continue
                elif labeled_image[i, j-1] > 0:
                    mark_touch_area[temp1-1] = labeled_image[i, j-1]
                    touchPixelsNum[temp1-1] += 1
                    isTouchPixels[i, j] = temp1
                    continue
                else:
                    mark_touch_area[temp1-1] = labeled_image[i, j+1]
                    touchPixelsNum[temp1-1] += 1
                    isTouchPixels[i, j] = temp1

    # 4、寻找骨架
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
            if mark_whiteRegion_isValid[l-1] == 0:
                new_white_connected3[i, j] = 0
            if mark_whiteRegion_isValid[l-1] == 1:
                new_white_connected3[i, j] = 1

    skel_new_white_connected = skeletonize(new_white_connected3)
    #skel_new_white_connected, distance = medial_axis(new_white_connected3, return_distance=True)
    #skel_new_white_connected = thin(new_white_connected3)
    skel_new_white_connected = skel_new_white_connected.astype(np.uint8)
    resized_image = cv2.resize(skel_new_white_connected * 255, (0, 0), fx=0.5, fy=0.5)
    cv2.imshow("skel_new_white_connected", resized_image)
    cv2.waitKey(0)
    
    #terminating_pts = find_skel_ends(skel_new_white_connected);
    # def find_skel_ends(skel):
    #     skel = skel.astype(np.uint8)
    #     contours, _ = cv2.findContours(skel, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #
    #     terminating_pts = []
    #     for contour in contours:
    #         if len(contour) == 1:
    #             x, y = contour[0][0]
    #             terminating_pts.append((x, y))
    #
    #     return terminating_pts
    
    def find_skel_ends(skel):
        rows, cols = skel.shape
        ends = []
        
        for i in range(1, rows-1):
            for j in range(1, cols-1):
                if skel[i, j] == 1:
                    neighbors = skel[i-1:i+2, j-1:j+2]
                    num_neighbors = np.sum(neighbors) - 1
                    if num_neighbors == 1:
                        ends.append((i, j))
        
        return ends
    
    terminating_pts = find_skel_ends(skel_new_white_connected)
    terminating_pts = np.array(terminating_pts)
    print("terminating_pts.shape", terminating_pts.shape)
    print(terminating_pts)
    count = np.count_nonzero(finalGrainBw == 1)

    # 获取图像中不同的数值
    unique_values = np.unique(finalGrainBw)

    print("值为1的像素数量：", count)
    print("图像中不同的数值：", unique_values)
    # 5、将胚芽与最近的谷粒连接起来
    num_terminating_pts = len(terminating_pts)
    # 将胚芽与最近的谷粒连接起来
    # for i in range(len(terminating_pts)):
    #     for r in range(1, 8):
    #         t1 = finalGrainBw[terminating_pts[i, 0], terminating_pts[i, 1] - r]  # 左
    #         t2 = finalGrainBw[terminating_pts[i, 0], terminating_pts[i, 1] + r]  # 右
    #         t3 = finalGrainBw[terminating_pts[i, 0] - r, terminating_pts[i, 1]]  # 上
    #         t4 = finalGrainBw[terminating_pts[i, 0] + r, terminating_pts[i, 1]]  # 下
    #         t5 = finalGrainBw[terminating_pts[i, 0] - r, terminating_pts[i, 1] - r]  # 左上
    #         t6 = finalGrainBw[terminating_pts[i, 0] - r, terminating_pts[i, 1] + r]  # 右上
    #         t7 = finalGrainBw[terminating_pts[i, 0] + r, terminating_pts[i, 1] - r]  # 左下
    #         t8 = finalGrainBw[terminating_pts[i, 0] + r, terminating_pts[i, 1] + r]  # 右下
    #
    #         if t1 == 1:
    #             new_white_connected3[terminating_pts[i, 0], terminating_pts[i, 1] - r + 1:terminating_pts[i, 1] + 1] = 1
    #             break
    #         if t2 == 1:
    #             new_white_connected3[terminating_pts[i, 0], terminating_pts[i, 1]:terminating_pts[i, 1] + r] = 1
    #             break
    #         if t3 == 1:
    #             new_white_connected3[terminating_pts[i, 0] - r + 1:terminating_pts[i, 0] + 1, terminating_pts[i, 1]] = 1
    #             break
    #         if t4 == 1:
    #             new_white_connected3[terminating_pts[i, 0]:terminating_pts[i, 0] + r, terminating_pts[i, 1]] = 1
    #             break
    #         if t5 == 1:
    #             for j in range(1, r):
    #                 new_white_connected3[terminating_pts[i, 0] - j, terminating_pts[i, 1] - j] = 1
    #             break
    #         if t6 == 1:
    #             for j in range(1, r):
    #                 new_white_connected3[terminating_pts[i, 0] - j, terminating_pts[i, 1] + j] = 1
    #             break
    #         if t7 == 1:
    #             for j in range(1, r):
    #                 new_white_connected3[terminating_pts[i, 0] + j, terminating_pts[i, 1] - j] = 1
    #             break
    #         if t8 == 1:
    #             for j in range(1, r):
    #                 new_white_connected3[terminating_pts[i, 0] + j, terminating_pts[i, 1] + j] = 1
    #             break

    for i in range(num_terminating_pts):

        for r in range(1, 8):
            t1 = finalGrainBw[int(terminating_pts[i, 1]), int(terminating_pts[i, 0]-r)]  # 左
            t2 = finalGrainBw[int(terminating_pts[i, 1]), int(terminating_pts[i, 0]+r)]  # 右
            t3 = finalGrainBw[int(terminating_pts[i, 1]-r), int(terminating_pts[i, 0])]  # 上
            t4 = finalGrainBw[int(terminating_pts[i, 1]+r), int(terminating_pts[i, 0])]  # 下
            t5 = finalGrainBw[int(terminating_pts[i, 1]-r), int(terminating_pts[i, 0]-r)]  # 左上
            t6 = finalGrainBw[int(terminating_pts[i, 1]-r), int(terminating_pts[i, 0]+r)]  # 右上
            t7 = finalGrainBw[int(terminating_pts[i, 1]+r), int(terminating_pts[i, 0]-r)]  # 左下
            t8 = finalGrainBw[int(terminating_pts[i, 1]+r), int(terminating_pts[i, 0]+r)]  # 右下

            if t1 == 1:
                new_white_connected3[int(terminating_pts[i, 1]), int(terminating_pts[i, 0]-r+1):int(terminating_pts[i, 0]+1)] = 1
                break
            if t2 == 1:
                new_white_connected3[int(terminating_pts[i, 1]), int(terminating_pts[i, 0]):int(terminating_pts[i, 0]+r)] = 1
                break
            if t3 == 1:
                new_white_connected3[int(terminating_pts[i, 1])-r+1:int(terminating_pts[i, 1]+1), int(terminating_pts[i, 0])] = 1
                break
            if t4 == 1:
                new_white_connected3[int(terminating_pts[i, 1]):int(terminating_pts[i, 1]+r), int(terminating_pts[i, 0])] = 1
                break
            if t5 == 1:
                for j in range(1, r):
                    new_white_connected3[int(terminating_pts[i, 1]-j), int(terminating_pts[i, 0]-j)] = 1
                break
            if t6 == 1:
                for j in range(1, r):
                    new_white_connected3[int(terminating_pts[i, 1]-j), int(terminating_pts[i, 0]+j)] = 1
                break
            if t7 == 1:
                for j in range(1, r):
                    new_white_connected3[int(terminating_pts[i, 1]+j), int(terminating_pts[i, 0]-j)] = 1
                break
            if t8 == 1:
                for j in range(1, r):
                    new_white_connected3[int(terminating_pts[i, 1]+j), int(terminating_pts[i, 0]+j)] = 1
                break
    
    #% finalGrainBw=imdilate(finalGrainBw,strel('arbitrary',NHOOD)); 
    new_white_connected3 = new_white_connected3.astype(np.uint8)
    N, L = cv2.connectedComponents(new_white_connected3, connectivity=8)    
    N = np.max(L)# 获取最大连通组件数
    
    #L, N = ndimage.label(new_white_connected3, structure=np.ones((3,3)))
    
    #finalGrainBw=finalGrainBw.astype(np.uint8)
    #N1, Labeled_finalGrainBw = cv2.connectedComponents(finalGrainBw, connectivity=4)    
    #N1 = np.max(Labeled_finalGrainBw)# 获取最大连通组件数
    Labeled_finalGrainBw, N1 = ndimage.label(finalGrainBw, structure=np.ones((3, 3)))
    touchMatrix = np.zeros((N, N1))
    print(N)
    print(N1)
    resized_image = cv2.resize(new_white_connected3.astype(np.uint8)*255, (0, 0), fx=0.5, fy=0.5)
    cv2.imshow("new_white_connected3_2", resized_image)
    cv2.waitKey(0)

    # 6、矩阵法遍历谷粒和芽
    for i in range(1, size1[0]-1):
        for j in range(1, size1[1]-1):
            temp1 = L[i, j]
            if temp1 == 0:
                continue
            
            t1 = Labeled_finalGrainBw[i-1, j]  # 上
            t2 = Labeled_finalGrainBw[i+1, j]  # 下
            t3 = Labeled_finalGrainBw[i, j-1]  # 左
            t4 = Labeled_finalGrainBw[i, j+1]  # 右
    
            t5 = Labeled_finalGrainBw[i-1, j-1]  # 左上
            t6 = Labeled_finalGrainBw[i-1, j+1]  # 右上
            t7 = Labeled_finalGrainBw[i+1, j-1]  # 左下
            t8 = Labeled_finalGrainBw[i+1, j+1]  # 右下
    
            if temp1 > 0 and t1 > 0:
                touchMatrix[temp1-1, t1-1] += 1
                continue
            if temp1 > 0 and t2 > 0:
                touchMatrix[temp1-1, t2-1] += 1
                continue
            if temp1 > 0 and t3 > 0:
                touchMatrix[temp1-1, t3-1] += 1
                continue
            if temp1 > 0 and t4 > 0:
                touchMatrix[temp1-1, t4-1] += 1
                continue
            if temp1 > 0 and t5 > 0:
                touchMatrix[temp1-1, t5-1] += 1
                continue
            if temp1 > 0 and t6 > 0:
                touchMatrix[temp1-1, t6-1] += 1
                continue
            if temp1 > 0 and t7 > 0:
                touchMatrix[temp1-1, t7-1] += 1
                continue
            if temp1 > 0 and t8 > 0:
                touchMatrix[temp1-1, t8-1] += 1
                continue
    print(touchMatrix.shape)
    #print(touchMatrix)
    mark_whiteRegion_isValid2 = np.zeros(N)
    mark_finalGrainBw = np.zeros(N1)
    
    m = True
    while m:
        m = False
        for i in range(N):
            if mark_whiteRegion_isValid2[i] == 1:
                continue
            
            rVector = touchMatrix[i, :]
            index = np.where(rVector > 0)[0]
            
            if len(index) > 0 and len(index) == 1 and mark_finalGrainBw[index[0]] == 0:
                mark_whiteRegion_isValid2[i] = 1
                mark_finalGrainBw[index[0]] = 1
                touchMatrix[:, index[0]] = 0
                m = True
    
    m = 1
    while m:
        m = 0
        for i in range(N):
            if mark_whiteRegion_isValid2[i] == 1:
                continue
            
            rVector = touchMatrix[i, :]
            index = np.where(rVector > 0)[0]
            
            if len(index) > 1:
                for j in range(len(index)):
                    if mark_finalGrainBw[index[j]] == 0:
                        mark_whiteRegion_isValid2[i] = 1
                        mark_finalGrainBw[index[j]] = 1
                        touchMatrix[:, index[j]] = 0
                        m += 1
                        break
            
            if len(index) == 1 and mark_finalGrainBw[index[0]] == 0:
                mark_whiteRegion_isValid2[i] = 1
                mark_finalGrainBw[index[0]] = 1
                touchMatrix[:, index[0]] = 0
                m += 1
    new_white_connected4 = np.zeros((size1[0], size1[1]))
    for i in range(size1[0]):
        for j in range(size1[1]):
            l = L[i, j]-1
            if l == 0:
                continue
            if mark_whiteRegion_isValid2[l] == 0:
                new_white_connected4[i, j] = 0
            if mark_whiteRegion_isValid2[l] == 1:
                new_white_connected4[i, j] = 1
    new_white_connected4 = new_white_connected4.astype(np.uint8)
    finalGrainBw = finalGrainBw.astype(np.uint8)
    resized_image = cv2.resize(new_white_connected4*255, (0, 0), fx=0.5, fy=0.5)
    cv2.imshow("new_white_connected4", resized_image)
    cv2.waitKey(0)
    I_tmp = I2
    for i in range(size1[0]):
        for j in range(size1[1]):
            if finalGrainBw[i, j] == 1:
                I_tmp[i, j, 0] = 0
                I_tmp[i, j, 1] = 255
                I_tmp[i, j, 2] = 0
            if new_white_connected4[i, j] == 1:
                I_tmp[i, j, 0] = 255
                I_tmp[i, j, 1] = 0
                I_tmp[i, j, 2] = 0
    resized_image = cv2.resize(I_tmp.astype(np.uint8)*255, (0, 0), fx=0.5, fy=0.5)
    cv2.imshow("I_tmp", resized_image)
    cv2.waitKey(0)
    numOfBud = np.sum(mark_whiteRegion_isValid2)
    gr = numOfBud / totalNum
    #gr_1= bud_count / totalNum
    print('谷粒总数：',totalNum)
    print("萌发谷粒数",numOfBud)
    print("萌发谷粒数_1",bud_count_1, bud_count_2,bud_count)
    print("萌发率",gr)
    #print("萌发率",gr_1)
# =============================================================================
#     方法1
#     @jit()
#     def getBudNumber():
#         bud_number = np.zeros((white_numObjects, 1))
#         for i in range(1,size1[0]-1):
#             for j in range(1, size1[1] - 1):
#                 temp1 = white_labeled[i, j]
#                 if(temp1==0):
#                     continue
#                 if(bud_number[temp1-1,0]==1):
#                     continue
#                 if(temp1>0 and (labeled_image[i-1,j]>0 or labeled_image[i+1,j]>0 or labeled_image[i,j-1]>0 or labeled_image[i,j+1]>0)):
#                     bud_number[temp1-1,0]=1
#         return bud_number
#     bud_num=getBudNumber()
#     total_bud_num=sum(bud_num)[0]
#     print('谷粒总数：',totalNum)
#     print("萌发谷粒数",total_bud_num)
# 
# =============================================================================
getNumberOfGerminatedSeeds()