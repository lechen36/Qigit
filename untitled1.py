#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 17:04:26 2019

@author: mac
"""
# 把所有数据获取一遍，并更新数据信息，每天运行一次即可
import dataAnalysis as da
import pandas as pd
df=da.data_read('000002.SZ')

# 绘图
import kplot as kp
import dataAnalysis as da
import matplotlib.pyplot as plt 

startDate='20181201'
df1=df[df['trade_date']>startDate]

df1['mavol5']=df1['vol'].rolling(5).mean()
df1['mavol10']=df1['vol'].rolling(10).mean()
df1.to_csv('a1.csv')
fig=kp.kplot(df1,'vol')


