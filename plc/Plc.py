import socket
import re
import time
import yaml
import os


class plc(object):
    def __init__(self, plc_ip="", plc_port="1", plc_name="1"):
        self.plc_ip = plc_ip
        self.plc_port = plc_port
        self.plc_name = plc_name
        # self.start_digit = 1

    def read_yaml(self):
        with open("./data.yml", 'r') as f:
            temp = yaml.load(f, Loader=yaml.FullLoader)
            return temp

    def try_connect(self,keep=False):
        # 连接
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.settimeout(3)
            self.s.connect((self.plc_ip, self.plc_port))
        except TimeoutError:
            self.logger.error('connect fail')
            return False

    def returnStr(self, start_digit):
        a=self.read_yaml()
        if a[1] == "FX3U":
            str1 = '01FF0A00' + self.reverse_per_two_char('{:0=8x}'.format(start_digit)) + '20440200'  # 三菱
        elif a[1] == "FinsTcp":
            str1 = '4649 4E53 0000 001A 0000 0002 0000 0000 800002 002100 00C000 00 0101 B2 00' + start_digit + '000001'       # 欧姆龙
        else:
            print("无对应型号")
        return str1

    @staticmethod
    def reverse_per_two_char(chars):
        '''
        reverse '010203' to '030201'
        '''
        return ''.join(reversed(re.findall('..?', chars)))

    def read(self,start_digit, digit_num=2, dic=True):
        str1=self.returnStr(1)
        msg = bytes.fromhex(str1)  # 转成字节
        self.s.send(msg)
        res = self.s.recv(1024).hex()
        # print(res)
        if dic:
            # 十六进制转十进制
            return int(self.reverse_per_two_char(res[4 * digit_num:]), 16)
        else:
            return int(self.reverse_per_two_char(res[4 * digit_num:]), 16)

    def execution(self):
        a = self.read_yaml()
        self.__init__(plc_ip=a[0], plc_port=a[2], plc_name=a[1])
        self.try_connect(keep=True)
        print("进行A类的execution方法")

    #设备连接
    def Connect_plc(self):
        a = self.read_yaml()
        self.__init__(plc_ip=a[0], plc_port=a[2], plc_name=a[1])
        self.try_connect(keep=True)
        result = []

        while True:
            for i in range(100, 200):
                # s = hex(i)[2:]
                # result.append("H" + str(i+1) + ": " + str((self.read(s))))
                result.append("D" + str(i + 1) + ": " + str((self.read(int(i + 1)))))

            if result:
                time.sleep(2)
                result.clear()


    # def write(self):
    #     print(self.plc_name+", xie")
# if __name__ == '__main__':
#     print("main")
#     finsTcp=plc(plc_ip="192.168.2.179",plc_port=9600,plc_name="Oml")
#     finsTcp.try_connect(keep=True)
#     new = True
#     data=[]
#     result=[]
#     while True:
#         for i in range(100):
#             s = hex(i)[2:]
#             result.append("H" + str(i + 1) + ": " + str((finsTcp.read(s))))
#         if result:
#             time.sleep(2)
#             print(result)
#             result.clear()
# #
#
#




