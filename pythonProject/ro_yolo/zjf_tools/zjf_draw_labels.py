# *_* coding : UTF-8 *_*
# 开发工具   ：PyCharm
#https://blog.csdn.net/qq_36563273/article/details/109528493
# 功能描述   ：计算roLableImg标注的xml文件中labels的直方图

import os
import xml.etree.ElementTree as ET
import math
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from matplotlib import rcParams
config = {
    "font.family":'serif',
    "font.size": 24,
    "mathtext.fontset": 'stix',
#     "font.serif": ['SimSun'],

}
rcParams.update(config)

plt.rc('font',family='Times New Roman')

x_list=[]
y_list=[]
w_list=[]
h_list=[]
angle_list = []   # 存储角度的列表

# 读取xml文件，存储其中的angle值
def read_xml(xml_file):
    """
    读取xml文件，找到角度并存储进列表
    :param xml_file:xml文件的路径
    :return:
    """
    tree = ET.parse(xml_file)
    objs = tree.findall('object')
    for ix, obj in enumerate(objs):
        robndbox = obj.find('robndbox')
        if robndbox is not None:
            x_label = float(robndbox.find('cx').text)
            y_label = float(robndbox.find('cy').text)
            w_label = float(robndbox.find('w').text)
            h_label = float(robndbox.find('h').text)
            x_list.append(x_label)
            y_list.append(y_label)
            w_list.append(w_label)
            h_list.append(h_label)

            angle = float(robndbox.find('angle').text)
            angle = angle * 180 / math.pi   # 弧度转化为角度
            angle_list.append(angle)        # 添加进列表

def plt_hist(angle_list):
    # 绘制直方图
    plt.hist(x=angle_list,  # 指定绘图数据
    bins = 30,  # 指定直方图中条块的个数
    color = 'steelblue',  # 指定直方图的填充色
    edgecolor = 'black')  # 指定直方图的边框色
    # 添加x轴和y轴标签
    plt.xlabel('Angle')
    plt.ylabel('Object_num ( all:%d )'%(len(angle_list)))
    # 添加标题
    plt.title('xml-angle',fontsize=26)
    # 设置横坐标刻度和起始
    my_xticks = np.arange(-90,95,15)
    plt.xticks(my_xticks,fontproperties='Times New Roman',size=20)
    # 显示图形
    plt.show()
def plot_labels(x_list,y_list,w_list,h_list):
    save_dir='plots_labels'
    fig,ax=plt.subplots(1,2,figsize=(8,8),tight_layout=True)
    ax=ax.ravel()
    # ax[0].hist(c,bins=np.linspace(0,1,1+1)-0.5,rwidth=0.8)
    # ax[0].set_xlabel('classes')
    ax[0].scatter(x_list,y_list,c=plt.hist2d(x_list,y_list,90),cmap='jet')
    ax[0].set_xlabel('x')
    ax[0].set_ylabel('y')
    ax[1].scatter(w_list, h_list, c=plt.hist2d(w_list, h_list, 90), cmap='jet')
    ax[1].set_xlabel('width')
    ax[1].set_ylabel('height')
    plt.savefig(Path(save_dir)/'labels.png',dpi=200)
    plt.close()

if __name__ == '__main__':
    xmls_dir = 'E:/Projects/xmls_origin'
    xmls = os.listdir(xmls_dir)
    for xml in xmls:
        read_xml(os.path.join(xmls_dir,xml)) # 读取一遍xml文件，存储角度值

    plt_hist(angle_list)
