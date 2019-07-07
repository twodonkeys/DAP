#!/usr/bin/python3
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/4 15:46
# @Author  : Twodonkeys
# @Email   :liangzhilv@qq.com
# @Site    : 
# @File    : Load_linear.py
# @Software: PyCharm

import numpy as np
import pymysql
from sklearn.externals import joblib
import MyFunction
#从数据库读取训练数据

def getdata(ip,name,password,database_name,select_table):
    db = pymysql.connect(ip,name,password,database_name)
    cursor = db.cursor()
    cursor.execute(select_table)
    rows_many = cursor.fetchall()
    rows_many = np.matrix(rows_many)
    rows_many = np.float32(rows_many)
    cursor.close()
    db.close()
    X_value=rows_many[0]
    return X_value
#数据方次转换
def datatransform(inputdata,arr):
    arr_x1=arr[0:4]
    arr_x2=arr[4:8]
    arr_x3=arr[8:12]
    arr_x4=arr[12:]
    if arr_x1[0]==True:
        inputdata[:, 0]=np.sqrt(inputdata[:,0])
    if arr_x1[1]==True:
        inputdata[:,0]=inputdata[:,0]
    if arr_x1[2] == True:
        inputdata[:,0]=np.square(inputdata[:,0])
    if arr_x1[3]==True:
        inputdata[:,0]=pow(inputdata[:,0],3)
    if arr_x2[0]==True:
        inputdata[:, 1]=np.sqrt(inputdata[:,1])
    if arr_x2[1]==True:
        inputdata[:,1]=inputdata[:,1]
    if arr_x2[2] == True:
        inputdata[:,1]=np.square(inputdata[:,1])
    if arr_x2[3]==True:
        inputdata[:,1]=pow(inputdata[:,1],3)
    if arr_x3[0]==True:
        inputdata[:, 2]=np.sqrt(inputdata[:,2])
    if arr_x3[1]==True:
        inputdata[:,2]=inputdata[:,2]
    if arr_x3[2] == True:
        inputdata[:,2]=np.square(inputdata[:,2])
    if arr_x3[3]==True:
        inputdata[:,2]=pow(inputdata[:,2],3)
    if arr_x4[0]==True:
        inputdata[:, 3]=np.sqrt(inputdata[:,3])
    if arr_x4[1]==True:
        inputdata[:,3]=inputdata[:,3]
    if arr_x4[2] == True:
        inputdata[:,3]=np.square(inputdata[:,3])
    if arr_x4[3]==True:
        inputdata[:,3]=pow(inputdata[:,3],3)
    return inputdata

def Loadlinear(MySQL,Data,SelectX,ARR=[True,True,True,False,False,True,False,False,False,False,True,False,False,False,False,True]):
    print(Data)
    # 数据IP地址
    ip = MySQL[0]
    # 数据库数据用户名称
    name = MySQL[1]
    # 数据库密码
    password = MySQL[2]
    # 数据库名称
    database_name = MySQL[3]
    # 数据库表单
    table=MySQL[4]+'_tx'
    # 数据库获取表
    select_table = "select %s,%s,%s,%s,%s from %s" % (Data[0], Data[1], Data[2], Data[3], Data[4], table)
    inputdata = getdata(ip, name, password, database_name, select_table)
    inputdata = np.array(inputdata)
    inputdata = datatransform(inputdata, ARR)
    list = MyFunction.BoolStr2list(SelectX, False)
    inputdata = np.delete(inputdata, list, axis=1)  # 删除复选框没有选中的变量数据
    inputdata = inputdata[:,0:-1]
    # 加载训练好的模型
    RF = joblib.load('model/linear.model')  # 训练模型
    RF1 = joblib.load('model/linear_y.model')  # Y归一化模型
    RF2 = joblib.load('model/linear_x.model')  # X归一化模型
    # 或者用RF1.inverse_transform反归一化
    data_result_min = RF1.data_min_
    data_result_max = RF1.data_max_
    # 训练数据归一化
    inputdata = RF2.transform(inputdata)
    # 模型计算
    y_console = RF.predict(inputdata)
    # 计算结果重构（反归一化）
    # 或者用RF1.inverse_transform反归一化
    y_console = y_console * (data_result_max - data_result_min) + data_result_min
    # 打印结果
    result=y_console[0,0]
    print(result)
    y_name=Data[-1]
    print(y_name)
    excute_table=" UPDATE %s SET %s = %s" % (table,y_name,result )
    print(excute_table)
    db = pymysql.connect(ip,name,password,database_name)
    cursor = db.cursor()
    cursor.execute(excute_table)
    db.commit()
    cursor.close()
    db.close()
    return result

if __name__ == '__main__':
    Loadlinear()