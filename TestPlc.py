# encoding=utf8
from tkinter import ttk
from tkinter import *
import snap7
from snap7.util import *
import time
import yaml
import os
import ioc
port = 5551
connect_flag = True
a = []
class WidgetsDemo:
    def __init__(self):
        window = Tk()
        window.title("多型号plc数据采集")

        # 添加一个label、entry、button和message到frame2
        frame2 = Frame(window)
        frame2.pack()
        label = Label(frame2, text="请输入IP")
        # label2 = Label(frame2, text="端口")
        label3 = Label(frame2, text="设备型号")
        label4 = Label(frame2, text="插槽号")
        lblDBNo = Label(frame2, text="db")
        lblDBType = Label(frame2, text="数据类型")  ####
        lblDataSz = Label(frame2, text="数据大小(byte)")
        lblDataAd = Label(frame2, text="数据起始地址")
        btnCls = Button(frame2, text="清屏", command=self.cearMsg, width=8)
        btnTstCnn = Button(frame2, text="连接测试", command=self.testCnn, width=8)
        self.v1 = IntVar()
        btnRead = Button(frame2, text="查询数据", command=self.queryData, width=8)
        self.IP = StringVar()
        self.IP.set('192.168.2.178')
        self.slot = IntVar()
        self.ddl = ttk.Combobox(frame2)
        self.slot.set('0')
        self.rack = IntVar()
        current_path = os.path.abspath(os.path.dirname(__file__))
        with open(current_path + '/dir/' + 'y.yaml', 'r') as f:
            temp = yaml.load(f, Loader=yaml.FullLoader)
            print(temp)
            print(temp["first_plc"])
            for i in temp.values():
                a.append(i)
        self.ddl['value'] = a
        self.ddl.current(0)
        self.rack = IntVar()
        print(str(self.ddl.get()))
        self.rack.set('5551')
        self.port = IntVar()
        self.port.set(502)
        self.DBNo = IntVar()
        self.DBType = StringVar()
        self.dataAd = IntVar()
        self.dataSz = IntVar()
        self.data = StringVar()
        self.msg = StringVar()
        self.sendTl = StringVar()
        self.sendTl.set("发送")

        entryIP = Entry(frame2, textvariable=self.IP)
        entryslot = Entry(frame2, textvariable=self.slot)
        entryrack = Entry(frame2, textvariable=self.rack)
        # entryport = Entry(frame2, textvariable=self.port)
        entryDBNo = Entry(frame2, textvariable=self.DBNo)
        entrydataAd = Entry(frame2, textvariable=self.dataAd)
        entrydataSz = Entry(frame2, textvariable=self.dataSz)
        entryDBType = Entry(frame2, textvariable=self.DBType)

        self.btnSendData = Button(frame2, text=self.sendTl.get(), command=self.sendData, width=8)
        label.grid(row=1, column=1)
        entryIP.grid(row=1, column=2)
        # label2.grid(row=1, column=3)
        # entryport.grid(row=1, column=4)
        label3.grid(row=1, column=3)
        # entryslot.grid(row=1, column=4)
        # #下拉框位置
        self.ddl.grid(row=1, column=4)
        label4.grid(row=1, column=5)
        entryrack.grid(row=1, column=6)
        lblDBNo.grid(row=2, column=1)
        lblDBType.grid(row=5, column=1)  #####
        entryDBType.grid(row=5, column=2)  #####
        entryDBNo.grid(row=2, column=2)
        lblDataAd.grid(row=2, column=3)
        entrydataAd.grid(row=2, column=4)
        lblDataSz.grid(row=2, column=5)
        entrydataSz.grid(row=2, column=6)
        btnRead.grid(row=4, column=6, sticky=W)
        self.btnSendData.grid(row=3, column=6, sticky=W)
        btnCls.grid(row=4, column=2, sticky=W)
        btnTstCnn.grid(row=4, column=5)

        lblData = Label(frame2, text="发送数据")
        lblData.grid(row=3, column=1)
        txtData = Entry(frame2, textvariable=self.data, width=62)
        txtData.grid(row=3, column=2, columnspan=4, sticky=W)

        # message.grid(row = 1, column = 4)
        # 添加一个texttext = Text(window)，显示测试的相关信息
        self.txtMsg = Text(window)
        self.txtMsg.pack()
        self.txtMsg.insert(END, "")  # END表示插入到当前文本最后

        window.mainloop()

    # 清空文本框中的信息
    def cearMsg(self):
        self.txtMsg.delete(1.0, END)

    def write_yaml(self):
        data = {'IP': self.IP.get(), 'modle': self.ddl.get(), 'port': self.rack.get()}

        # IOC_data = [{'services': "",
        #             'FX3U': "",
        #             'class': 'plc.'+self.ddl.get()+self.ddl.get()}]
        curpath = os.path.dirname(os.path.realpath(__file__))
        yamlpath = os.path.join(curpath, "data.yaml")
        with open(yamlpath, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True)
    # 创建IOC文件
        IOC_data = {
            "services": {
             "A1": {
              "class": 'plc.' + self.ddl.get() + "." + self.ddl.get()
                }
            }
        }
        curpath_service = os.path.dirname(os.path.realpath(__file__))
        yamlpath_service = os.path.join(curpath_service, "service.yml")
        with open(yamlpath_service, "w", encoding="gbk") as d:
            yaml.dump(IOC_data, d, allow_unicode=True)

    #连接测试

    def testCnn(self):

        self.write_yaml()
        curpath = os.path.dirname(os.path.realpath(__file__))
        service_yml_path = os.path.join(curpath, "service.yml")
        container = ioc.build([service_yml_path])
        # container = ioc.build(['C:/Users/84307/Desktop/three_plc/service.yml'])
        container.get("A1").execution_connect()


    def Text_Show(self,result):
        for i in range(len(result)):
            self.txtMsg.insert(END, result[i]+'\n')

    # 数据查询

    def queryData(self):
        self.write_yaml()
        curpath = os.path.dirname(os.path.realpath(__file__))
        service_yml_path = os.path.join(curpath, "service.yml")
        print(service_yml_path)
        container = ioc.build([service_yml_path])
        # container = ioc.build(['C:/Users/84307/Desktop/three_plc/service.yml'])
        plc_data = container.get("A1").execution_queryDate()
        self.Text_Show(plc_data)


        # def insert(self, index, chars, *args):
        # data = siemens.queryData()
        # connect = plc(self.IP.get(), self.ddl.get(), self.rack.get())
        # data = connect.Connect_plc()
        # self.txtMsg.insert(END, 'i')


        #
        # if result:
        #     # self.txtMsg.insert(END, result[0])
        #     # time.sleep(10)
        #     print(result.__len__())
        #     # self.txtMsg.insert(END, result[0])
        #     result.clear()
    # 发送数据
    def sendData(self):
        # services:
        # A1:
        #
        # class: three_plc.plc.fINSTcp.FinsTcp
        self.txtMsg.insert(END, 'i')
        print("发送")
        # plc = snap7.client.Client()
        # """
        #     Here we replace a piece of data in a db block with new data
        #
        #     Args:
        #        db (int): The db to use
        #        start(int): The start within the db
        #        size(int): The size of the data in bytes
        #        _butearray (enumerable): The data to put in the db
        #     """
        # try:
        #     plc.connect(self.IP.get(), self.rack.get(), self.slot.get())
        #     data = self.data.get()
        #     databyte = plc.db_read(self.DBNo.get(), self.dataAd.get(), self.dataSz.get())
        #     if not data.strip():
        #         self.txtMsg.insert(END, '发送数据不能为空')
        #         return
        #     # plc.db_write(self.DBNo.get(), self.dataAd.get(), data)
        #     if (self.DBType.get() == "int"):
        #         set_int(databyte, 0, data)
        #         plc.write_area(0x84, self.DBNo.get(), self.dataAd.get(), databyte)
        #     elif (self.DBType.get() == "string"):
        #         set_string(databyte, 0, data,256)
        #         plc.write_area(0x84,self.DBNo.get(), self.dataAd.get(),databyte)
        #     elif (self.DBType.get() == "bool"):
        #         data = bool(int(data))
        #         set_bool(databyte,0,0, data)
        #         plc.write_area(0x84,self.DBNo.get(), self.dataAd.get(),databyte)
        #     else:
        #         print('')
        #
        #     # plc.write_area(0x84,1,4)
        # except  Exception as e:
        #     self.txtMsg.insert(END, (e, 'IP:', self.IP.get(), '异常'))
        # finally:
        #     if plc.get_connected():
        #         plc.disconnect()

    # 将bytes字符串转化为bytes
    def StrtoByesarray(self, strdata):
        strarry = strdata.split()
        list = []
        for itm in strarry:
            list.append(itm)

        return bytearray(list)


WidgetsDemo()

