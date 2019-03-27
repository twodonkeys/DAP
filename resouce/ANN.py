#!/usr/bin/python3
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/6 19:41
# @Author  : Twodonkeys
# @Site    : 
# @File    : ANN.py
# @Software: PyCharm
from keras.models import Sequential
from keras.layers import Dense,Activation
model = Sequential()
model.add(Dense(32,input_dim=784))
model.add(Activation('relu'))
model.add(Dense(10))
model.add(Activation('softmax'))

