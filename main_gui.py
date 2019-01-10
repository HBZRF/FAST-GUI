#!/usr/bin/env python3
# -*- coding: utf8 -*-
# 导入用到的模块
from gui_config import *
import threading
import time, datetime  # 导入时间模块
from tkinter import *
import requests
from tkinter import filedialog
from tkinter.filedialog import askdirectory
from tkinter import messagebox  # 导入提示模块
from tkinter import scrolledtext #导入滚动text

# 定义全局变量
global PATH2  # 保存文件路径
global FILE_NAME  # 打开的xls文件名字
# global var
global OMC_IP
global OMC_PORT
global OMC_USER
global OMC_PW
global OMC_OSS
global ID_MIN
global ID_MAX
global PACK_NUM
global PACK_LEN
global SELECT_MODE  # 保存选择ping方式的变量
global he  # 保存当前时间
global ENB_IP
global oss_config_file  # oss Oracle配置文件的名字
FILE_NAME = ""
class App(guiConfig):
    def __init__(self):
        # 定义UI中用到的变量
        
        self.jqghoupt = ''
        self.xnlcoupt = ''
        self.jdfxoupt = ''
        self.mrfxoupt = ''
        self.zcsloupt = ''
        
        self.current_exec_task = 0
        self.execing_funcId = {}
        self.date_start = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y%m%d%H")
        self.date_end = (datetime.datetime.now()).strftime("%Y%m%d%H")
        self.city = ''
        self.is_download_execing = 0
        self.root = Tk()
        self.dfbg = self.root.cget('bg')#窗口默认颜色
        self.root.title("FAST-自动化运维工具-RN-2",)
        self.root.resizable(0, 0)  # 阻止窗口调整
        # root.geometry("600x600+450+210")#width x height;起始坐标
        self.frame = Frame(self.root,width=200)
        self.frame.grid()
        #self.frame.grid_propagate(0)
        self.selected_func = 0
    def oracle_oupt(self):
        self.usrid = StringVar()
        self.usrpwd = StringVar()
        self.get_port = StringVar()
        self.get_user = StringVar()
        self.get_pw = StringVar()
        self.get_oss = StringVar()
        self.get_ip = StringVar()
        self.get_date_start = StringVar()
        self.get_date_end = StringVar()
        self.get_city = StringVar()
        self.frame1 = Frame(self.root, bd=1, relief=RIDGE,width=580,height=200 )
        self.frame1.grid(row=0, column=0, sticky=W+N+S+E,padx=2)
        #self.frame1.grid_propagate(0)
        # 创建Oracle配置UI
        self.frame12 = Frame(self.frame1, bd=0,  relief=GROOVE)
        self.frame12.grid(row=0, column=0,sticky=W,padx = 0,pady=2)
        #self.frame12.grid_propagate(0)
        Label(self.frame12, text="Oracle 配置",).grid(row=0,  column=0, columnspan=2, pady=2,sticky=N)
        Label(self.frame12, text="OSS IP地址:").grid(row=1, column=0, sticky=W)
        Entry(self.frame12, textvariable=self.get_ip, bd=1).grid(row=1, column=1)
        Label(self.frame12, text="OSS 端口号:").grid(row=2, column=0, sticky=W)
        Entry(self.frame12, textvariable=self.get_port, bd=1).grid(row=2, column=1)
        Label(self.frame12, text="OSS 用户名:").grid(row=3, column=0, sticky=W)
        Entry(self.frame12, textvariable=self.get_user, bd=1).grid(row=3, column=1)
        Label(self.frame12, text="OSS 密码:").grid(row=4, column=0, sticky=W)
        Entry(self.frame12, show='*',textvariable=self.get_pw, bd=1).grid(row=4, column=1)
        Label(self.frame12, text="OSS 服务名称:").grid(row=5, column=0, sticky=W)
        Entry(self.frame12, textvariable=self.get_oss, bd=1).grid(row=5, column=1)
        self.button_frame = Frame(self.frame12)
        self.conntest = Button(self.button_frame,bg = self.dfbg, text="连通性测试", command=self.oracle_test,pady=1)
        self.conntest.grid(row=121, column=0, padx=1)
        Button(self.button_frame, text="保存配置", command=self.oracle_save).grid(row=121, column=1, padx=1,pady=6)
        Button(self.button_frame, text="重置配置", command=self.oracle_reconfig).grid(row=121, column=2, padx=1,pady=6)
        self.button_frame.grid(columnspan=2)

        # 创建输出窗口
        # Label(frame1, text="批量PING基站方式(需要填写网管Oracle相关配置)").grid(pady=15, row=10, columnspan=2)
        self.frame11 = Frame(self.frame1, bd=1, relief=GROOVE)
        self.frame11.grid(row=0, column=1,sticky=N+E+S)
        Label(self.frame11, text="LOG输出：").grid(row=0, column=0, pady=4,)
        self.scr = scrolledtext.ScrolledText(self.frame11,   wrap=WORD,height=10,width=35)
        self.scr.grid(row=1, column=0,ipadx=2,sticky=N+S+E,ipady = 2)
    def func_button(self):
        # 创建功能模块UI
        self.frame2 = Frame(self.root, bd=4, relief=RIDGE, width=580,height=37)
        self.button_func_0 = Button(self.frame2, bg='DarkGray', text="精确规划", command=self.change_select(0),)
        self.button_func_0.grid(row=0, column=0)
        self.button_func_1 = Button(self.frame2, bg=self.dfbg, text="虚拟路测", command=self.change_select(1),)
        self.button_func_1.grid(row=0, column=1)
        self.button_func_2 = Button(self.frame2, bg=self.dfbg, text="竞对分析", command=self.change_select(2),)
        self.button_func_2.grid(row=0, column=2)
        self.button_func_3 = Button(self.frame2, bg=self.dfbg, text="MR分析", command=self.change_select(3),)
        self.button_func_3.grid(row=0, column=3)
        self.button_func_4 = Button(self.frame2, bg=self.dfbg, text="众筹扫楼", command=self.change_select(4),)
        self.button_func_4.grid(row=0, column=4)
        self.button_func_5 = Button(self.frame2, bg=self.dfbg, text="预留功能", command=self.change_select(5),state = 'disabled')
        self.button_func_5.grid(row=0, column=5,sticky=W+N+S+E)
        self.frame2.grid(row=1, column=0,sticky=W)
        #self.frame2.grid_propagate(0)
        self.temp_li = [self.button_func_0,self.button_func_1, self.button_func_2, self.button_func_3, self.button_func_4,
                        self.button_func_5, ]
    def func_moudle(self):
        entry_width = 11
        self.frame3 = Frame(self.root, bd=1, relief=RIDGE, width=580,height=260 )
        self.frame3.grid(row=2, column=0,sticky=W,padx=2)
        #self.frame3.grid_propagate(0)
        # 创建功能模块UI

        # 创建功能模块UI(part-1)
        self.frame31 = Frame(self.frame3, bd=1, relief=RIDGE, height=130)
        self.frame31.grid(row=0, column=0,sticky=W)        
        self.frame311 = Frame(self.frame31, bd=1, relief=RIDGE )       
        self.frame311.grid(row=0, column=0,sticky=W,padx=0)# 创建功能模块UI(upper-left-part)
        #self.frame311.grid_propagate(0) #part-1开始
        tma = Label(self.frame311, text="数据核查" ,width=6,bg = 'DarkGreen')
        tma.grid(row=0, column=0, sticky=W+N+S+E,columnspan = 9,padx=2)           
        tma = Label(self.frame311,  text="开始时间:" ,width=6,)
        tma.grid(row=1, column=0, sticky=W,columnspan = 3, padx = 2)
        tmb = Entry(self.frame311, width = entry_width,textvariable=self.get_date_start, bd=1)
        tmb.grid(row=1, padx = 2,column=3,columnspan = 1) 
        self.get_date_start.set(self.date_start)
        tmc = Label(self.frame311,  text="结束时间:",width=6, )
        tmc.grid(row=2, column=0, padx = 2, sticky=W,columnspan = 3)
        tmd = Entry(self.frame311,  textvariable=self.get_date_end, bd=1,width = entry_width)
        tmd.grid(row=2, column=3, padx = 2,sticky=W,columnspan = 1)
        self.get_date_end.set(self.date_end)
        tme = Label(self.frame311,width=5,  text="城市：",)
        tme.grid(row=3, column=0, padx = 2, sticky=E,columnspan = 3)
        Entry(self.frame311,  textvariable=self.get_city, bd=1,width = entry_width).grid(row=3, column=3, padx = 2,columnspan =3,sticky=W) 
        
        self.get_city.set('SHENYANG')
        Button(self.frame311,text="预留",state = 'disabled',width = 18).grid(row=1,column=5,rowspan = 3,columnspan = 2, sticky=W+N+S+E,padx = 2)
        self.bt_sjhc = Button(self.frame311,bg = 'DarkGray',text="开始\n核查",command=self.exec_func,width = 8, height=3)
        self.bt_sjhc.grid(row=4,rowspan=2, column=6,columnspan = 1,sticky=E,padx =2 )
        self.bt_cphj = Button(self.frame311,bg = 'DarkGray',text="重跑\n汇聚",width = 8, height=3)
        self.bt_cphj.grid(row=4,rowspan=2, column=5,columnspan = 1,sticky=E,padx =2 )
        #Button(self.frame311,width = 10).grid(row=6, column=4,columnspan = 1,sticky=E,padx =2 )
        
        self.frame312 = Frame(self.frame31, bd=1, relief=RIDGE )# 创建功能模块UI(upper-right-part)
        self.frame312.grid(row=0, column=1)
        Label(self.frame312,  text="指标提取:" ,bg = 'DarkGreen',width=8,).grid(row=0, column=0, sticky=W+N+S+E,columnspan = 9,padx=2) 
        Label(self.frame312,  text="开始时间:" ,width=8,).grid(row=1, column=0, sticky=W,columnspan = 3, padx = 2)        
        Entry(self.frame312,  width = entry_width,textvariable=self.get_date_start, bd=1).grid(row=1, padx = 2,column=3,columnspan = 1)       
        self.get_date_start.set(self.date_start)
        Label(self.frame312,  text="结束时间:",width=8,).grid(row=2, column=0, padx = 2, sticky=W,columnspan = 3)       
        Entry(self.frame312,  textvariable=self.get_date_end, bd=1,width = entry_width).grid(row=2, column=3, padx = 2,sticky=W,columnspan = 1)     
        self.get_date_end.set(self.date_end)
        Label(self.frame312,width=4,  text="城市：",).grid(row=3, column=0, padx = 2, sticky=E,columnspan = 3)
        Entry(self.frame312,  textvariable=self.get_city, bd=1,width = entry_width).grid(row=3, column=3, ipadx = 0,columnspan =1) 
        self.get_city.set('SHENYANG')        
        Button(self.frame312,text="预留",state = 'disabled',width = 18).grid(row=1,column=5,rowspan = 3,columnspan = 2, sticky=W+N+S+E,padx = 2)
        self.bt_sjhc = Button(self.frame312,bg = 'DarkGray',text="开始\n核查",command=self.exec_func,width = 8, height=3)
        self.bt_sjhc.grid(row=4,rowspan=2, column=6,columnspan = 1,sticky=E,padx =2 )
        self.bt_cphj = Button(self.frame312,bg = 'DarkGray',text="重跑\n汇聚",width = 8, height=3)
        self.bt_cphj.grid(row=4,rowspan=2, column=5,columnspan = 1,sticky=E,padx =2 )
        #Button(self.frame312,width = 10).grid(row=6, column=4,columnspan = 1,sticky=E,padx =2 )
        
        # 创建功能模块UI(part-2)
        self.frame32 = Frame(self.frame3, bd=1, relief=RIDGE, height=130)
        self.frame32.grid(row=1, column=0,sticky=W)        
        self.frame321 = Frame(self.frame32, bd=1, relief=RIDGE )       
        self.frame321.grid(row=0, column=0,)# 创建功能模块UI(lower-right-part)        
        Label(self.frame321,  text="数据处理:" ,width=8,bg = 'DarkGreen').grid(row=0, column=0, sticky=W+N+S+E,columnspan = 9,padx=2) 
        Label(self.frame321, text="开始时间:" ,width=6,).grid(row=1, column=0, sticky=W,columnspan = 3, padx = 2)        
        Entry(self.frame321,  width = entry_width,textvariable=self.get_date_start, bd=1).grid(row=1, padx = 2,column=3,columnspan = 1)       
        self.get_date_start.set(self.date_start)
        Label(self.frame321,  text="结束时间:",width=6, ).grid(row=2, column=0, padx = 2, sticky=W,columnspan = 3)       
        Entry(self.frame321,  textvariable=self.get_date_end, bd=1,width = entry_width).grid(row=2, column=3, padx = 2,sticky=W,columnspan = 1)     
        self.get_date_end.set(self.date_end)
        Label(self.frame321,width=5,  text="城市：").grid(row=3, column=0, padx = 2, sticky=E,columnspan = 3)
        Entry(self.frame321,  textvariable=self.get_city, bd=1,width = entry_width).grid(row=3, column=3, ipadx = 0,columnspan =1) 
        self.get_city.set('SHENYANG')        
        Button(self.frame321,text="预留",state = 'disabled',width = 18).grid(row=1,column=5,rowspan = 3,columnspan = 2, sticky=W+N+S+E,padx = 2)
        self.bt_sjcl = Button(self.frame321,bg = 'DarkGray',text="开始\n核查",command=self.exec_func,width = 8, height=3)
        self.bt_sjcl.grid(row=4,rowspan=2, column=6,columnspan = 1,sticky=E,padx =2 )
        self.bt_sjcl = Button(self.frame321,bg = 'DarkGray',text="重跑\n汇聚",width = 8, height=3)
        self.bt_sjcl.grid(row=4,rowspan=2, column=5,columnspan = 1,sticky=E,padx =2 )

        self.frame322 = Frame(self.frame32, bd=1, relief=RIDGE, )# 创建功能模块UI(lower-right-part)
        self.frame322.grid(row=0, column=1,sticky=NW,padx=0)
        self.frame322_1 = Frame(self.frame322, bd=1, relief=RIDGE, )
        self.frame322_1.grid(row=0, column=0,sticky=NW,padx=0)# 创建功能模块UI(upper-left-part)
        self.frame322_2 = Frame(self.frame322, bd=1, relief=RIDGE, )
        self.frame322_2.grid(row=1, column=0,sticky=NW,padx=0)
        
        Label(self.frame322_1,  text="资源下载:" ,width=8,bg = 'DarkGreen').grid(row=0, column=0, sticky=W+N+S+E,columnspan = 4,padx=2,) 
        Label(self.frame322_1, text="用户名:" ,width=9,).grid(row=1, column=0, sticky=W,columnspan = 1, padx = 2)
        #Entry(self.frame322,width=10, textvariable=self.usrid, bd=1).grid(row=0,column=1,sticky=W+E+N+S)
        Entry(self.frame322_1,  width = 8,textvariable=self.usrid, bd=1).grid(row=1,  padx = 2,column=1,columnspan = 1)       
        Label(self.frame322_1,  text="密码:",width=8, ).grid(row=1, column=2, padx = 2, sticky=W,columnspan = 1)
        
        Entry(self.frame322_1, show='*', textvariable=self.usrpwd, bd=1,width = entry_width).grid(row=1, column=3, padx = 2,sticky=W,columnspan = 1)
        
        

        self.bt_0 = Button(self.frame322_2,width=12,  text="MDT解析软件",)
        self.bt_0.grid(row=0, column=0, padx = 2,pady=2, sticky=E,)
        self.bt_1 = Button(self.frame322_2,width=12,  text="自动化推送",)
        self.bt_1.grid(row=0, column=1, padx = 2,pady=2, sticky=E,)
        self.bt_2 = Button(self.frame322_2,width=12,  text="入库推送",)
        self.bt_2.grid(row=0, column=2, padx = 2,pady=2, sticky=E,)
       
        self.bt_3 = Button(self.frame322_2,width=12,  text="MR解析软件",)
        self.bt_3.grid(row=1, column=0, padx = 2,pady=3, sticky=E,)
        self.bt_4 = Button(self.frame322_2,width=12,  text="自动化采集",)
        self.bt_4.grid(row=1, column=1, padx = 2, pady=3,sticky=E,)
        self.bt_5 = Button(self.frame322_2,width=12,  text="预留",state = 'disabled')
        self.bt_5.grid(row=1, column=2, padx = 2,pady=3, sticky=E,)
        
        self.bt_6 = Button(self.frame322_2,width=12,  text="预留",state = 'disabled')
        self.bt_6.grid(row=2, column=0, padx = 2, pady=3,sticky=E,)
        self.bt_7 = Button(self.frame322_2,width=12,  text="预留",state = 'disabled')
        self.bt_7.grid(row=2, column=1, padx = 2, pady=3,sticky=E,)
        self.bt_8 = Button(self.frame322_2,width=12,  text="预留",state = 'disabled')
        self.bt_8.grid(row=2, column=2, padx = 2, pady=3,sticky=E,)
        

        self.temp_download_li = [self.bt_0,self.bt_1,self.bt_2,self.bt_3,self.bt_4,self.bt_5,self.bt_6,self.bt_7,self.bt_8]
        self.temp_resource_name = ['MDT','AUTO_SEND','DB_IN','MR_paser','AUTO_PASER',]

        
    def footer(self):        
        self.frame4 = Frame(self.root,  relief=RAISED,  height=48,)
        Label(self.frame4, text="Copyright © 2019 - 2029 HuaNuo Technology . All Rights Reserved.华诺科技 \n版权所有 ",bg = self.dfbg,state = 'disabled').grid(sticky=W+E+N+S)
        self.frame4.grid()
        #self.frame4.grid_propagate(0)

    def change_select(self, nbr):
        def xx():
            self.selected_func = nbr
            self.scr.delete(1.0, END) # 使用 delete
            if nbr ==0:
                self.scr.insert("insert", self.jqghoupt)
            elif nbr == 1:
                self.scr.insert("insert", self.xnlcoupt)
            elif nbr == 2:
                self.scr.insert("insert", self.jdfxoupt)
            elif nbr == 3:
                self.scr.insert("insert", self.mrfxoupt)
            elif nbr == 4:
                self.scr.insert("insert", self.zcsloupt)
            else:
                self.scr.insert("insert", '')
            if self.temp_li[nbr]['bg'] == 'DarkGray':
                pass
            else:
                self.temp_li[nbr]['bg'] = 'DarkGray'
                
                for i in range(len(self.temp_li)):
                    if i == nbr:
                        pass
                    else:
                        self.temp_li[i]['bg'] = self.dfbg
                if nbr in self.execing_funcId:
                    self.bt_sjhc['state'] = 'disabled'
                    self.bt_sjhc['bg'] = 'DarkGray'                    
                else:
                    self.bt_sjhc['state'] = 'active'
                    self.bt_sjhc['bg'] = self.dfbg
                    
                    
        return xx
    def downloadReq(self, nbr):
        def xx():
            path = str(self.temp_resource_name[nbr]) + '.zip'
            if not self.usrid.get():
                messagebox.showerror('FAST-自动化运维工具-RN-2', u'用户名不能为空！')
                return
            elif not self.usrpwd.get():
                messagebox.showerror('FAST-自动化运维工具-RN-2', u'密码不能为空！')
                return
            else:
                try:
                    t= threading.Thread(target=self.down_and_save,args=(self.temp_download_li[nbr],path))#创建线程
                    t.setDaemon(True)#设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
                    t.start()#开启线程

                except Exception as e:
                    if u'由于目标计算机积极拒' in str(e):
                        messagebox.showerror('FAST-自动化运维工具-RN-2', u'请检查网络连接或联系管理员处理！')
                    else:
                        messagebox.showerror('FAST-自动化运维工具-RN-2', e)
        return xx
    def down_and_save(self,button,file_name):
        if not self.is_download_execing:
            try:
                self.is_download_execing = 1
                button['state'] = 'disabled'
                button['bg'] = 'DarkGray'
                url = 'http://nokia-nsb.com/download/{}/?usr={}&pwd={}'.format(file_name,self.usrid.get(),self.usrpwd.get())
                res = requests.get(url)
                if res.status_code == 401:
                    messagebox.showerror('FAST-自动化运维工具-RN-2', u'用户名、密码不匹配！！')
                    return
                elif res.status_code == 404:
                    messagebox.showerror('FAST-自动化运维工具-RN-2', u'访问的资源不存在，请联系管理员处理！！')
                    return
                elif res.status_code == 500:
                    messagebox.showerror('FAST-自动化运维工具-RN-2', u'服务器内部故障，请联系管理员处理！！')
                    return
                elif res.status_code == 200:
                    self.safe_save('./download')
                    file = './download/%s'%file_name
                    with open(file,'wb') as f:
                        f.write(res.content)
                    messagebox.showerror('FAST-自动化运维工具-RN-2', u'下载成功，存储在%s！！'%file)

                else:
                    raise Exception("访问在线资源服务器时发生故障，请稍后重试或联系管理处理！")
                    return
            except Exception as e:
                if u'由于目标计算机积极拒' in str(e):
                    messagebox.showerror('FAST-自动化运维工具-RN-2', u'请检查网络连接或联系管理员处理！')
                else:
                    messagebox.showerror('FAST-自动化运维工具-RN-2',e)
            finally:
                self.is_download_execing = 0
                button['state'] = 'active'
                button['bg'] = self.dfbg 
                
        else:
            messagebox.showerror('FAST-自动化运维工具-RN-2', u'其它资源正在下载，请稍后再试！！')
            
    def is_date_valied(self,k):
        if not k.isdigit():
            messagebox.showerror('FAST-自动化运维工具-RN-2','日期为数字格式，请正确输入！')
            return False
        try:
            time.strptime(k, "%Y%m%d%H")
            return True
        except Exception as e:
            #if ''
            messagebox.showerror('FAST-自动化运维工具-RN-2',e)
            return False
            
    def exec_func(self,task_id):
        if not self.get_ip.get():
            tkinter.messagebox.showerror(title='FAST-自动化运维工具-RN-2', message='请输入Oracle数据库ip！！')
            return
        elif not self.get_port.get():
            tkinter.messagebox.showerror(title='FAST-自动化运维工具-RN-2', message='请输入Oracle数据库端口号！！')
            return
        elif not self.get_port.get().isdigit():
            tkinter.messagebox.showerror(title='FAST-自动化运维工具-RN-2', message='Oracle数据库端口号需要为数字！！')
            return
        elif not self.get_user.get():
            tkinter.messagebox.showerror(title='FAST-自动化运维工具-RN-2', message='请输入Oracle数据库用户名！！')
            return
        elif not self.get_pw.get():
            tkinter.messagebox.showerror(title='FAST-自动化运维工具-RN-2', message='请输入Oracle数据库密码！！')
            return
        elif not self.get_oss.get():
            tkinter.messagebox.showerror(title='FAST-自动化运维工具-RN-2', message='请输入Oracle数据库名称！！')
            return
        else:
            pass
        if len(self.execing_funcId) >= 2:
            messagebox.showerror('FAST-自动化运维工具-RN-2','目前已有两个任务在运行，请稍后再试！')
            return
        if self.is_date_valied(self.get_date_end.get()) and self.is_date_valied(self.get_date_start.get()):
            pass
        else:
            return
        if not self.get_city.get():
            messagebox.showerror('FAST-自动化运维工具-RN-2','城市为空,请填写城市名称，如：SHENYANG！')
            return    
        try:
            tmp_li = []
            exec_id = self.selected_func        
            DB_URI = '{}/{}@{}:{}/{}'.format(self.get_user.get(),self.get_pw.get(),self.get_ip.get(),self.get_port.get(),self.get_oss.get())
            #conn = cx_Oracle.connect(DB_URI)
            city = self.get_city.get()
            if self.selected_func == 4:#业务范畴id
                if task_id == 1:#任务类型id，1 数据核查， 2 重跑汇聚
                    t= threading.Thread(target=self.zcsl,args=(city,self.get_date_start.get(),self.get_date_end.get(),exec_id,DB_URI))#创建线程
                    t.setDaemon(True)#设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
                    t.start()#开启线程
            elif self.selected_func == 1:
                t= threading.Thread(target=self.xnlc,args=(city,self.get_date_start.get(),self.get_date_end.get(),exec_id,DB_URI))#创建线程
                t.setDaemon(True)#设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
                t.start()#开启线程
            else:
                messagebox.showerror('FAST-自动化运维工具-RN-2','二期功能，目前暂未开放！！')

        except Exception as e:
            messagebox.showerror('FAST-自动化运维工具-RN-2',e)
            return           

        
    def run(self):
        self.root.mainloop()
    def zcsl(self,city,start_date,end_date,exec_id,DB_URI):
        try:
            self.zcsloupt = ''
            #exec_id = str(exec_id)
            self.execing_funcId.append(exec_id)
            self.bt_sjhc['state'] = 'disabled'
            self.bt_sjhc['bg'] = 'DarkGray'
            #----------DIM_MRO_BUILDING_DAY------------------
            zcsl_1 = "select * from DIM_MRO_BUILDING_DAY where CITY = '" +city +"' AND SDATE >= TO_DATE('" + start_date + "', 'YYYYMMDD') AND SDATE =< TO_DATE('" + end_date+"', 'YYYYMMDD') AND rownum=1;"
            #----------cfg_map_building_mapx------------------
            zcsl_2 = "select * from cfg_map_building_mapx where CITY = '"+ city + "' AND rownum=1;"

            #----------DIM_MRO_BUILDING_CELL_DAY------------------
            zcsl_3 ="select * from DIM_MRO_BUILDING_CELL_DAY where CITY = '" +city +"' AND SDATE >= TO_DATE('" + start_date + "', 'YYYYMMDD') AND SDATE =< TO_DATE('" + end_date+"', 'YYYYMMDD') AND rownum=1;"

            #----------DIM_MRO_BUILDING_GRID10_DAY------------------
            zcsl_4 = "select * from DIM_MRO_BUILDING_GRID10_DAY where CITY = '" + city + "' AND SDATE >= TO_DATE('" + start_date + "', 'YYYYMMDD') AND SDATE =< TO_DATE('" + end_date+"', 'YYYYMMDD') AND rownum=1;"
            #----------TDLTE_MRO_PNN_GRID10_CELL_DAY------------------
            zcsl_5 = "select * from TDLTE_MRO_PNN_GRID10_CELL_DAY where CITY = '" + city + "' AND SDATE >= TO_DATE('" + start_date + "', 'YYYYMMDD') AND SDATE =< TO_DATE('" + end_date+"', 'YYYYMMDD') AND rownum=1;"
            #----------TDLTE_MRO_PNN_GRID10_CELL_HOUR------------------
            zcsl_6 = "select * from TDLTE_MRO_PNN_GRID10_CELL_HOUR where CITY = '" + city + "' AND SDATE >= TO_DATE('" + start_date + "', 'YYYYMMDD') AND SDATE =< TO_DATE('" + end_date+"', 'YYYYMMDD') AND rownum=1;"
            #----------TDLTE_MRO_LOCATE_HOUR------------------
            zcsl_7 = "select * from TDLTE_MRO_LOCATE_HOUR where CITY = '" + city + "' AND SDATE >= TO_DATE('" + start_date + "', 'YYYYMMDD') AND SDATE =< TO_DATE('" + end_date+"', 'YYYYMMDD') AND rownum=1;"
            #----------CFG_BUILDING_MAPPING_GRID10------------------
            zcsl_8 = "select * from CFG_BUILDING_MAPPING_GRID10 where CITY = '" + city + "'  AND rownum=1;"
            #----------CFG_SITEINFO_TDLTE------------------
            zcsl_9 = "select * from CFG_SITEINFO_TDLTE where CITY = '"+ city + "'  AND rownum=1;"
            

            zcsl_sql_1 = {'name':'DIM_MRO_BUILDING_DAY',
                          'sql':zcsl_1
                          ,}
            zcsl_sql_2 = {'name':'cfg_map_building_mapx',
                          'sql':zcsl_2
                          ,}
            zcsl_sql_3 = {'name':'DIM_MRO_BUILDING_CELL_DAY',
                          'sql':zcsl_3
                          ,}
            zcsl_sql_4 = {'name':'DIM_MRO_BUILDING_GRID10_DAY',
                          'sql':zcsl_4
                          ,}
            zcsl_sql_5 = {'name':'TDLTE_MRO_PNN_GRID10_CELL_DAY',
                          'sql':zcsl_5
                          ,}
            zcsl_sql_6 = {'name':'TDLTE_MRO_PNN_GRID10_CELL_HOUR',
                          'sql':zcsl_6
                          ,}
            zcsl_sql_7 = {'name':'TDLTE_MRO_LOCATE_HOUR',
                          'sql':zcsl_7
                          ,}
            zcsl_sql_8 = {'name':'CFG_BUILDING_MAPPING_GRID10',
                          'sql':zcsl_8
                          ,}
            zcsl_sql_9 = {'name':'CFG_SITEINFO_TDLTE',
                          'sql':zcsl_9
                          ,}          
            steb_1 = [{'pre_task':'',
                      'tasks':[zcsl_sql_1,zcsl_sql_2]}]
            steb_2 = [{'pre_task':zcsl_sql_2,
                      'tasks':[zcsl_sql_3,zcsl_sql_4]}]
            steb_3 = [
                     {'pre_task':zcsl_sql_3,
                      'tasks':[zcsl_sql_2,zcsl_sql_9]
                      },
                     {'pre_task':zcsl_sql_4,
                      'tasks':[zcsl_sql_8,zcsl_sql_5]
                      },
                      ]
            steb_4 = [{'pre_task':zcsl_sql_5,
                      'tasks':[zcsl_sql_6,]}]
            steb_5 = [{'pre_task':zcsl_sql_6,
                      'tasks':[zcsl_sql_7,]}]
            task_flow = [steb_1,steb_2,steb_3,steb_4,steb_5]
            noDataTask = []
            
            actStebid = 0
            for i in task_flow:
                time.sleep(10)
                actStebid = actStebid + 1
                
                self.zcsloupt = self.zcsloupt + '开始执行steb' +'-'+ str(actStebid)+'：\n'
                if self.selected_func == exec_id:
                    self.scr.delete(1.0, END) # 使用 delete
                    self.scr.insert("insert", self.zcsloupt)
                for m in i:
                    if m.get('pre_task'):#有前置任务
                        if m.get('pre_task').get('status',1):#前置任务状态是0 就不要往下执行了，是1，该任务可以执行。#状态 0 1 的条件是，查询结果里有数据，则状态置为0，无数据，则是1.
                            tasks_todo = m.get('tasks')
                            for task in tasks_todo:
                                name = task.get('name')
                                sql = task.get('sql')
                                self.zcsloupt = self.zcsloupt +'开始核查，表：' + name +'\n'
                                if self.selected_func == exec_id:
                                    self.scr.delete(1.0, END) # 使用 delete
                                    self.scr.insert("insert", self.zcsloupt)

                                #cursor.execute (sql)#执行sql语句
                                #rows = cursor.fetchall()#读取sql结果
                                if 0:#可以得到数据，将task 状态置为0
                                    task['status'] = 0
                                    self.zcsloupt = self.zcsloupt + '表：' + name +'有数据，该支线查询结束'+'\n'
                                    if self.selected_func == exec_id:
                                        self.scr.delete(1.0, END) # 使用 delete
                                        self.scr.insert("insert", self.zcsloupt)
                                else:
                                    noDataTask.append(task)
                                    self.zcsloupt = self.zcsloupt + '表：' + name +'无数据，将尝试查询上游表是否正常'+'\n'
                                    if self.selected_func == exec_id:
                                        self.scr.delete(1.0, END) # 使用 delete
                                        self.scr.insert("insert", self.zcsloupt)
                        else:
                            tasks_todo = m.get('tasks')
                            for task in tasks_todo:
                                name = task.get('name')
                                self.zcsloupt = self.zcsloupt + '表：' + name +'下游结果表有数据，该步骤不执行'+'\n'
                                if self.selected_func == exec_id:
                                    self.scr.delete(1.0, END) # 使用 delete
                                    self.scr.insert("insert", self.zcsloupt)
                                
                        
                    else:#没有前置任务的
                        tasks_todo = m.get('tasks')
                        for task in tasks_todo:

                            name = task.get('name')
                            sql = task.get('sql')
                            self.zcsloupt = self.zcsloupt +'开始核查，表：' + name +'\n'
                            if self.selected_func == exec_id:
                                self.scr.delete(1.0, END) # 使用 delete
                                self.scr.insert("insert", self.zcsloupt)
                            #cursor.execute (sql)#执行sql语句
                            #rows = cursor.fetchall()#读取sql结果
                            if 1:#可以得到数据，将task 状态置为0
                                task['status'] = 0
                                self.zcsloupt = self.zcsloupt + '表：' + name +'有数据，该支线查询结束'+'\n'
                                if self.selected_func == exec_id:
                                    self.scr.delete(1.0, END) # 使用 delete
                                    self.scr.insert("insert", self.zcsloupt)
                            else:
                                noDataTask.append(task)
                                self.zcsloupt = self.zcsloupt + '表：' + name +'无数据，将尝试查询上游表是否正常'+'\n'
                                if self.selected_func == exec_id:
                                    self.scr.delete(1.0, END) # 使用 delete
                                    self.scr.insert("insert", self.zcsloupt)
            res_noDataTask = []
            for i in noDataTask:
                sor_name = i.get('name')
                for m in task_flow:
                    for n in m:
                        ta_name = n.get('pre_task')
                        tar_name = dict(ta_name).get('name',None)
                        #.get('name',None)
                        if sor_name == tar_name:                        
                            for task in n.get('tasks'):
                                flag = task.get('status',1)
                                if flag == 1:
                                    res_noDataTask.append(i)
                                    break

            self.zcsloupt =  self.zcsloupt + '初步诊断结果如下：' +'\n'
            if self.selected_func == exec_id:
                self.scr.delete(1.0, END) # 使用 delete
                self.scr.insert("insert", self.zcsloupt)
            if res_noDataTask:
                for i in res_noDataTask:           
                    self.zcsloupt = self.zcsloupt +'表'+  i.get('name')  +' 无数据，请核查！'+'\n'
                    if self.selected_func == exec_id:
                        self.scr.delete(1.0, END) # 使用 delete
                        self.scr.insert("insert", self.zcsloupt)
            else:
                self.zcsloupt =  self.zcsloupt +  '无明显线索，请联系L2支持！' +'\n'
                if self.selected_func == exec_id:
                    self.scr.delete(1.0, END) # 使用 delete
                    self.scr.insert("insert", self.zcsloupt)
        except Exception as e:
            messagebox.showerror('FAST-自动化运维工具-RN-2',e)
        finally:
            self.bt_sjhc['state'] = 'active'
            self.bt_sjhc['bg'] = self.dfbg
            self.execing_funcId.remove(exec_id)

    def xnlc(self,city,start_date,end_date,exec_id,DB_URI):
        try:
            self.xnlcoupt = ''
            self.execing_funcId.append(self.selected_func)
            self.bt_sjhc['state'] = 'disabled'
            self.bt_sjhc['bg'] = 'DarkGray'
            self.xnlcoupt = '我是在做测试的！'
            time.sleep(10)
            
        except Exception as e:
            messagebox.showerror('FAST-自动化运维工具-RN-2',e)
        finally:
            self.bt_sjhc['state'] = 'active'
            self.bt_sjhc['bg'] = self.dfbg
            self.execing_funcId.remove(exec_id)
            

def main():
    app = App()
    app.oracle_oupt()
    app.func_button()
    app.func_moudle()
    app.run()
    
if __name__ == '__main__':
    app = App()
    app.oracle_oupt()
    app.func_button()
    app.func_moudle()
    app.check_ossconfig()
    app.footer()
    app.run()

# app.change_select(1)

