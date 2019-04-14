#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 17:04:26 2019

@author: mac
"""
# 把所有数据获取一遍，并更新数据信息，每天运行一次即可
import dataAnalysis as da
df=da.data_read('000002.SZ')

# 绘图
import kplot as kp
import dataAnalysis as da
import matplotlib.pyplot as plt 

startDate='20180501'
df1=df[df['trade_date']>startDate]

fig=kp.kplot(df1,'close')


