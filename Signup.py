#!/usr/bin/python3
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/28 15:06
# @Author  : Twodonkeys
# @Site    : 
# @File    : Signup.py
# @Software: PyCharm

from PyQt5 import QtGui,QtWidgets,QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import  QFileDialog,QMessageBox,QDockWidget,QListWidget,QLabel
from ui.SignupWindow import Ui_SignupWindow
import webbrowser
import sys
import sqlite3
import ctypes
import configparser#读取配置文件
import re
import hashlib
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")#本行与import ctypes使用是为了使任务栏图标与标题栏图标一致

class MySignupWindow(QtWidgets.QMainWindow,Ui_SignupWindow):
    def __init__(self):
        super(MySignupWindow,self).__init__()
        self.setupUi(self)
        self.username = self.lineEdit_User.text()
        self.password=self.lineEdit_Password.text()
        self.password2=self.lineEdit_Password2.text()
        config = configparser.ConfigParser()
        config.sections()
        config.read('config/config.ini')
        self.db = config['Sqlite']['db']
        self.table = config['Sqlite']['table']
        self.privateKey=config['Sqlite']['privatekey']
        self.signupEn=config['Sqlite']['signupEn']
        self.dbconfig()
        self.Btn_SignUp.clicked.connect(self.SignUp)

    def dbconfig(self):
        conn = sqlite3.connect("db/%s.db"%(self.db))  # 在此文件所在的文件夹打开或创建数据库文件
        c = conn.cursor()  # 设置游标
        # 创建一个含有id，name，password字段的表
        try:
            c.execute('''CREATE TABLE %s
                  (id INTEGER PRIMARY KEY AUTOINCREMENT , 
                   name TEXT NOT NULL , 
                   password TEXT NOT NULL,
                   signupTime TIMESTAMP default CURRENT_TIMESTAMP)'''%(self.table))
            conn.commit()  # python连接数据库默认开启事务，所以需先提交
        except Exception as e:
            pass
        conn.close()  # 关闭连接

    def SignUp(self):
        if self.signupEn!='True':
            QMessageBox.information(self,
                                    "抱歉",
                                    "不允许注册,请联系管理员获取权限!")
            return
        self.username = self.lineEdit_User.text()
        self.password=self.lineEdit_Password.text()
        self.password2=self.lineEdit_Password2.text()
        if self.username=="":
            QMessageBox.warning(self,
                                "警告",
                                "帐户不能为空!")
            return
        if len(self.username)>=16:
            QMessageBox.warning(self,
                                "警告",
                                "用户名字符长度不能超过16个字节!")
            return
        if len(self.username)<=3:
            QMessageBox.warning(self,
                                "警告",
                                "用户名字符长度不能低于3个字节!")
            return
        if self.password=="":
            QMessageBox.warning(self,
                                "警告",
                                "密码不能为空!")
            return
        if len(self.password)<6:
            QMessageBox.warning(self,
                                "警告",
                                "密码长度不能低于6个字节!")
            return
        if len(self.password) >12:
            QMessageBox.warning(self,
                                "警告",
                                "密码长度不能高于12个字节!")
            return

        if self.Verify(self.username,self.password)==False:
            QMessageBox.warning(self,
                                "警告",
                                "帐户名或密码输入字符不符合要求")
            self.lineEdit_Password.clear()
            self.lineEdit_Password2.clear()
            return

        if self.password != self.password2:
            QMessageBox.critical(self,
                                 "错误",
                                 "第二次输入密码不一致!")
            self.lineEdit_Password.clear()
            self.lineEdit_Password2.clear()
            return
        conn = sqlite3.connect("db/%s.db" % (self.db))  # 在此文件所在的文件夹打开或创建数据库文件
        c = conn.cursor()  # 设置游标
        # 创建一个含有id，name，password字段的表
        c.execute("""SELECT password FROM %s WHERE name = '%s'""" %(self.table,self.username))

        if not c.fetchall():
            self.password = self.hash(self.password)
            c.execute("""INSERT INTO %s(name,password) VALUES ('%s','%s')"""%(self.table,self.username,self.password))
            conn.commit()
            conn.close()  # 关闭连接
            self.lineEdit_Password.clear()
            self.lineEdit_Password2.clear()
            QMessageBox.information(self,
                                    "恭喜",
                                    "注册成功!")
            return
        else:
            conn.close()  # 关闭连接
            self.lineEdit_Password.clear()
            self.lineEdit_Password2.clear()
            self.lineEdit_User.clear()
            QMessageBox.information(self,
                                    "抱歉!",
                                    "用户名已存在!")
            return


    def hash(self,src):
        """
        哈希md5加密方法
        :param src: 字符串str
        :return:
        """
        src = (src+self.privateKey).encode("utf-8")
        m = hashlib.md5()
        m.update(src)
        return m.hexdigest()
    @staticmethod
    def Verify(name, password):
        #"判断用户名密码是否合法！"
        result_name = re.compile(r"^[0-9a-zA-Z_]{1,}$")
        result_password = re.compile(r"^[0-9a-zA-Z_]{1,}$")
        if result_name.match(name) and result_password.match(password):
            return True
        else:
            return False

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MySignupWindow()
    window.show()
    sys.exit(app.exec_())
