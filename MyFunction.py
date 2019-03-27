#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Project : LZL0704 
# @Time : 2018/8/12 22:37
# @Author : twodonkeys
# @Email :  liangzhilv@qq.com
# @Site : 
# @File : MyFunction.py
# @Software: PyCharm
import numpy as np
def BoolStr2list(Bstr,TorF):
    try:
        m=len(Bstr)
        if TorF==True:
            n=np.count_nonzero(Bstr)
        elif TorF==False:
            n=m-np.count_nonzero(Bstr)
        else:
            pass
        n_b=[0]*n
        x=0
        for b in range(m):
            if Bstr[b]==TorF:
                n_b[x]=b
                x+=1
        return (n_b)
    except:
        print("Error")

def DelArr(Arr, list,num):
    n = len(list)
    for i in range(n):
        m = 0
        m = (list[i] - i) * num
        for i in range(num):
            del Arr[m]
    return (Arr)