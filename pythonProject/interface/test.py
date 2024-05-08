import argparse

# 创建参数解析器
parser = argparse.ArgumentParser()
parser.add_argument('--source', nargs='+', help='输入文件路径和XML路径')
opt = parser.parse_args()

# 创建一个新列表，将每两个参数作为一对文件路径和XML路径添加到其中
file_paths = []
for i in range(0, len(opt.source), 2):
    file_paths.append((opt.source[i], opt.source[i+1]))

# 遍历新列表中的每个元组
for filePath, xmlPath in file_paths:
    print("文件路径:", filePath)
    print("XML路径:", xmlPath)
    # 调用您的处理函数，例如segment_grain(filePath, xmlPath)
