#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 17:04:26 2019

@author: mac

第一： 选择一个日期作为测试日，看后续3天内有没有出现上涨，看下成功率的情况。
把这些图绘制在 kplot

第二：筹码计算分析试一下
重写回测系统
"""
# 把所有数据获取一遍，并更新数据信息，每天运行一次即可
import sys
sys.path.append('../core')

import dataAnalysis as da
da.data_cal_index()
# 数据获取及分析，分析今日出现MACD金叉，金叉Pre的股票
import pandas as pd
import symbol_select as ss
select_Df_macd=ss.macd_select()
#select_Df_kdj=ss.kdj_select()

# 绘图
import kplot as kp
import dataAnalysis as da
import matplotlib.pyplot as plt 

#ResultDf=pd.read_pickle('result_data/Select_macd.pkl')
#select_Df2=select_Df[select_Df['kdX']==1]#
select_Df=select_Df_macd
if len(select_Df)!=0:
    Symbollist=select_Df.loc[:,'ts_code']
else:
    Symbollist=[]
    
for iSymbol in Symbollist:
    df=da.data_read(iSymbol)
    startDate='20180501'
    df1=df[df['trade_date']>startDate]
    #fig=kp.kplot(df1,'MACD')#绘图
    #fig=kp.kplot(df1,'KDJ')#绘图
    
    fig=kp.kplot(df1,'MACD_KDJ')
    fig.savefig('MACD_%s.png'%df1['ts_code'][0],dpi=600)

Symbollist.to_pickle('Symbollist.pkl')
