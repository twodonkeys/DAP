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
    def scatter_sub(self,host, port, user, passwd, dbname, charset,autoOpen=True):
        try:
            conn = pymysql.Connection(
                host=host,
                port=port,
                user=user,
                passwd=passwd,
                db=dbname,
                charset=charset
            )
            cur = conn.cursor()
            cur.execute("select * from rflll_1;")
            # cursor对象使用MySQL查询字符串执行查询，返回一个包含多个元组的元组——每行对应一个元组
            rows = cur.fetchall()
            # print(rows)
            select_head = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s'" % ('rflll_1')
            headcursor = cur.execute(select_head)
            header = cur.fetchall()
            headerT_ = list(np.array(header).T)[0]
            headerT= (','.join(headerT_)).split(',')
            # 使用Pandas的DataFrame来处理每一行要比使用一个包含元组的元组方便
            # 下面的Python代码片段将所有行转化为DataFrame实例
            df = pd.DataFrame([[ij for ij in i] for i in rows])
            df.columns =headerT#替换列名
            trace1 = go.Scatter(x=df[(headerT[6])], y=df[headerT[2]],mode='markers')
            trace2 = go.Scatter(x=df[(headerT[6])], y=df[(headerT[3])],mode='markers')
            trace3 = go.Scatter(x=df[(headerT[6])], y=df[(headerT[4])],mode='markers')
            trace4 = go.Scatter(x=df[(headerT[6])], y=df[(headerT[5])],mode='markers')
            fig = tools.make_subplots(rows=2, cols=2, subplot_titles=('Plot 1', 'Plot 2',
                                                                      'Plot 3', 'Plot 4'))
            fig.append_trace(trace1, 1, 1)
            fig.append_trace(trace2, 1, 2)
            fig.append_trace(trace3, 2, 1)
            fig.append_trace(trace4, 2, 2)
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
