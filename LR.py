import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymysql
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.cross_validation import train_test_split   #交叉验证

def data_mysql():
    #链接数据库
    connection=pymysql.connect(host="127.0.0.1",port=3306,user='root',password='123456',db='data')
    #创建游标
    cursor=connection.cursor()
    #sql语句
    sql="select * from flowdata"
    cursor.execute(sql)
    a=cursor.fetchall()
    a=np.matrix(a)
    return a

def datatest_mysql():
    #链接数据库
    connection=pymysql.connect(host="127.0.0.1",port=3306,user='root',password='123456',db='data')
    #创建游标
    cursor=connection.cursor()
    #sql语句
    sql="select * from flowdata"
    cursor.execute(sql)
    b=cursor.fetchall()
    b=np.matrix(b)
    return b

def LR():
    # 训练集
    data = data_mysql()
    data = pd.DataFrame(data, dtype=np.float)

    data = np.float32(data)
    x = data[:, 0:4]
    y = data[:, -1]
    # 测试集
    datatest = datatest_mysql()
    datatest = pd.DataFrame(datatest, dtype=np.float)
    datatest = np.float32(datatest)
    x_test = datatest[:, 0:4]
    y_test = datatest[:, -1]
    #线性回归模型
    model = LinearRegression()
    model.fit(x,y)
    print(model.score(x,y))
    print(model.intercept_)      #截距
    print(model.coef_)    #权重系数
    y_pred=model.predict(x_test)
    #还原预测结果
    y_pred_true=[]
    for i in  range(0,len(y_pred)):
        y_pred_true.append(y_pred[i]*14897.523949247547+37239.07215498417)
    # =======================================================转换数据类型
    a1 = []
    b1 = []
    c1 = 0
    for i in range(len(y_pred_true)):
        a1 = y_test[i] * 0.1
        b1 = np.abs(y_test[i] - y_pred_true[i])
        if b1 <= a1:
            c1 += 1

    print(c1)
    print(len(y_pred_true))
    print("accuracy is %a" % (c1 / len(y_pred_true)))


    plt.figure() #实例化作图变量
    plt.title('dx LR')
    plt.xlabel('x')
    plt.ylabel('flow')
    # plt.axis([-5,1,50000,70000])#确定坐标范围
    plt.grid(True)#是否绘制网格线
    plt.plot(range(len(y_pred_true)),y_pred_true,'b',label='predict')
    plt.plot(range(len(y_test)),y_test,'r',label="test")
    plt.show()
    return
LR()


def more_LR():
    #训练集
    data=data_mysql()
    data=pd.DataFrame(data,dtype=np.float)

    data=np.float32(data)
    x=data[:,0:4]
    y=data[:,-1]
    #测试集
    datatest=datatest_mysql()
    datatest = pd.DataFrame(datatest, dtype=np.float)
    datatest=np.float32(datatest)
    x_test = datatest[:,0:4]
    y_test = datatest[:, -1]
    #多项式线性回归模型

    poly_reg=PolynomialFeatures(4)
    x_more=poly_reg.fit_transform(x)
    x_test_more=poly_reg.fit_transform(x_test)
    model = LinearRegression()
    model.fit(x_more,y)
    print(model.score(x_more,y))
    print(model.intercept_)      #截距
    print(model.coef_)    #权重系数
    y_pred=model.predict(x_test_more)
    #还原预测结果
    y_pred_true=[]
    for i in  range(0,len(y_pred)):
        y_pred_true.append(y_pred[i]*14897.523949247547+37239.07215498417)


    # =======================================================转换数据类型
    a1=[]
    b1=[]
    c1=0
    for i in range(len(y_pred_true)):
        a1 = y_test[i]*0.05
        b1 = np.abs(y_test[i] - y_pred_true[i])
        if b1 <= a1:
            c1 += 1

    print(c1)
    print(len(y_pred_true))
    print("accuracy is %a" % (c1 / len(y_pred_true)))


    #类型转换
    # y_pred_true=np.matrix(y_pred_true)
    # y_test=np.matrix(y_test)


    #作图
    plt.figure() #实例化作图变量
    plt.title('dx more LR')
    plt.xlabel('x')
    plt.ylabel('flow')
    # plt.axis([-5,1,50000,70000])#确定坐标范围
    plt.grid(True)#是否绘制网格线
    plt.plot(range(len(y_pred_true)),y_pred_true,'b',label='predict')
    plt.plot(range(len(y_test)),y_test,'r',label="test")
    # plt.show()
    return
# more_LR()

