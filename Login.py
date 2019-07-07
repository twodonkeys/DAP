#!/usr/bin/python3
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 10:55
# @Author  : Twodonkeys
# @Site    : 
# @File    : Login.py
# @Software: PyCharm

import sys
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import  QFileDialog,QMessageBox,QDockWidget,QListWidget,QLabel
from ui.LoginWindow import Ui_LoginForm
from Signup import MySignupWindow
from Main import *
import webbrowser
import ctypes
import sqlite3
import hashlib
import configparser#读取配置文件
import numpy as np
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")#本行与import ctypes使用是为了使任务栏图标与标题栏图标一致

class MyLoginWindow(QtWidgets.QMainWindow,Ui_LoginForm):
    def __init__(self):
        super(MyLoginWindow,self).__init__()
        self.setupUi(self)
        config = configparser.ConfigParser()
        config.sections()
        config.read('config/config.ini')
        self.table = config['Sqlite']['table']
        self.privateKey=config['Sqlite']['privatekey']
        self.db=config['Sqlite']['db']
        self.pushbtn_Login.clicked.connect(self.btn_login)
        self.pushbtn_Reg.clicked.connect(self.btn_signup)
        self.label_Logo.mousePressEvent
    def hash(self,src):
        """
        哈希md5加密方法
        :param src: 字符串str
        :return:
        """
        src = (src + self.privateKey).encode("utf-8")
        m = hashlib.md5()
        m.update(src)
        return m.hexdigest()

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        config = configparser.ConfigParser()
        config.sections()
        config.read('config/config.ini')
        web = config['Web']['WebHost']
        if web=="":
            return
        else:
            webbrowser.open(web)
    def btn_signup(self):
        signupWindow.show()

    def btn_login(self):
        #1 获取帐号密码
        Username = self.line_Username.text()
        Password =self.hash(self.line_Userpassword.text())
        if Username=="" or Password=="":
            QMessageBox.warning(self,
                                 "警告",
                                 "帐号密码不能为空,请输入!")
            return
        conn = sqlite3.connect("db/%s.db" % (self.db))  # 在此文件所在的文件夹打开或创建数据库文件
        c = conn.cursor()  # 设置游标
        # 创建一个含有id，name，password字段的表
        c.execute("""SELECT password FROM %s WHERE name = '%s'"""%(self.table, Username))
        print("Password:",Password)
        PasswordDb=c.fetchall()

        #2 查询数据库,判定是否有匹配项
        if not PasswordDb :
            QMessageBox.critical(self,
                                 "错误",
                                 "用户不存在!")
            self.line_Username.clear()
            self.line_Userpassword.clear()
            return
        PasswordDb = list(np.array(PasswordDb).T)[0]
        if Password == PasswordDb[0]:
            window.close()
            MyMainWindow.show()
        else:
            print(Password)
            QMessageBox.warning(self,
                                "警告",
                                "帐号密码错误,请重新输入!")
            self.line_Username.clear()
            self.line_Userpassword.clear()
            return

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)#QApplication相当于main函数，也就是整个程序（很多文件）的主入口函数。对于GUI程序必须至少有一个这样的实例来让程序运行。
    window = MyLoginWindow()
    signupWindow = MySignupWindow()
    MyMainWindow=MyMainWindow()
    window.show()
    sys.exit(app.exec_())





