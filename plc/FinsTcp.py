import socket
import re
import logging
import time
from plc.Plc import plc


class FinsTcp(plc):
    def __init__(self):
        a = self.read_yaml()
        self.plc_ip = a["IP"]
        self.plc_port = a["port"]
        self.plc_name = a["name"]
        self.s = None
        self.FINS = '46494E53'
        self.command_err_code = ['0000000000000000', '0000000100000000', '0000000200000000']
        self.ICF_RSV_GCT = ['800002', 'C00002']
        self.SID = 'FF'
        self.send = ''
        # self.receive = ''
        # logging.basicConfig(filename='../LOG/' + __name__ + '1.log',
        #                     format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', level=logging.DEBUG,
        #                     filemode='a', datefmt='%Y-%m-%d %I:%M:%S %p')
        # self.logger = logging.getLogger(__name__)
        # self.logger.disabled = False

    def try_connect(self, keep=False):
        """
        FINSTcp 握手
        :param keep: 保持连接
        :return:
        """
        try:
            if self.s is None:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.settimeout(3)
                self.s.connect((self.plc_ip, self.plc_port))
        except TimeoutError:
            self.logger.error('connect fail')
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
        # start_digit = start_digit.hex()
        str1 = '4649 4E53 0000 001A 0000 0002 0000 0000 800002 002100 00C000 00 0101 B2 00' + start_digit + '00 0001'
        '''
        46494E53 0000001A（发送字节数） 00000002 00000000
            800002 002100 00C000 00
            0101（读代码） 82（DM 地址） 000000（D0） 0002（2 个数据）
        '''

        msg = bytes.fromhex(str1)  # 转成字节
        self.s.send(msg)
        res = self.s.recv(1024).hex()
        if dic:
            # 十六进制转十进制
            return int(res[60:64], 16)
        else:
            return int(res[60:64], 16)

    def execution_connect(self):
        self.try_connect(keep=True)
        self.s.close()
        return "连接成功"

    def execution_queryDate(self):
        a = self.read_yaml()
        self.try_connect(keep=True)
        result = []
        while True:
            for i in range(100, 103):
                s = hex(i)[2:]
                result.append("H" + str(i + 1) + ": " + str((self.read_register(s))))
            self.s.close()
            return result
