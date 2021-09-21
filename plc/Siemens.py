from plc.Plc import plc
import snap7
from snap7.util import *
class Siemens(plc):
    def __init__(self):
        a = self.read_yaml()
        self.plc_ip = a["IP"]
        self.plc_port = a["port"]
        self.plc_name = a["name"]
        self.DBNo = a["db"]
        self.dataAd = a["dataAd"]
        self.dataSz = a["dataSz"]
        self.DBType = a["dataType"]
        self.plc = snap7.client.Client()


    def try_connect(self, keep=False):
        try:
            self.plc.connect(self.plc_ip, 0, self.plc_port)
            return True
        except Exception as e:
            return False


    def read(self):
        plc = snap7.client.Client()
        try:
            plc.connect(self.IP.get(), self.rack.get(), self.slot.get())
            # data = get_int(plc.read_area(0x84, 1, 2, 2), 0),
            # data_byte= plc.read_area(0x84,self.DBNo.get(),self.dataAd,self.dataSz)
            # data = plc.db_read(self.DBNo.get(),self.dataAd.get(),self.dataSz.get()),
            databyte = plc.db_read(self.DBNo.get(), self.dataAd.get(), self.dataSz.get())
            if (self.DBType == "int"):
                data = get_int(databyte, 0),
            elif (self.DBType == "string"):
                data = get_string(databyte, 0, 256),
            elif (self.DBType == "bool"):
                data = get_bool(databyte, 0, 0)
            else:
                print("无此类型")

            return data
        except  Exception as e:
            return e
        finally:
            if plc.get_connected():
                plc.disconnect()

    def execution_connect(self):
        if self.try_connect():
            self.plc.disconnect()
            return "连接成功"
        else:
            return "连接失败"

    def execution_queryDate(self):
        try:
            self.plc.connect(self.plc_ip, 0, self.plc_port)
            # data = get_int(plc.read_area(0x84, 1, 2, 2), 0),
            # data_byte= plc.read_area(0x84,self.DBNo.get(),self.dataAd,self.dataSz)
            # data = plc.db_read(self.DBNo.get(),self.dataAd.get(),self.dataSz.get()),
            databyte = self.plc.db_read(self.DBNo, self.dataAd, self.dataSz)
            if (self.DBType == "int"):
                data = get_int(databyte, 0),
            elif (self.DBType == "string"):
                data = get_string(databyte, 0, 256),
            elif (self.DBType == "bool"):
                data = get_bool(databyte, 0, 0)
            else:
                return "无此类型"

            return data
        except Exception as e:
            return "query fail!"
        finally:
            if self.plc.get_connected():
                self.plc.disconnect()