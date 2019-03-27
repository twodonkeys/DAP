from sklearn.externals import joblib
import numpy as np
import pymysql
def getdata(ip,name,password,database_name,select_table):
    db = pymysql.connect(ip,name,password,database_name)
    cursor = db.cursor()
    cursor.execute(select_table)
    rows_many = cursor.fetchall()
    rows_many = np.matrix(rows_many)
    rows_many = np.float32(rows_many)
    X_value = rows_many[:, 1:, ]
    return X_value
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
#获取数据转换信号
ARR=[True,True,True,False,False,True,False,False,False,False,True,False,False,False,False,True]
ip='127.0.0.1'
#数据库数据用户名称
name='root'
#数据库密码
password='123456'
#数据库名称
database_name= 'data'
#数据库获取表
select_table="select * from testtable"
#加载训练好的模型
RF=joblib.load('rf.model')#训练模型
RF1=joblib.load('rf1.model')#Y归一化模型
RF2=joblib.load('rf2.model')#X归一化模型
#获取架子训练数据的结果最大值最小值
data_result_min=RF1.data_min_
data_result_max=RF1.data_max_
#读取数据
inputdata=getdata(ip,name,password,database_name,select_table)
inputdata=np.array(inputdata)
inputdata=datatransform(inputdata,ARR)
inputdata=np.matrix(inputdata)
#训练数据归一化
inputdata=RF2.transform(inputdata)
#模型计算
y_console=RF.predict(inputdata)
#计算结果重构（反归一化）
y_console=y_console*(data_result_max-data_result_min)+data_result_min
#打印结果
print(y_console)
