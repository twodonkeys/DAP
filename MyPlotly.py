#!/usr/bin/python3
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/3 23:01
# @Author  : Twodonkeys
# @Email   :liangzhilv@qq.com
# @Site    : 
# @File    : MyPlotly.py
# @Software: PyCharm
import pymysql
import pandas as pd
import plotly
import plotly.graph_objs as go
import numpy as np
import os
from plotly import tools

class MyPlotly():
    def __init__(self):
        plotly_dir = 'html'
        if not os.path.isdir(plotly_dir):
            os.mkdir(plotly_dir)
        self.path_dir_plotly_html = os.getcwd() + os.sep + plotly_dir
    def get_plotly_path(self,filename='plotly_sub.html'):
        path_plotly = self.path_dir_plotly_html + os.sep + filename
        return path_plotly
    def scatter_sub(self,mysql, name,charset,autoOpen=True):
        try:
            conn = pymysql.Connection(
                host=mysql[0],
                user=mysql[1],
                passwd=mysql[2],
                db=mysql[3],
                charset=charset
            )

            table = mysql[4]
            print(table)
            print(name)
            cur = conn.cursor()
            print("select %s,%s,%s,%s,%s from %s;"%(name[0],name[1],name[2],name[3],name[4],table))
            cur.execute("select %s,%s,%s,%s,%s from %s;"%(name[0],name[1],name[2],name[3],name[4],table))
            # cursor对象使用MySQL查询字符串执行查询，返回一个包含多个元组的元组——每行对应一个元组
            rows = cur.fetchall()
            # print(rows)
            #select_head = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s'" % (table)
            #headcursor = cur.execute(select_head)
            #header = cur.fetchall()
            #headerT_ = list(np.array(header).T)[0]
            #headerT= (','.join(headerT_)).split(',')
            headerT=name
            # 使用Pandas的DataFrame来处理每一行要比使用一个包含元组的元组方便
            # 下面的Python代码片段将所有行转化为DataFrame实例
            df=pd.DataFrame([[ij for ij in i] for i in rows])
            df.columns =headerT#替换列名
            trace1 = go.Scatter(x=df[(headerT[0])], y=df[headerT[4]],mode='markers',name="图1:"+headerT[0])
            trace2 = go.Scatter(x=df[(headerT[1])], y=df[(headerT[4])],mode='markers',name="图2:"+headerT[1])
            trace3 = go.Scatter(x=df[(headerT[2])], y=df[(headerT[4])],mode='markers',name="图3:"+headerT[2])
            trace4 = go.Scatter(x=df[(headerT[3])], y=df[(headerT[4])],mode='markers',name="图4:"+headerT[3])
            figname1="%s与%s关系图"%(headerT[0],headerT[4])
            figname2 = "%s与%s关系图" % (headerT[1], headerT[4])
            figname3 = "%s与%s关系图" % (headerT[2], headerT[4])
            figname4 = "%s与%s关系图" % (headerT[3], headerT[4])
            fig = tools.make_subplots(rows=2, cols=2, subplot_titles=(figname1, figname2,
                                                                      figname3, figname4))
            fig.append_trace(trace1, 1, 1)
            fig.append_trace(trace2, 1, 2)
            fig.append_trace(trace3, 2, 1)
            fig.append_trace(trace4, 2, 2)

            fig['layout']['xaxis1'].update(title=str(headerT[0]))
            fig['layout']['xaxis2'].update(title=str(headerT[1]))
            fig['layout']['xaxis3'].update(title=str(headerT[2]))
            fig['layout']['xaxis4'].update(title=str(headerT[3]))

            # fig['layout']['yaxis1'].update(title=str(headerT[4]))
            # fig['layout']['yaxis2'].update(title=str(headerT[4]))
            # fig['layout']['yaxis3'].update(title=str(headerT[4]))
            # fig['layout']['yaxis4'].update(title=str(headerT[4]))

            fig['layout'].update(height=600, width=600, title='Ｘ－Ｙ' +
                                                              ' 变量关系图')
            output_path=self.get_plotly_path()
            plotly.offline.plot(fig,filename=output_path,auto_open=autoOpen)
        finally:
            if conn:
                conn.close()

if __name__ == '__main__':
    myplot=MyPlotly()
    myplot.scatter_sub("localhost", 3306, "root", "123456", "rfl", "utf8",True)
