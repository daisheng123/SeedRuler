import sys
import cv2
from PyQt5.Qt import QMessageBox  # QMessage用
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication
from new import Ui_MainWindow
# from picture_2 import Ui_tsd

import shutil
import time
import json
from PyQt5.QtWidgets import *
from my_show_1 import My_show_1
from my_show_2 import My_show_2
# from my_show_2 import My_show_2
import socket


class My_souye(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(My_souye, self).__init__()
        self.setupUi(self)

        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.camera.set(cv2.CAP_PROP_FPS, 60)
        # self.camera.set(cv2.CAP_PROP_BUFFERSIZE,3)
        self.is_camera_opened = False  # 摄像头有没有打开
        # 定时器，30ms捕获一帧
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._queryFrame)
        # self._timer.start(1)
        # self.timelb = time.clock()

        self.startfilename = "startgrain.png"

    # 打开摄像头

    def open_camera_click(self):
        '''
        打开和关闭摄像头
        '''
        self.is_camera_opened = ~self.is_camera_opened
        if self.is_camera_opened:
            self.button2.setText("关闭摄像头")
            self._timer.start()
        else:
            self.button2.setText("打开摄像头")
            self._timer.stop()

    # 从视频中截取图片的function
    def camera_click(self):
        if not self.is_camera_opened:
            return
        # 捕获视频
        self.button2.setText("打开摄像头")
        self._timer.stop()
        self.is_camera_opened = ~self.is_camera_opened
        temp = self.src
        temp = cv2.cvtColor(temp, cv2.COLOR_BGR2RGB)
        cv2.imwrite(self.startfilename, temp)
        img_rows, img_cols, channels = self.src.shape
        bytePerLine = channels * img_cols
        # Qt显示图片时，需要先转换成QImgage类型
        QImg = QImage(self.src.data, img_cols, img_rows, bytePerLine, QImage.Format_RGB888)
        self.label_3.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.label_3.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))

    # 打开文件,并显示原图
    def openfile_click(self):
        filename, _ = QFileDialog.getOpenFileName(self, '打开图片', '..\inference\images_rice', "Image(*.png *jpg)")
        # 若为现有文件，则直接调用该路径

        if filename:
            self.src = cv2.imread(str(filename))  # 原图，以后很多要用,所有要用self
            # Opencv图像以BGR存储，显示的时候要从BGR转到RGB
            shutil.copyfile(filename, self.startfilename)
            temp = cv2.cvtColor(self.src, cv2.COLOR_BGR2RGB)
            rows, cols, channels = temp.shape
            bytePerLine = channels * cols
            QImg = QImage(temp.data, cols, rows, bytePerLine, QImage.Format_RGB888)
            self.label_2.setPixmap(QPixmap.fromImage(QImg).scaled(
                self.label_2.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        else:
            QMessageBox.information(self, "打开失败", "没有选择图片")

    # 运行算法
    def function1_click(self):
        # 萌发率测量
        # print('dd')
        self.child1 = My_show_1()
        # self.child1.sh_1()
        self.child1.show()

    def function2_click(self):
        # size测量
        self.child1 = My_show_2()
        # self.child1.sh_1()
        self.child1.show()
        # pass
        # self.child2=My_show_2()
        # self.child2.sh_2(self.s)
        # self.child2.show()

        # 保存结果

    def save_click(self):
        savefilename, _ = QFileDialog.getSaveFileName(self, "保存图片", '..\inference\images_rice',
                                                      'Image(*.png;*.jpg)')
        if savefilename:
            shutil.copyfile(self.startfilename, savefilename)
            QMessageBox.information(self, "保存结果", "保存成功")

        else:
            QMessageBox.information(self, "保存结果失败", "请选择有效路径")
            return

    # @QtCore.pyqtSlot()
    def _queryFrame(self):
        '''
        循环捕获图片
        '''
        ret, self.src = self.camera.read()
        img_rows, img_cols, channels = self.src.shape
        bytePerLine = channels * img_cols
        self.src = cv2.flip(self.src, -1)
        self.src = cv2.cvtColor(self.src, cv2.COLOR_BGR2RGB)
        QImg = QImage(self.src.data, img_cols, img_rows, bytePerLine, QImage.Format_RGB888)
        self.label_2.setPixmap(
            QPixmap.fromImage(QImg).scaled(self.label_2.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
                                           ))

    def grain_weight(self):
        pass

    # def show_picture(self):
    #     pass
    #     #if hasattr(self, "temp"):
    #        self.form2 = Ui_tsd()
    #        self.form2.show()
    #     #else:
    #   QMessageBox.information(self, "无效打开", "请先运行结果")
    def quit(self):
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = My_souye()
    ex.show()
    sys.exit(app.exec_())
