#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Project : LZL0704
# @Time : 2018/8/8 9:39
# @Author : twodonkeys
# @Email :  liangzhilv@qq.com
# @Site :
# @File : Main.py
# @Software: PyCharm

from PyQt5 import QtCore, QtGui, QtWidgets,sip,QtWinExtras
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui.UI import Ui_Form
from ui.MainWindow import Ui_MainWindow
from ui.About1 import Ui_Dialog
from ui.Configure import Ui_ConfigForm
from scipy._lib import messagestream
from sklearn.neighbors import typedefs
from pandas._libs.tslibs import np_datetime,nattype
from pandas._libs import skiplist
import Linear
import Ridge
import MoreLinear
#import qdarkstyle#暗黑风格
import sys
import pymysql
import numpy as np
import MyFunction
import configparser#读取配置文件
import os
import logging
import time
import re
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler
#主窗口

class MyLog():
    # 日志打印格式
    log_fmt = '%(asctime)s\tFile \"%(filename)s\",line %(lineno)s\t%(levelname)s: %(message)s'
    formatter = logging.Formatter(log_fmt)
    # 创建TimedRotatingFileHandler对象
    log_file_handler = TimedRotatingFileHandler(filename="./logs/log", when="M", interval=1, backupCount=2)
    log_file_handler.suffix = "%Y-%m-%d_%H-%M.log"
    # log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log$")
    log_file_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger()
    log.addHandler(log_file_handler)
    def MyLogDebug(str):
        MyLog.log.debug(str,exc_info=True)

    def MyLogInfo(str):
        MyLog.log.info(str,exc_info=True)

    def MyLogWarning(str):
        MyLog.log.warning(str,exc_info=True)

    def MyLogError(str):

        MyLog.log.error(str, exc_info=True)

    def MyLogCritical(str):
        MyLog.log.critical(str, exc_info=True)

class MyMainWindow(QMainWindow,Ui_MainWindow):
    count = 0
    config = configparser.ConfigParser()
    config.sections()
    config.read('config/config.ini')
    host = config['Mysql']['host']
    user = config['Mysql']['user']
    password = config['Mysql']['password']
    db = config['Mysql']['db']
    table = config['Mysql']['table']
    MySQL = [host, user, password, db, table]
    def __init__(self):
        MyLog.MyLogInfo("Open MainWindow")
        super(MyMainWindow,self).__init__()
        self.setupUi(self)
        self.center()
        #self.changeStyle() #改变界面风格为fusion
        # self.setWindowIcon((QIcon('resouce\\ico.ico')))
        self.action_8.triggered.connect(self.windowaction)
        self.action_6.triggered.connect(self.action_View_Til)
        self.action_7.triggered.connect(self.action_View_cas)
        self.actionabout.triggered.connect(self.action_About)
        self.action_2.triggered.connect(self.action_Config)
        self.action.triggered.connect(self.close)
        self.ConfigWin=ConfigWindow(self.MySQL)
        self.ConfigWin.ConfigChanged.connect(self.setConfig)
        self.ConfigWin.DataChanged.connect(self.setData)
    def windowaction(self):
        try:
            self.count = self.count + 1
            sub = QMdiSubWindow()
            sub.setWidget(MyWindow(self.MySQL,self.Data))
            str1="新建在线分析模块" + str(self.count)
            MyLog.MyLogInfo("New"+str1)
            self.statusBar().showMessage(str1)
            sub.setWindowTitle(str1)
            self.mdiArea.addSubWindow(sub)
            sub.show()
        except Exception as e:
            QMessageBox.critical(self,
                                 'Error',
                                 str(e))
            MyLog.MyLogError(e)

    def action_View_cas(self):
        self.mdiArea.cascadeSubWindows()

    def action_View_Til(self):
        self.mdiArea.tileSubWindows()

    def action_About(self):
        # sub = QMdiSubWindow()
        # sub.setWidget(AboutWindow())
        # self.mdiArea.addSubWindow(sub)
        # sub.show()
        aboutDialog = AboutDialog()
        aboutDialog.exec_()
    def action_Config(self):
        self.ConfigWin.show()

    def closeEvent(self,Event):
        reply=QMessageBox.question(self,
                                   'RASO',
                                   "确定要退出RASO系统吗？",
                                   QMessageBox.Yes|QMessageBox.No,
                                   QMessageBox.No)
        if reply==QMessageBox.Yes:
            MyLog.MyLogInfo("RASO is closing")
            Event.accept()
        else:
            Event.ignore()
            MyLog.MyLogInfo("Cancel RASO close")
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
        (screen.height() - size.height()) / 2)

    def changeStyle(self,styleName='Fusion'):
        QApplication.setStyle(QStyleFactory.create(styleName))
        MyLog.MyLogInfo("Change style Fusion")
    def setConfig(self,list):
        self.MySQL = list

    def setData(self,list):
        self.Data=list

#关于窗口
class AboutWindow(QtWidgets.QWidget,Ui_Dialog):
    def __init__(self):
        MyLog.MyLogInfo("Open AboutWindow")
        super(AboutWindow,self).__init__()
        self.setupUi(self)
        # self.setWindowIcon((QIcon('resouce\\ico.ico')))
        # self.label.setPixmap((QPixmap('resouce\\logo.png')))

#关于对话框
class AboutDialog(QDialog,Ui_Dialog):
    def __init__(self):
        MyLog.MyLogInfo("Open AboutDialog")
        super(AboutDialog,self).__init__()
        self.setupUi(self)
        # self.setWindowIcon((QIcon('resouce\\ico.ico')))
        # self.label.setPixmap((QPixmap('resouce\\logo.png')))

#配置窗口
class ConfigWindow(QtWidgets.QWidget,Ui_ConfigForm):
    ConfigChanged=pyqtSignal(list)
    DataChanged=pyqtSignal(list)
    def __init__(self,MySQL):
        MyLog.MyLogInfo("Open ConfigWindow")
        super(ConfigWindow,self).__init__()
        self.setupUi(self)
        self.MySQL = MySQL
        try:
            self.ini_MySQL()
            self.MySQLOK_pushButton.clicked.connect(self.change_MySQL)
            self.MySQLSAVE_pushButton.clicked.connect(self.save_MySQL)
            self.MySQLLOAD_pushButton.clicked.connect(self.load_MySQL)
            self.VarApply_pushButton.clicked.connect(self.apply_Btn)
            self.VarOK_pushButton.clicked.connect(self.ok_Btn)
            self.TableRe_Btn.clicked.connect(self.tableRe_btn)
            self.TableOK_Btn.clicked.connect(self.tableOK_btn)
        except Exception as e:
            QMessageBox.critical(self,
                                 'Error',
                                 str(e))
            MyLog.MyLogError(e)

    def ini_MySQL(self):
        self.IP_lineEdit.setText(self.MySQL[0])
        self.User_lineEdit.setText(self.MySQL[1])
        self.Password_lineEdit.setText(self.MySQL[2])
        self.DataBase_lineEdit.setText(self.MySQL[3])
        self.Table_lineEdit.setText(self.MySQL[4])
    def change_MySQL(self):
        MyLog.MyLogInfo("Perform database operations")
        IP=self.IP_lineEdit.text()
        User=self.User_lineEdit.text()
        Password=self.Password_lineEdit.text()
        DataBase=self.DataBase_lineEdit.text()
        Table=self.Table_lineEdit.text()
        if IP=='...':
            QMessageBox.warning(self,
                                'Warning',
                                'Please Enter your IP address!'
                                )
        elif User=='':
            QMessageBox.warning(self,
                                'Warning',
                                'Please Enter your User name!')
        elif Password=='':
            QMessageBox.warning(self,
                                'Warning',
                                'Please Enter your Password!')
        elif DataBase=='':
            QMessageBox.warning(self,
                                'Warning',
                                'Please Enter your DataBase!')
        elif Table=='':
            QMessageBox.warning(self,
                                'Warning',
                                'Please Enter your Tabel!')
        else:
            self.MySQL=[IP,User,Password,DataBase,Table]

        try:
            db = pymysql.connect(IP, User, Password, DataBase)
            cursor = db.cursor()
            select_head = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s'" % (Table)
            select_table = "select * from %s order by id desc limit 100" % (Table)
            headcursor = cursor.execute(select_head)
            header = cursor.fetchall()
            headerT_ = list(np.array(header).T)[0]
            headerT = (','.join(headerT_)).split(',')
            tablecursor = cursor.execute(select_table)
            table = cursor.fetchall()
            self.Table_tableWidget.clear()
            rowcount = self.Table_tableWidget.rowCount()
            self.Table_tableWidget.setRowCount(rowcount + 100)
            rown = 0
            for row in table:
                for col in range(len(row)):
                    newItem = QTableWidgetItem(str(row[col]))
                    self.Table_tableWidget.setItem(rown, col, newItem)
                rown += 1
            self.Table_tableWidget.setHorizontalHeaderLabels(headerT)
            self.Config_tabWidget.setCurrentIndex(1)
            self.X1_comboBox.clear()
            self.X2_comboBox.clear()
            self.X3_comboBox.clear()
            self.X4_comboBox.clear()
            self.Y_comboBox.clear()
            self.X1_comboBox.addItems(headerT)
            self.X2_comboBox.addItems(headerT)
            self.X3_comboBox.addItems(headerT)
            self.X4_comboBox.addItems(headerT)
            self.Y_comboBox.addItems(headerT)
            if len(headerT) >= 5:
                self.X1_comboBox.setCurrentIndex(1)
                self.X2_comboBox.setCurrentIndex(2)
                self.X3_comboBox.setCurrentIndex(3)
                self.X4_comboBox.setCurrentIndex(4)
                self.Y_comboBox.setCurrentIndex(5)
            else:
                pass
        except Exception as e:

            QMessageBox.critical(self,
                                 'Error',
                                 str(e))
            MyLog.MyLogError(e)

        self.ConfigChanged.emit(self.MySQL)
    def save_MySQL(self):
        try:
            MyLog.MyLogInfo("Save MySQL config")
            IP=self.IP_lineEdit.text()
            User=self.User_lineEdit.text()
            Password=self.Password_lineEdit.text()
            DataBase=self.DataBase_lineEdit.text()
            Table=self.Table_lineEdit.text()
            fileName,fileType  = QFileDialog.getSaveFileName(self,
                                                         "文件保存",
                                                         "./config/",
                                                         "ini Files (*.ini);;ini Files (*.ini)")

            if fileName=='':
                return
            filepath=os.path.abspath('.')
            filepath=os.path.join(filepath,"config\config.ini")#注意第二个参数的起始字符不能为斜杠
            filepath = filepath.replace('\\', '/')
            if fileName == filepath:
                QMessageBox.critical(self,
                                     "Save error",
                                     "Can't replace system config file!")
                return
            config = configparser.ConfigParser()
            config['Mysql'] = {'host': IP,
                               'user': User,
                               'password': Password,
                               'db': DataBase,
                               'table': Table}
            with open(fileName, 'w') as configfile:
                config.write(configfile)
        except Exception as e:
            QMessageBox.critical(self,
                                 'Error',
                                 str(e))
            MyLog.MyLogError(e)

    def load_MySQL(self):
        try:
            MyLog.MyLogInfo("Load MySQL config")
            fileName, fileType = QFileDialog.getOpenFileName(self,
                                                             "选择文件",
                                                             "./config/",
                                                             "All Files (*);; Ini Files(*.ini)")
            config = configparser.ConfigParser()
            config.sections()
            config.read(fileName)
            config.sections()
            host = config['Mysql']['host']
            user = config['Mysql']['user']
            password = config['Mysql']['password']
            db = config['Mysql']['db']
            table = config['Mysql']['table']
            self.IP_lineEdit.setText(host)
            self.User_lineEdit.setText(user)
            self.Password_lineEdit.setText(password)
            self.DataBase_lineEdit.setText(db)
            self.Table_lineEdit.setText(table)
        except Exception as e:
            QMessageBox.critical(self,
                                 'Error',
                                 str(e))
            MyLog.MyLogError(e)

    def apply_Btn(self):
        X1 = self.X1_comboBox.currentText()
        X2 = self.X2_comboBox.currentText()
        X3 = self.X3_comboBox.currentText()
        X4 = self.X4_comboBox.currentText()
        Y = self.Y_comboBox.currentText()
        self.Data = [X1, X2, X3, X4, Y]
        self.DataChanged.emit(self.Data)

    def ok_Btn(self):
        try:
            self.apply_Btn()
        except Exception as e:
            QMessageBox.critical(self,
                                 'Error',
                                 str(e))
            MyLog.MyLogError(e)
        self.close()
    def tableRe_btn(self):
        self.load_MySQL()
    def tableOK_btn(self):
        self.Config_tabWidget.setCurrentIndex(2)

#在线分析子窗口
class MyWindow(QtWidgets.QWidget,Ui_Form):
    def __init__(self,MySQL,Data):
        try:
            MyLog.MyLogInfo("Create on-line analysis Window")
            super(MyWindow,self).__init__()
            self.setupUi(self)
            # self.setWindowIcon((QIcon('resouce\\ico.ico')))
            self.pushButton.clicked.connect(self.Work)
            self.comboBox.currentTextChanged.connect(self.ComBoxChge)
            self.MySQL=MySQL
            self.Data=Data
        except Exception as e:
            QMessageBox.critical(self,
                                 'Error',
                                 str(e))
            MyLog.MyLogError(e)

    def ComBoxChge(self):
        A=self.comboBox.currentIndex()
        switch={
            0:("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#ffffff;\"><span style=\" font-family:\'宋体\'; font-size:12pt; font-weight:600; color:#000000;\">多元线性回归</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#ffffff;\"><span style=\" font-family:\'宋体\'; font-weight:600; color:#000080;\"><br /></span><span style=\" font-family:\'宋体\'; font-weight:600; color:#000000;\">    简介：</span><span style=\" font-family:\'宋体\'; color:#000000;\">线性回归是利用数理统计中回归分析，来确定两种或两种以上变量间相互依赖的定量关系的一种统计分析方法。其表达形式为y = w\'x+e，e为误差服从均值为0的正态分布。<br />    </span><span style=\" font-family:\'宋体\'; font-weight:600; color:#000000;\">优点：</span><span style=\" font-family:\'宋体\'; color:#000000;\">线性回归的理解与解释都十分直观，并且还能通过正则化来降低过拟合的风险。另外，线性模型很容易使用随机梯度下降和新数据更新模型权重。<br />    </span><span style=\" font-family:\'宋体\'; font-weight:600; color:#000000;\">缺点：</span><span style=\" font-family:\'宋体\'; color:#000000;\">线性回归在变量是非线性关系的时候表现很差。并且其也不够灵活以捕捉更复杂的模式，添加正确的交互项或使用多项式很困难并需要大量时间。<br />    </span><span style=\" font-family:\'宋体\'; font-weight:600; color:#000000;\">适用：</span><span style=\" font-family:\'宋体\'; color:#000000;\">线性回归算法主要适用于线性模型。</span></p></body></html>"),
            1:"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#ffffff;\"><span style=\" font-family:\'宋体\'; font-size:12pt; font-weight:600; color:#000000;\">岭回归</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#ffffff;\"><span style=\" font-family:\'宋体\'; font-weight:600; color:#000080;\"><br /></span><span style=\" font-family:\'宋体\'; font-weight:600; color:#000000;\">    简介：</span><span style=\" font-family:\'宋体\'; color:#000000;\">岭回归(英文名：ridge regression, Tikhonov regularization)是一种专用于共线性数据分析的有偏估计回归方法，实质上是一种改良的最小二乘估计法，通过放弃最小二乘法的无偏性，以损失部分信息、降低精度为代价获得回归系数更为符合实际、更可靠的回归方法，对病态数据的拟合要强于最小二乘法。<span style=\" font-family:\'宋体\'; color:#000000;\"><br />    </span><span style=\" font-family:\'宋体\'; font-weight:600; color:#000000;\">优点：</span><span style=\" font-family:\'宋体\'; color:#000000;\">通过放弃最小二乘法的无偏性，以损失部分信息、降低精度为代价获得回归系数更为符合实际、更可靠的回归方法，对病态数据的拟合要强于最小二乘法。<br />    </span><span style=\" font-family:\'宋体\'; font-weight:600; color:#000000;\">缺点：</span><span style=\" font-family:\'宋体\'; color:#000000;\">没有特征选择功能。<br />    </span><span style=\" font-family:\'宋体\'; font-weight:600; color:#000000;\">适用：</span><span style=\" font-family:\'宋体\'; color:#000000;\">主要适用于线性模型。</span></p></body></html>",
            2:"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#ffffff;\"><span style=\" font-family:\'宋体\'; font-size:12pt; font-weight:600; color:#000000;\">多项式回归</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">简介：</span>多项式回归是一种原理上可以无限逼近任意曲线的一种回归方式。</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">优点：</span>无限逼近方程，常用于单个变量之间的关系。</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">缺点：</span>容易过拟合。</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">适用：</span>单个变量关系时更有作用，容易过拟合。(注：多项式回归请选择变量时，选择多选框变量。)</p></body></html>"
                }
        self.textEdit.setText(switch[A])

    def Work(self):
        self.thread=MyThread(self)
        self.thread.update_text_singal.connect(self.update_text)
        self.thread.start()

    def update_text(self,text):
        self.textEdit_2.append(text)

#传参线程
class MyThread(QtCore.QThread):

    update_text_singal=QtCore.pyqtSignal(str)

    def __init__(self,parent=None):
        super(MyThread,self).__init__(parent)
        self.parent=parent#把父窗口所有控件传递过来，要不然下面无法直接调用父窗口控件。
    def run(self):
        mywindow = self.parent
        CheckBoxValue = [0] * 16  # CheckBox值
        ComboxValue = mywindow.comboBox.currentIndex()  # 使用算法
        Combox2Value = mywindow.comboBox_2.currentText()  # 参数1
        Combox3Value = mywindow.comboBox_3.currentText()  # 参数2
        CheckBoxValue[0] = mywindow.radioButton.isChecked()
        CheckBoxValue[1] = mywindow.radioButton_2.isChecked()
        CheckBoxValue[2] = mywindow.radioButton_3.isChecked()
        CheckBoxValue[3] = mywindow.radioButton_4.isChecked()
        CheckBoxValue[4] = mywindow.radioButton_5.isChecked()
        CheckBoxValue[5] = mywindow.radioButton_6.isChecked()
        CheckBoxValue[6] = mywindow.radioButton_7.isChecked()
        CheckBoxValue[7] = mywindow.radioButton_8.isChecked()
        CheckBoxValue[8] = mywindow.radioButton_9.isChecked()
        CheckBoxValue[9] = mywindow.radioButton_10.isChecked()
        CheckBoxValue[10] = mywindow.radioButton_11.isChecked()
        CheckBoxValue[11] = mywindow.radioButton_12.isChecked()
        CheckBoxValue[12] = mywindow.radioButton_13.isChecked()
        CheckBoxValue[13] = mywindow.radioButton_14.isChecked()
        CheckBoxValue[14] = mywindow.radioButton_15.isChecked()
        CheckBoxValue[15] = mywindow.radioButton_16.isChecked()

        switch={
                0: 'X1^0.5,',
                1: 'X1,',
                2: 'X1^2,',
                3: 'X1^3,',
                4: 'X2^0.5,',
                5: 'X2,',
                6: 'X2^2,',
                7: 'X2^3,',
                8: 'X3^0.5,',
                9: 'X3,',
                10: 'X3^2,',
                11: 'X3^3,',
                12: 'X4^0.5,',
                13: 'X4,',
                14: 'X4^2,',
                15: 'X4^3,'
        }
        ARR = [0] * 4
        ARR[0] = mywindow.checkBox.isChecked()
        ARR[1] = mywindow.checkBox_2.isChecked()
        ARR[2] = mywindow.checkBox_3.isChecked()
        ARR[3] = mywindow.checkBox_4.isChecked()
        SelectX=ARR
        CheckBoxValue_=CheckBoxValue
        for i in range(4):
            if SelectX[i]==False:
                CheckBoxValue_[i*4]=False
                CheckBoxValue_[i * 4+1] = False
                CheckBoxValue_[i * 4+2] = False
                CheckBoxValue_[i * 4+3] = False
        try:
            str1=''

            n=0
            for x in list(range(0,16)):
                if CheckBoxValue[x]==True :
                    str1+=switch[x]
            strX=str1.split(",")
            del strX[-1]
            if ComboxValue==0:
                Modelreturn=Linear.LinearMain(mywindow.MySQL,mywindow.Data,SelectX,CheckBoxValue)
                score=Modelreturn[0]
                coef=Modelreturn[1]
                intercept=Modelreturn[2]
                x_Max=Modelreturn[3]
                x_Min=Modelreturn[4]
                y_Max=Modelreturn[5]
                y_Min=Modelreturn[6]
                equation="输入x数据均需归一化：x'=(x-x_Min)/(x_Max-x_Min),输出y需反归一化处理：y=y'*(y_Max-y_Min)+y_Min"
                self.str="<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"\
    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"\
    "p, li { white-space: pre-wrap; }\n"\
    "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n" \
                    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">\n\n\n" \
                    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">---拟合公式说明:---</span>%s；</p>\n" \
                    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">---训练数据变量为:---</span>%s；</p>\n" \
                    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">---测试参数与预测参数偏差小于百分之五的数据比重为</span>:<span style=\" font-weight:600;\">---</span>%s；</p>\n"\
    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">---模型系数为：---</span>%s</p>\n"\
    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">---模型截距为：---</span>%s；</p>\n"\
    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">---归一化模型X最大值为：---</span>%s；</p>\n"\
    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">---归一化模型X最小值为：---</span>%s；</p>\n"\
    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">---归一化模型Y最大值为：---</span>%s；</p>\n"\
    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">---归一化模型Y最小值为：---</span>%s；</p></body></html>" %(equation,str1,score,coef,intercept,x_Max,x_Min,y_Max,y_Min)

            if ComboxValue==1:
                Modelreturn = Ridge.RidgeMain(mywindow.MySQL,mywindow.Data,SelectX,CheckBoxValue)
                score = Modelreturn[0]
                coef = Modelreturn[1]
                coef_t=tuple(coef[0])
                intercept = Modelreturn[2]
                equation = "Y = "
                for x,a in zip(strX,coef_t):
                    equation =equation+str(a)+" * "+str(x)+" + "
                equation+=str(intercept[0])
                self.str = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n" \
                      "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n" \
                      "p, li { white-space: pre-wrap; }\n" \
                      "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n" \
                      "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">\n\n\n" \
                      "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">---拟合公式说明:---</span>%s；</p>\n" \
                      "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">---训练数据变量为:---</span>%s；</p>\n" \
                      "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">---测试参数与预测参数偏差小于百分之五的数据比重为</span>:<span style=\" font-weight:600;\">---</span>%s；</p>\n" \
                      "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">---模型系数为：---</span>%s</p>\n" \
                      "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">---模型截距为：---</span>%s；</p>\n"  % (equation,str1, score, coef, intercept)

            if ComboxValue==2:
                Modelreturn = MoreLinear.DXSMain(mywindow.MySQL,mywindow.Data,SelectX,2)
                score = Modelreturn[0]
                coef = Modelreturn[1]
                intercept = Modelreturn[2]
                Msg=Modelreturn[3]

                self.str = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n" \
                      "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n" \
                      "p, li { white-space: pre-wrap; }\n" \
                      "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n" \
                      "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">\n\n\n" \
                      "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">---训练数据变量为:---</span>%s；</p>\n" \
                      "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">---测试参数与预测参数偏差小于百分之五的数据比重为</span>:<span style=\" font-weight:600;\">---</span>%s；</p>\n" \
                      "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">---模型系数为：---</span>%s</p>\n" \
                      "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    <span style=\" font-weight:600;\">---模型截距为：---</span>%s；</p>\n"  % (Msg, score, coef, intercept)
            mywindow.textEdit_2.append(self.str)
        except Exception as e:
            QMessageBox.critical(self,
                                 'Error',
                                 str(e))
            MyLog.MyLogError(e)

#主程序
if __name__ == '__main__':
    #app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())#设置暗黑风格，需要去掉标题栏，标题栏自己设置
    app = QtWidgets.QApplication(sys.argv)  # 实例化QApplication
    MyMainWindow = MyMainWindow()
    MyMainWindow.show()
    #mywindow=mywindow()
    #mywindow.show()
    sys.exit(app.exec_())