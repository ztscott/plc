import socket
import re
import logging
import time
from plc.Plc import plc
import ioc


class FX3U(plc):
    def __init__(self):
        a = self.read_yaml()
        self.plc_ip = a["IP"]
        self.plc_port = a["port"]
        self.plc_name = a["name"]
        self.send = ''
        self.receive = ''
        self.s = None
        # logging.basicConfig(filename='../three_plc/LOG/' + __name__ + '.log',
        #                     format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', level=logging.DEBUG,
        #                     filemode='a', datefmt='%Y-%m-%d%I:%M:%S %p')
        # self.logger = logging.getLogger(__name__)
        # self.logger.disabled = False
    def try_connect(self, keep=False):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.settimeout(3)
            self.s.connect((self.plc_ip, self.plc_port))
        except TimeoutError:
            self.logger.info('connect fail')
            return False


    @staticmethod
    def reverse_per_two_char(chars):
        '''
        reverse '010203' to '030201'
        '''
        return ''.join(reversed(re.findall('..?', chars)))

    def read_register(self,start_digit, digit_num=2, dic=True):
        '''
        Example:
            read D400 single word: read_register('192.168.100.2', 400)
        '''

        str1 = '01FF0A00' + self.reverse_per_two_char('{:0=8x}'.format(start_digit)) \
               + '20440200'
        # self.reverse_per_two_char('{:0=4x}'.format(digit_num))
        msg = bytes.fromhex(str1)  # 转成字节
        self.s.send(msg)
        res = self.s.recv(1024).hex()
        if dic:
            # 十六进制转十进制
            return int(self.reverse_per_two_char(res[-4 * digit_num:]), 16)
        else:
            return int(self.reverse_per_two_char(res[-4 * digit_num:]), 16)

    def execution_connect(self):
        # a = self.read_yaml()
        # self.__init__(plc_ip=a[0], plc_port=a[2], plc_name=a[1])
        self.try_connect(keep=True)
        self.s.close()
        return "连接成功"


    def execution_queryDate(self):
        # a = self.read_yaml()
        # self.__init__(plc_ip=a[0], plc_port=a[2], plc_name=a[1])
        self.try_connect(keep=False)
        result = []
        while True:
            for i in range(3):
                result.append("H" + str(i + 1) + ": " + str((self.read_register(int(i+1)))))
            self.s.close()
            return result
