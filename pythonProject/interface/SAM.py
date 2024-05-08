import argparse
import os
import cv2
import sys
import torch
import numpy as np
import pandas as pd
from PIL import Image
from pathlib import Path

# output_dir = r"E:\yjs\data\test\image_xml"  # 保存目录
output_dir = r"/root/tomcat/apache-tomcat-8.5.96/webapps/IMSFGM/resource/images/image_xml/"  # 保存目录
# 本地
# save_path_serve = r"E:\yjs\myeclipse\.metadata\.me_tcat85\webapps\IMSFGM\resource\images\measure"


# 服务器
save_path_serve = r"/root/tomcat/apache-tomcat-8.5.96/webapps/IMSFGM/resource/images/measure/"


# def show_mask(mask, ax, random_color=False):
#     if random_color:
#         color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
#     else:
#         color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
#     h, w = mask.shape[-2:]
#     mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
#     ax.imshow(mask_image)

def start(filename, x, y):
    path_openfile_name = os.path.join(os.path.join(output_dir, filename), 'result_data.xlsx')
    df = pd.read_excel(path_openfile_name)
    name_list = df["名称"].tolist()
    lefttop_x = df["左上坐标_x"].tolist()
    lefttop_y = df["左上坐标_y"].tolist()
    rightbot_x = df["右下坐标_x"].tolist()
    rightbot_y = df["右下坐标_y"].tolist()
    image_name = name_list[1]
    for i in range(len(lefttop_x)):
        if lefttop_x[i] < x < rightbot_x[i] and lefttop_y[i] < y < rightbot_y[i]:
            image_name = name_list[i]
            # image_path = os.path.join(path_grain, image_name, image_name + '.png')
    single_excel_path = os.path.join(os.path.join(output_dir, filename), 'result_data.xlsx')
    all_excel_path = os.path.join(output_dir, 'result_data.xlsx')
    single_df = pd.read_excel(single_excel_path)
    all_df = pd.read_excel(all_excel_path)

    area_value = single_df.loc[single_df["名称"] == image_name, "面积"].values[0]  # 读取选中图片的面积
    origin_df = all_df["名称"]  # 获取所有谷粒名称，方便后续计算图片中的谷粒数
    loc_origin_df = all_df[["名称", "左上坐标_x", "左上坐标_y", "右下坐标_x", "右下坐标_y"]]  # 所有谷粒原始坐标
    loc_after_df = all_df.loc[
        all_df["面积"] >= area_value, ["名称", "左上坐标_x", "左上坐标_y", "右下坐标_x", "右下坐标_y"]]  # 获取标准选择后的谷粒的坐标
    #  "名称", "左上坐标_x", "左上坐标_y", "右下坐标_x", "右下坐标_y" 是唯一标识一个谷粒的列
    unique_columns = ["名称", "左上坐标_x", "左上坐标_y", "右下坐标_x", "右下坐标_y"]
    # 获取两个DataFrame的交集
    intersection_df = pd.merge(loc_after_df, loc_origin_df, on=unique_columns, how="inner")
    # 获取loc_after_df和loc_origin_df的差集
    difference_df = loc_origin_df.loc[
        ~loc_origin_df.set_index(unique_columns).index.isin(intersection_df.set_index(unique_columns).index)]
    inter_name_list = list(set(intersection_df["名称"].tolist()))  # 获取交集中不重复的文件名
    dif_name_list = list(set(difference_df["名称"].tolist()))  # 获取差集中不重复的文件名
    inter_list = intersection_df.to_dict(orient='records')  # 字典的键是"名称"，值是对应行的数值（交集）
    dif_list = difference_df.to_dict(orient='records')  # 字典的键是"名称"，值是对应行的数值（差集）
    # sam_label_dir = os.path.join()  # SAM分割打标图片位置
    os.makedirs(save_path_serve, exist_ok=True)
    # 打标YES标签
    for count, name in enumerate(inter_name_list):
        filtered_values = [d for d in inter_list if d['名称'] == filename]  # 获取当前图片名中的发芽谷粒字典
        result_list = [list(d.values())[1:] for d in filtered_values]  # 获取当前图片名中的发芽谷粒坐标
        sam_img_path = os.path.join(output_dir, filename + '.png')  # SAM分割图片文件名
        sam_label_path = os.path.join(save_path_serve, filename + '.png')  # SAM分割打标图片名
        sam_img = cv2.imread(sam_img_path)
        # 设置矩形框颜色 (B, G, R)
        color = (255, 0, 0)
        # 设置线宽
        thickness = 5
        for value in result_list:
            x1, y1, x2, y2 = value[0], value[1], value[2], value[3]
            # 使用cv2.rectangle绘制矩形框
            cv2.rectangle(sam_img, (x1, y1), (x2, y2), color, thickness)
            # 在矩形框上方添加文字
            text = "Yes"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.8
            text_color = (255, 255, 255)
            text_thickness = 1
            text_position = (x1, y1 - 10)  # 设置文字位置在矩形框上方
            cv2.putText(sam_img, text, text_position, font, font_scale, text_color, text_thickness)
        cv2.imwrite(sam_label_path, sam_img)
        # 打标NO标签
    for count, name in enumerate(dif_name_list):
        filtered_values = [d for d in dif_list if d['名称'] == filename]  # 获取当前图片名中的发芽谷粒字典
        result_list = [list(d.values())[1:] for d in filtered_values]  # 获取当前图片名中的发芽谷粒坐标
        sam_label_path = os.path.join(save_path_serve, filename + '.png')  # SAM分割打标图片名
        sam_img = cv2.imread(sam_label_path)
        # print(sam_label_path)
        # 设置矩形框颜色 (B, G, R)
        color = (0, 0, 255)
        # 设置线宽
        thickness = 5
        for value in result_list:
            x1, y1, x2, y2 = value[0], value[1], value[2], value[3]
            # 使用cv2.rectangle绘制矩形框
            cv2.rectangle(sam_img, (x1, y1), (x2, y2), color, thickness)
            # 在矩形框上方添加文字
            text = "No"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.8
            text_color = (255, 255, 255)
            text_thickness = 1
            text_position = (x1, y1 - 10)  # 设置文字位置在矩形框上方
            cv2.putText(sam_img, text, text_position, font, font_scale, text_color, text_thickness)
        cv2.imwrite(sam_label_path, sam_img)

    all_df = all_df.loc[all_df["面积"] >= area_value, ["名称"]]  # 获取所有大于选中图片面积的名称
    origin_df_list = origin_df.values.tolist()
    all_df_list = all_df.values.tolist()
    all_df_list = [str(x) for item in all_df_list for x in item]  # 去除列表元素的中括号
    origin_count = {}
    all_count = {}
    for i in origin_df_list:
        origin_count[i] = origin_df_list.count(i)  # 计算原始数据中每张图片中的谷粒数
    for i in all_df_list:
        all_count[i] = all_df_list.count(i)  # 计算选择后每张图片的剩余谷粒数
    for key in origin_count:  # 预防出现某张图片没有剩余谷粒数
        if key not in all_count.keys():
            all_count[key] = 0
    result_excel = pd.DataFrame()
    name_index = list(origin_count.keys())
    yes_number = list(all_count.values())
    total_number = list(origin_count.values())
    no_number = list(int(total_number[i]) - int(yes_number[i]) for i in range(len(total_number)))
    rate = list(round(int(yes_number[i]) / int(total_number[i]), 4) for i in range(len(total_number)))
    result_excel["name_index"] = name_index
    result_excel["yes_number"] = yes_number
    result_excel["no_number"] = no_number
    result_excel["total_number"] = total_number
    result_excel["rate"] = rate
    # excel_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(self.image_path))), 'rate_data.xlsx')
    # result_excel.to_excel(excel_path)
    print(f"Data saved ")

    dict = {}
    print('谷粒总数：', total_number[0])
    print("萌发谷粒数：", yes_number[0])
    print("萌发率：", yes_number[0] / total_number[0])
    dict[1] = [total_number[0], yes_number[0], rate[0], filename]
    print(dict)
    # self.ui.lineEdit_2.setText(excel_path)
    # # 显示excel文件
    # # 读取表格
    # if len(excel_path) > 0:
    #     input_table = pd.read_excel(excel_path)
    #     input_table_rows = input_table.shape[0]
    #     input_table_colunms = input_table.shape[1]
    #     input_table_header = input_table.columns.values.tolist()
    #     self.ui.tableWidget.setColumnCount(input_table_colunms)
    #     self.ui.tableWidget.setRowCount(input_table_rows)
    #     self.ui.tableWidget.setHorizontalHeaderLabels(input_table_header)
    #
    #     for i in range(input_table_rows):
    #         input_table_rows_values = input_table.iloc[[i]]
    #         input_table_rows_values_array = np.array(input_table_rows_values)
    #         input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
    #         for j in range(input_table_colunms):
    #             input_table_items_list = input_table_rows_values_list[j]
    #             input_table_items = str(input_table_items_list)
    #             newItem = QTableWidgetItem(input_table_items)
    #             newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    #             self.ui.tableWidget.setItem(i, j, newItem)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', nargs='+', type=str, help='source')  # file/folder, 0 for webcam
    opt = parser.parse_args()

    file_paths = []
    if len(opt.source) == 1:
        opt.source.extend(['1081', '815'])
    for i in range(0, len(opt.source), 3):
        file_paths.append((opt.source[i], opt.source[i + 1], opt.source[i + 2]))

    for filename, x_str, y_str in file_paths:
        x= int(x_str)
        y=int(y_str)
        start(filename, x, y)
