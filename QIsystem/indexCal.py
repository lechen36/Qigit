#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 16:28:23 2018

@author: mac
input:symbolData  date(日期)  open  high close low volume
output:df   date(日期)  open  high close low volume  macd ...
"""

def macd_index_cal(symbolData): 
    df=symbolData
    short_ema=df['close'].ewm(span=12).mean()
    long_ema=df['close'].ewm(span=26).mean()
    df['DIFF']=short_ema-long_ema
    df['DEA']=df['DIFF'].ewm(span=9).mean()
    df['MACD']=2*(df['DIFF']-df['DEA'])
    df2=df[['close','MACD']]
    df2['MACDlag1']=df2['MACD'].shift(1)
    df2['MACDX']=0
    df2.loc[(df2['MACD']>0) & (df2['MACDlag1']<0),'MACDX']=1
    df2.loc[(df2['MACD']<0) & (df2['MACDlag1']>0),'MACDX']=-1
    df['MACDX']=df2['MACDX']
#   df['MACDalpha']=(df['DIFF']-df['DIFF'].shift(1))-(df['DEA']-df['DEA'].shift(1))
    
    return df

def kdj_index_cal(symbolData):
    df=symbolData
    lowList=df['low'].rolling(9).min()
    lowList.fillna(value=df['low'].expanding().min(), inplace=True)
    highList = df['high'].rolling(9).max()
    highList.fillna(value=df['high'].expanding().max(), inplace=True)
    rsv = (df['close'] - lowList) / (highList - lowList) * 100
    df['kdj_k'] = rsv.ewm(com=2).mean()
    df['kdj_d'] = df['kdj_k'].ewm(com=2).mean()
    df['kdj_j'] = 3.0 * df['kdj_k'] - 2.0 * df['kdj_d']
    return df

def ema_index_cal(symbolData):
    df=symbolData
    df['ema5']=df['close'].ewm(span=5).mean()
    df['ema10']=df['close'].ewm(span=10).mean()
    df['ema20']=df['close'].ewm(span=20).mean()
    df['ema60']=df['close'].ewm(span=60).mean()
    return df

def rsi_index_cal(symbolData):
    pass

def roc_index_cal(symbolData):
    df=symbolData
    for i in [1,2,3,5]:
        N = df['close'].diff(i)
        D = df['close'].shift(i)
        df['ROC_%s'%str(i)]=N/D*100.0 # x% 百分比
    return df 


