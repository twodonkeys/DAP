import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import pymysql
from sklearn.preprocessing import MinMaxScaler
from sklearn.externals import joblib
from sklearn.preprocessing import PolynomialFeatures
from sklearn.neighbors import KNeighborsClassifier
import MyFunction

#从数据库读取训练数据
def getdata(ip,name,password,database_name,select_table):
    db = pymysql.connect(ip,name,password,database_name)
    cursor = db.cursor()
    cursor.execute(select_table)
    rows_many = cursor.fetchall()
    rows_many = np.matrix(rows_many)
    rows_many = np.float32(rows_many)
    X_value = rows_many[:, :, ]
    return X_value
#数据选择
def datatransform(inputdata,arr):#删除
    arr_x1=arr[0:1]
    arr_x2=arr[1:2]
    arr_x3=arr[2:3]
    arr_x4=arr[-1:]
    if arr_x1[0:1]==True:
        inputdata.inputdata[:,0]
    if arr_x2[1:2]==True:
        inputdata[:,1]=inputdata[:,1]
    if arr_x3[2:3] == True:
        inputdata[:,2]=inputdata[:,2]
    if arr_x4[-1:]==True:
        inputdata[:,3]=inputdata[:,3]

    return inputdata

#训练测试数据划分
def trainingdata(break_point,inputdata):
    X_train=inputdata[:break_point,:-1]
    Y_train=inputdata[:break_point,-1]
    X_test=inputdata[break_point:,:-1]
    Y_test=inputdata[break_point:,-1]
    return X_train,Y_train,X_test,Y_test

def DXSMain(MySQL,Data,SelectX=[True,True,True,True],degree=2):
    #数据IP地址
    ip=MySQL[0]
    #数据库数据用户名称
    name=MySQL[1]
    #数据库密码
    password=MySQL[2]
    #数据库名称
    database_name=MySQL[3]
    #数据库获取表
    select_table="select %s,%s,%s,%s,%s from %s"%(Data[0],Data[1],Data[2],Data[3],Data[4],MySQL[4])

    #输入数据方次信号
    # ARR=[True,True,True,True]
    inputdata=getdata(ip,name,password,database_name,select_table)
    inputdata=np.array(inputdata)
    inputdata=datatransform(inputdata,SelectX)
    list = MyFunction.BoolStr2list(SelectX, False)
    inputdata = np.delete(inputdata, list, axis=1)  # 删除复选框没有选中的变量数据
    inputdata=np.matrix(inputdata)
    #测试训练数据分割点
    break_point=int(inputdata.shape[0]*2/3)
    x_train,y_train,x_test,y_test=trainingdata(break_point,inputdata)

    #建立训练模型
    poly_reg =PolynomialFeatures(degree,interaction_only=False,include_bias=False) #控制多项式的度，决定特征自己结合的项，决定有没有1那一项
    x_train= poly_reg.fit_transform(x_train)
    x_test= poly_reg.fit_transform(x_test)
    lineargression=LinearRegression()
    rf=lineargression.fit(x_train,y_train)
    joblib.dump(rf,'model/morelinear.model')
    #原特征经过多项式特征增加后各特征的组合方式（列名）
    X_ploly_df = pd.DataFrame(x_test, columns=poly_reg.get_feature_names())
    lie = X_ploly_df.columns.values.tolist()
    #测试集测试
    outdata=lineargression.predict(x_test)

    c1 = 0
    for i in range(len(outdata)):
        a1 = y_test[i] * 0.05
        b1 = np.abs(y_test[i] - outdata[i])
        if b1 <= a1:
            c1 += 1
    #计算置信度
    score = c1 / len(outdata)
    coef = rf.coef_
    intercept = rf.intercept_
    Msg = lie
    return score,coef,intercept,Msg
if __name__ == '__main__':
    DXS=DXSMain()
    print(DXS)
