#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 16:28:23 2018

@author: mac
input:symbolData  date(日期)  open  high close low volume
output:df   date(日期)  open  high close low volume  macd ...
"""
from scipy import stats
import numpy as np
import pandas as pd
import tushare as ts 


def macd_index_cal(symbolData): 
    df=symbolData
    short_ema=df['close'].ewm(span=12).mean()
    long_ema=df['close'].ewm(span=26).mean()
    df.loc[:,'DIFF']=short_ema-long_ema
    df.loc[:,'DEA']=df['DIFF'].ewm(span=9).mean()
    df.loc[:,'MACD']=2*(df['DIFF']-df['DEA'])
    df2=df.loc[:,['close','MACD']]
    df2.loc[:,'MACDlag1']=df2['MACD'].shift(1)
    
    # MACD 
    df2.loc[:,'MACDX']=0
    df2.loc[(df2['MACD']>0) & (df2['MACDlag1']<0),'MACDX']=1
    df2.loc[(df2['MACD']<0) & (df2['MACDlag1']>0),'MACDX']=-1
    df.loc[:,'MACDX']=df2.loc[:,'MACDX']
#   df['MACDalpha']=(df['DIFF']-df['DIFF'].shift(1))-(df['DEA']-df['DEA'].shift(1))
    
    df2.loc[:,'MACDXPre']=0
    df2.loc[:,'MACDlag4']=df2.loc[:,'MACD'].shift(4)
    df2.loc[:,'MACDlag3']=df2.loc[:,'MACD'].shift(3)
    df2.loc[:,'MACDlag2']=df2.loc[:,'MACD'].shift(2)
    df2.loc[:,'MACDlag1']=df2.loc[:,'MACD'].shift(1)
    df2.loc[:,'MACDlag0']=df2.loc[:,'MACD'].shift(0)
    
    for iData in df2.index:  
        x = np.array([-4,-3,-2,-1,0])
        y = df2.loc[iData,['MACDlag4','MACDlag3','MACDlag2','MACDlag1','MACDlag0']].values
        k, b, r_value, p_value, std_err = stats.linregress(x,y) #一维线性回归，返回斜率、截距、r相关系数等
        try:
            x0=-b/k#计算为0的时刻x值 联合r值进行计算 如果5天内r值比较高，可以预测则可以计算下。
            if r_value>=0.90:
                if (x0>0) & (x0<5):
                    df2.loc[iData,'MACDXPre']=int(x0)
        except:
            pass
                
    df.loc[:,'MACDXPre']=df2.loc[:,'MACDXPre']
           
    return df

def kdj_index_cal(symbolData):
    df=symbolData
    lowList=df['low'].rolling(9).min()
    lowList.fillna(value=df['low'].expanding().min(), inplace=True)
    highList = df['high'].rolling(9).max()
    highList.fillna(value=df['high'].expanding().max(), inplace=True)
    rsv = (df.loc[:,'close'] - lowList) / (highList - lowList) * 100
    df.loc[:,'kdj_k'] = rsv.ewm(com=2).mean()
    df.loc[:,'kdj_d'] = df.loc[:,'kdj_k'].ewm(com=2).mean()
    df.loc[:,'kdj_j'] = 3.0 * df.loc[:,'kdj_k'] - 2.0 * df.loc[:,'kdj_d']
    
    
    df2=df.loc[:,['kdj_k','kdj_d']]
    df2.loc[:,'kd']=df2.loc[:,'kdj_k']-df2.loc[:,'kdj_d']
    df2.loc[:,'kdlag1']=df2.loc[:,'kd'].shift(1)
    df2.loc[:,'kdX']=0
    df2.loc[(df2.loc[:,'kd']>0) & (df2.loc[:,'kdlag1']<0),'kdX']=1
    df2.loc[(df2['kd']<0) & (df2['kdlag1']>0),'kdX']=-1
    df.loc[:,'kdX']=df2.loc[:,'kdX']
    
    df2.loc[:,'kdXPre']=0
    df2.loc[:,'kdlag4']=df2.loc[:,'kd'].shift(4)
    df2.loc[:,'kdlag3']=df2.loc[:,'kd'].shift(3)
    df2.loc[:,'kdlag2']=df2.loc[:,'kd'].shift(2)
    df2.loc[:,'kdlag1']=df2.loc[:,'kd'].shift(1)
    df2.loc[:,'kdlag0']=df2.loc[:,'kd'].shift(0)
    
    for iData in df2.index:  
        x = np.array([-4,-3,-2,-1,0])
        y = df2.loc[iData,['kdlag4','kdlag3','kdlag2','kdlag1','kdlag0']].values
        k, b, r_value, p_value, std_err = stats.linregress(x,y) #一维线性回归，返回斜率、截距、r相关系数等
        try:
            x0=-b/k#计算为0的时刻x值 联合r值进行计算 如果5天内r值比较高，可以预测则可以计算下。
            if r_value>=0.90:
                if (x0>0) & (x0<5):
                    df2.loc[iData,'kdXPre']=int(x0)
        except:
            pass
                
    df.loc[:,'kdXPre']=df2.loc[:,'kdXPre']   
    return df

def ema_index_cal(symbolData):
    df=symbolData
    df.loc[:,'ema5']=df['close'].ewm(span=5).mean()
    df.loc[:,'ema10']=df['close'].ewm(span=10).mean()
    df.loc[:,'ema20']=df['close'].ewm(span=20).mean()
    df.loc[:,'ema60']=df['close'].ewm(span=60).mean()
    return df

def rsi_index_cal(symbolData):
    for periods in [6,12,24]:
        array_list=symbolData['close'].values   
        length = len(array_list)
        rsies = [np.nan] * length
        if length <= periods:
            return rsies
        up_avg = 0
        down_avg = 0
    
        first_t = array_list[:periods + 1]
        for i in range(1, len(first_t)):
            if first_t[i] >= first_t[i - 1]:
                up_avg += first_t[i] - first_t[i - 1]
            else:
                down_avg += first_t[i - 1] - first_t[i]
        up_avg = up_avg / periods
        down_avg = down_avg / periods
        rs = up_avg / down_avg
        rsies[periods] = 100 - 100 / (1 + rs)
    
        for j in range(periods + 1, length):
            up = 0
            down = 0
            if array_list[j] >= array_list[j - 1]:
                up = array_list[j] - array_list[j - 1]
                down = 0
            else:
                up = 0
                down = array_list[j - 1] - array_list[j]
            up_avg = (up_avg * (periods - 1) + up) / periods
            down_avg = (down_avg * (periods - 1) + down) / periods
            rs = up_avg / down_avg
            rsies[j] = 100 - 100 / (1 + rs)
            symbolData.loc[:,'rsi%d'%periods]= rsies
            symbolData.fillna(0,inplace=True)
    return symbolData

def roc_index_cal(symbolData):
    df=symbolData
    df=df.sort_values('trade_date')
    for i in [1,2,3,5]:
        N = df['close'].diff(i)
        D = df['close'].shift(i)
        df.loc[:,'ROC-%d'%i]=N/D*100.0 # x% 百分比
        df.loc[:,'ROC+%d'%i]=df['ROC-%d'%i].shift(-i) #未来1天后的变化率
    return df 

def vol_index_cal(symbolData):
    df=symbolData
    df=df.sort_values('trade_date')
    df.loc[:,'mavol5']=df['vol'].rolling(5).mean()
    df.loc[:,'mavol10']=df['vol'].rolling(10).mean()
    
    df2=df.loc[:,['mavol5','mavol10']]
    df2.loc[:,'volminus']=df2.loc[:,'mavol10']-df2.loc[:,'mavol5']
    df2.loc[:,'volminuslag1']=df2.loc[:,'volminus'].shift(1)
    df2.loc[:,'volX']=0
    df2.loc[(df2.loc[:,'volminus']>0) & (df2.loc[:,'volminuslag1']<0),'volX']=1
    df.loc[:,'volX']=df2.loc[:,'volX']
    return df

if __name__== '__main__':
    import kplot as kp 
    ts.set_token('bf3b4e51fcc67507e8694e9a3f2bd591be93bea276f9d86f564fe28f')
    pro = ts.pro_api()
    df = ts.pro_bar(api=pro, ts_code='000001.SZ', adj='qfq',start_date='20180101')   
#   df = ts.pro_bar(ts_code='0A0001.SH', asset='I', start_date='20180101', end_date='20190411')
#   df = ts.get_hist_data('sh',start='2017-01-01',end='2018-03-31')
    macd_index_cal(df)
    kdj_index_cal(df)
    rsi_index_cal(df)
    vol_index_cal(df)
    kp.kplot(df,'vol')
    
    
    


