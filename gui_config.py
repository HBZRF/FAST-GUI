import xlwt
import os
import xlrd
import tkinter
import threading
import cx_Oracle
class guiConfig:
    def oracle_test(self):
        try:
            self.conntest['bg'] = 'DarkGray'
            self.conntest['state'] = 'disabled'
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
                DB_URI = '{}/{}@{}:{}/{}'.format(self.get_user.get(),self.get_pw.get(),self.get_ip.get(),self.get_port.get(),self.get_oss.get())
                t = threading.Thread(target=self.oracle_conn_test, args=(DB_URI,))  # 创建线程
                t.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
                t.start()  # 开启线程
        except Exception as e:
            tkinter.messagebox.showerror(title='FAST-自动化运维工具-RN-2', message=e)           
        
    def oracle_conn_test(self,DB_URI):
        try:
            conn = cx_Oracle.connect(DB_URI)
            conn.close()
            tkinter.messagebox.showerror(title='FAST-自动化运维工具-RN-2', message=u'Oracle数据库可以连通！！')
        except Exception as e:
            tkinter.messagebox.showerror(title='FAST-自动化运维工具-RN-2', message=e)
        finally:
            self.conntest['bg'] = self.dfbg
            self.conntest['state'] = 'active'


    def oracle_save(self):

        oss_config_file = "./config/oss_config.xls"
        
        if os.path.exists(oss_config_file):
            os.remove(oss_config_file)
        else:
            self.safe_save('./config')
            
        wb_oss = xlwt.Workbook()
        ws_oss = wb_oss.add_sheet('OSS Oracle配置')
        biaotou = [u'Oracle配置', u'配置值']
        k = 0
        for k in range(2):
            ws_oss.write(0, k, biaotou[k])
            k = k + 1
        biaolie = [u'OSS IP地址', u'OSS 端口号', u'OSS 用户名', u'OSS 密码', u'OSS 服务名称',u'online-user',u'online-pwd']
        k = 1
        for k in range(1, 8):
            ws_oss.write(k, 0, biaolie[k - 1])
            k = k + 1
        biaolie2 = [self.get_ip.get(), self.get_port.get(), self.get_user.get(), self.get_pw.get(), self.get_oss.get(),self.usrid.get(),self.usrpwd.get()]
        k = 1
        for k in range(1, 8):
            ws_oss.write(k, 1, biaolie2[k - 1])
            k = k + 1
        wb_oss.save(oss_config_file)
        self.OMC_IP = self.get_ip.get()
        self.OMC_PORT = self.get_port.get()
        self.OMC_USER = self.get_user.get()
        self.OMC_PW = self.get_pw.get()
        self.OMC_OSS = self.get_oss.get()
        self.usr_id = self.usrid.get()
        self.usr_pwd = self.usrpwd.get()
        self.get_ip.set(self.OMC_IP)
        self.get_user.set(self.OMC_USER)
        self.get_pw.set(self.OMC_PW)
        self.get_oss.set(self.OMC_OSS)
        self.usrid.set(self.usr_id)
        self.usrpwd.set(self.usr_pwd)

        wb_oss.save(oss_config_file)
        return
    # 定义Oracle重配置函数，清除Oracle配置
    def oracle_reconfig(self):
        self.get_ip.set('')
        self.get_port.set('')
        self.get_user.set('')
        self.get_pw.set('')
        self.get_oss.set('')

    def safe_save(self,path):
        if os.path.exists(path):
            if os.path.isdir(path):
                pass
            else:
                os.remove(path)
                os.makedirs(path)
        else:
            os.makedirs(path)
                

        return
    # 定义检查Oracle配置的函数，打开软件后检查Oracle配置文件是否存在，如果存在在UI界面上显示保存值，如果不存在不显示
    def check_ossconfig(self):
        oss_config_file = "./config/oss_config.xls"
        if os.path.exists(oss_config_file):
            bk = xlrd.open_workbook(oss_config_file)
            try:
                sh = bk.sheet_by_name("OSS Oracle配置")
            except:
                return
            self.OMC_IP = sh.cell_value(1, 1)
            self.OMC_PORT = sh.cell_value(2, 1)
            self.OMC_USER = sh.cell_value(3, 1)
            self.OMC_PW = sh.cell_value(4, 1)
            self.OMC_OSS = sh.cell_value(5, 1)
            self.usr_id = sh.cell_value(6, 1)
            self.usr_pwd = sh.cell_value(7, 1)
            self.get_ip.set(self.OMC_IP)
            self.get_port.set(self.OMC_PORT)
            self.get_user.set(self.OMC_USER)
            self.get_pw.set(self.OMC_PW)
            self.get_oss.set(self.OMC_OSS)
            self.usrid.set(self.usr_id)
            self.usrpwd.set(self.usr_pwd)
        else:
            return
        return


