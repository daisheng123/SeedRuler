import socket
import os
import sys
import struct
import  json
import time
# from Demo import model

def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # IP地址留空默认是本机IP地址
        s.bind(('192.168.43.242', 8080))
        s.listen(7)
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    sock, addr = s.accept()
    send(sock,addr)
def send(sock,addr):
    while True:
        print("连接开启，等待传图,进行长宽的测量")
        deal_data(sock, addr)

        os.system('conda activate mmd21')
        os.chdir('C:/Users/15322/Desktop/r3det-on-mmdetection-master')
        os.system(r'python demo/image_demo.py transp/picture_path/112.png work_dirs/r3det_r50_fpn_2x_20200616/r3det_r50_fpn_2x_CustomizeImageSplit.py work_dirs/r3det_r50_fpn_2x_20200616/epoch_100.pth ')
        send2(sock)
        time.sleep(1)
        send3(sock)
def send2(sock):
    while True:
        # filepath是要被发送图片的路径
        print("PC连接到树莓派成功,开始传输图片")
        recvpath = r'C:\Users\15322\Desktop\r3det-on-mmdetection-master\finalsize.jpg'  # 发送的结果图
        filename ='finalsize.jpg'
        share_dir=r'C:\Users\15322\Desktop\r3det-on-mmdetection-master'
        # 第一步：制作固定长度的报头
        header_dic = {
            'filename': filename,  # 1.txt
            'file_size': os.path.getsize(r'%s\%s' % (share_dir, filename))  # 路径/1.txt
        }

        header_json = json.dumps(header_dic)
        header_bytes = header_json.encode('utf-8')

        # 第二步：先发送报头的长度
        sock.send(struct.pack('i', len(header_bytes)))

        # 第三步:再发报头
        sock.send(header_bytes)

        # 第四步：再发送真实的数据
        with open('%s/%s' % (share_dir, filename), 'rb') as f:
            for line in f:
                sock.send(line)
        #print('client filepath: {0}'.format(recvpath))
        print("图片从pc传回树莓派成功")
        break
def send3(sock):
    while True:
        # filepath是要被发送图片的路径
        print("PC连接到树莓派成功,开始传输文档")
        #recvpath = r'C:\Users\15322\Desktop\r3det-on-mmdetection-master\finalsize.jpg'  # 发送的结果图
        filename ='list.txt'
        share_dir=r'C:\Users\15322\Desktop\r3det-on-mmdetection-master'
        # 第一步：制作固定长度的报头
        header_dic = {
            'filename': filename,  # 1.txt
            'file_size': os.path.getsize(r'%s\%s' % (share_dir, filename))  # 路径/1.txt
        }

        header_json = json.dumps(header_dic)
        header_bytes = header_json.encode('utf-8')

        # 第二步：先发送报头的长度
        sock.send(struct.pack('i', len(header_bytes)))
        # 第三步:再发报头
        sock.send(header_bytes)

        # 第四步：再发送真实的数据
        with open('%s/%s' % (share_dir, filename), 'rb') as f:
            for line in f:
                sock.send(line)
        #print('client filepath: {0}'.format(recvpath))
        print("文档从pc传回树莓派成功")
        break
    print("传输完成")


def deal_data(sock,addr):

    # 2、以写的方式打开一个新文件，接收服务端发来的文件的内容写入客户的新文件
    # 第一步：先收报头的长度
    while True:
        obj = sock.recv(4)
        header_size = struct.unpack('i', obj)[0]

        # 第二步：再收报头
        header_bytes = sock.recv(header_size)

        # 第三步：从报头中解析出对真实数据的描述信息
        header_json = header_bytes.decode('utf-8')
        header_dic = json.loads(header_json)
        '''
        header_dic = {
            'filename': filename,  # 1.txt
            'file_size': os.path.getsize(r'%s\%s' % (share_dir, filename))  # 路径/1.txt
        }    
        '''

        total_size = header_dic['file_size']
        file_name = header_dic['filename']
        download_dir =r'C:\Users\15322\Desktop\r3det-on-mmdetection-master\transp\picture_path'
        # 第四步：接收真实的数据
        with open(r'%s\%s' % (download_dir, file_name), 'wb') as f:
            recv_size = 0
            while recv_size < total_size:
                line = sock.recv(1024)
                f.write(line)
                recv_size += len(line)
                #print('总大小：%s   已下载大小：%s' % (total_size, recv_size))
        break


if __name__ == '__main__':
    # 接收到树莓派传来的谷粒拍摄图片
    socket_service()
