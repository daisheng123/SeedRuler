import sys
from show_1_1 import Ui_Form
from PyQt5.QtWidgets import QMainWindow
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pandas as pd
import numpy as np
import shutil
import json
import  os
import  sys
import re
from pathlib import Path

class My_show_2(QWidget):
    def __init__(self,parent = None):
        super().__init__(parent)
        self.ui=Ui_Form()
        self.ui.setupUi(self)
        print(1)
        #self.ui.pushButton_6.clicked.connect(self.close)
    def open_filepackage(self):
        directory = QFileDialog.getExistingDirectory(self,"选取文件夹","..\inference")
        self.ui.lineEdit.setText(directory)
    def open_file(self):
        file,_=QFileDialog.getOpenFileName(self,"选取文件","..\inference\images_rice")
        self.ui.lineEdit.setText(file)
    def start(self):
        #os.system('conda activate mmd21')
        path=os.path.split(sys.path[0])[0]
        os.chdir(path)
        temp = self.ui.lineEdit.text()
        result_path=Path(path+"/inference/output")
        path_list = os.listdir(result_path)
        path_list.sort(reverse=True)  # 对读取的路径进行排序
        count=0
        if path_list:
            for filename in path_list:
                filename = re.sub("\D", "", filename)
                filename = int(filename)
                if count<filename:
                    count=filename
            count=count+1

            print(count)
        end_path = str(result_path) + "/exp" + str(count)
        code = 'python ro_yolo/zjf_detect_rotation_6.py --source \"' + temp + '\" --img-size 640 --weights ro_yolo/runs/train/exp7/weights/best.pt --conf 0.9 --save-txt'
        print(code)
        os.system(code)
        self.ui.lineEdit_2.setText(end_path)


    def open_picture(self):
        filename, _ = QFileDialog.getOpenFileName(self, '打开图片', '', "Image(*.png *jpg)")
        if filename:
            img=cv2.imread(str(filename))
            #Opencv图像以BGR存储，显示的时候要从BGR转到RGB
            img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            x=img.shape[1]
            y=img.shape[0]
            # Qt显示图片时，需要先转换成QImgage类型
            self.ui.zoomscale=1

            QImg=QImage(img,x,y,QImage.Format_RGB888).scaled(1200,800,Qt.KeepAspectRatio,Qt.SmoothTransformation)
            pix=QPixmap.fromImage(QImg)
            self.item=QGraphicsPixmapItem(pix)
            self.scene = QGraphicsScene()
            self.scene.addItem(self.item)
            self.ui.graphicsView.setScene(self.scene)
            self.ui.graphicsView.show()
        else:
            QMessageBox.information(self,"打开失败","没有选择图片")
    def quit(self):
        self.close()
    def open_data(self):
        #显示对应的数据结果
        #获取相关路径
        openfile_name = QFileDialog.getOpenFileName(self, '选择文件', '..\inference\output', 'Excel files(*.xlsx , *.xls)')
        path_openfile_name = openfile_name[0]
        #读取表格
        if len(path_openfile_name) > 0:
            input_table = pd.read_excel(path_openfile_name)
            input_table_rows = input_table.shape[0]
            input_table_colunms = input_table.shape[1]
            input_table_header = input_table.columns.values.tolist()
            self.ui.tableWidget.setColumnCount(input_table_colunms)
            self.ui.tableWidget.setRowCount(input_table_rows)
            self.ui.tableWidget.setHorizontalHeaderLabels(input_table_header)


            for i in range(input_table_rows):
                input_table_rows_values = input_table.iloc[[i]]
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                for j in range(input_table_colunms):
                    input_table_items_list = input_table_rows_values_list[j]
                    input_table_items = str(input_table_items_list)
                    newItem = QTableWidgetItem(input_table_items)
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.ui.tableWidget.setItem(i, j, newItem)

        else:
            QMessageBox.information(self, "打开失败", "没有选择数据文件")

    # def sh_2(self):
    #     shutil.copyfile("startgrain.png",'./picture_path/112.png')
    #     length_start(self.port1,self.port2,self.port3)
    #     img=cv2.imread("./result_picture/finalsize.jpg")
    #     img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    #     x=img.shape[1]
    #     y=img.shape[0]
    #     # Qt显示图片时，需要先转换成QImgage类型
    #     self.ui.zoomscale=1
    #
    #     QImg=QImage(img,x,y,QImage.Format_RGB888)
    #     pix=QPixmap.fromImage(QImg)
    #     self.item=QGraphicsPixmapItem(pix)
    #     self.scene = QGraphicsScene()
    #     self.scene.addItem(self.item)
    #     self.ui.graphicsView.setScene(self.scene)
    #     self.ui.graphicsView.show()
    #
    #     f=open("./result_txt/test.txt",'r')
    #     file=f.read()
    #     file=file.split('end')
    #     file=json.loads(file[0])
    #     grainSizes=file
    #     temp = len(grainSizes)
    #     le=[]
    #     si=[]
    #     self.ui.table.setRowCount(temp)
    #     for num1 in range(temp):
    #         le.append(round(grainSizes[num1][1],2))
    #         si.append(round(grainSizes[num1][2],2))
    #         item1 = QTableWidgetItem()
    #         item2 = QTableWidgetItem()
    #         item3 = QTableWidgetItem()
    #         item4 = QTableWidgetItem()
    #         item1.setText(str(grainSizes[num1][0]))
    #         item2.setText(str(round(grainSizes[num1][1],2)))
    #         item3.setText(str(round(grainSizes[num1][2],2)))
    #         item4.setText(str(round((grainSizes[num1][1]/grainSizes[num1][2])*100,2))+'%')
    #         self.ui.table.setItem(num1,0,item1)
    #         self.ui.table.setItem(num1,1,item2)
    #         self.ui.table.setItem(num1,2,item3)
    #         self.ui.table.setItem(num1,3,item4)
    #     mean1 = round((min(le)+(max(le)-min(le))/2),2)
    #     tt1 = round(mean1-min(le),2)
    #     mean2 = round((min(si)+(max(si)-min(si))/2),2)
    #     tt2 = round(mean2-min(si),2)
    #     self.ui.plainTextEdit.setPlainText("谷粒长宽结果评析：")
    #     self.ui.plainTextEdit.appendPlainText("本次检测到饱满谷粒个数为"+str(temp)+"个")
    #     self.ui.plainTextEdit.appendPlainText("其中谷粒的长度范围为"+str(mean1)+"±"+str(tt1)+"(mm),"+"宽度范围为"+str(mean2)+"±"+str(tt2)+"(mm)")
    #     self.ui.plainTextEdit.appendPlainText("")
    #     self.ui.plainTextEdit.appendPlainText("")
    #     self.ui.plainTextEdit.appendPlainText("意义：")
    #     self.ui.plainTextEdit.appendPlainText("籽粒形状是影响水稻产量的重要指标之一 ,同时也影响着稻米的外观品质。合适的谷粒长宽比能够为种子的生长发育提供更好的营养物质，从而促进水稻的增产增收。")