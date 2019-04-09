#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 21:49:17 2019

@author: mac
"""
import mpl_finance
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib import ticker



def ax_kline(ax,df):
    date_tickers=df['trade_date'].values
    def format_date(x,pos=None):
    # 由于前面股票数据在 date 这个位置传入的都是int
    # 因此 x=0,1,2,...
    # date_tickers 是所有日期的字符串形式列表
        if x<0 or x>len(date_tickers)-1:
            return ''
        return date_tickers[int(x)]
    date_len=len(df)
    dateLoc=int(date_len/10+0.5)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(dateLoc))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    ax.set_ylabel('K')
    ax.grid(True)
    plt.setp(ax.get_xticklabels(), visible=False)
    mpl_finance.candlestick_ochl(
        ax=ax,
        quotes=df[['iNum', 'open', 'close', 'high', 'low']].values,
        width=0.7,
        colorup='r',
        colordown='g',
        alpha=0.7)
    ax.set_title('%s'%(df['ts_code'][0]))

def ax_kdj(ax,df):
    ax.plot(df['iNum'],df[['kdj_k', 'kdj_d', 'kdj_j']])
        # make these tick labels invisible
    ax.set_ylabel('KDJ')
    ax.grid(True)
    plt.setp(ax.get_xticklabels(), visible=True)
    
    ax.set_title('KDJ:',loc='right')


def ax_macd(ax,df):
    ax.bar(df['iNum'],df['MACD'],color='b')
    ax.plot(df['iNum'],df[['DIFF','DEA']])
    #ax.plot(df2['iNum'],df2['MACD'].values,'r*')
    # make these tick labels invisible
    ax.set_ylabel('MACD')
    #ax.set_title('MACD_%s_%0.2f'%(df['ts_code'][0],success_rate_macd))
    ax.grid(True)
    plt.setp(ax.get_xticklabels(), visible=True)
    
    df2=df[df['MACDXPre']>=1]  #选出MACD  金叉Pre
    df2_success=df2[(df2['ROC+1']>0)|(df2['ROC+2']>0)|(df2['ROC+3']>0)] #把预测出金叉中后三天内上涨的画出来
        
    if len(df2)!=0:
        success_rate_macd=len(df2_success)/len(df2)
    else:
        success_rate_macd=0
        
    ax.set_title('MACD:%0.2f'%(success_rate_macd),loc='right')
    


def kplot(df,index):
    '''
    df:  数据格式如下(实例)： 
        ts_code         000001.SZ  
        trade_date       20190329
        open                12.26
        high                12.82
        low                 12.21
        close               12.82
        pre_close           12.22
        change                0.6
        pct_chg              4.91
        vol           1.66951e+06
        amount         2.1083e+06
        DIFF          -0.00807692
        DEA           -0.00448718
        MACD          -0.00717949
        MACDX                   0
        MACDXPre                0
        kdj_k             46.7579
        kdj_d             47.4992
        kdj_j             45.2753
        kdX                     0
        kdXPre                  0
        Name: 20190329, dtype: object
    '''
    
    df=df.sort_values('trade_date')
    df['iNum']=np.arange(len(df))
    
    if index=='MACD_KDJ':
        fig=plt.figure(figsize=[12,8])
        ax1 = plt.axes([0.1,0.45,0.8,0.45])
        ax_kline(ax1,df)
        
        ax2=plt.axes([0.1,0.25,0.8,0.20],sharex=ax1)
        ax_macd(ax2,df)
        
        ax3=plt.axes([0.1,0.1,0.8,0.15],sharex=ax1)
        ax_kdj(ax3,df)
        
    if index=='MACD':
        fig=plt.figure(figsize=[12,8])
        ax1 = plt.axes([0.1,0.3,0.8,0.6])
        ax_kline(ax1,df)
        ax2=plt.axes([0.1,0.1,0.8,0.2],sharex=ax1)
        ax_macd(ax2,df)
        
    elif index=='KDJ':
        ax_kdj(ax2,df)

    elif index=='close':
        ax2.plot(df['iNum'],df[['close']])
        # make these tick labels invisible
        ax2.set_ylabel('close')
        ax2.grid(True)
        plt.setp(ax2.get_xticklabels(), visible=True)
    return fig
    

if __name__=='__main__':
    import tushare as ts
    import indexCal as ic
    ts.set_token('bf3b4e51fcc67507e8694e9a3f2bd591be93bea276f9d86f564fe28f')
    pro = ts.pro_api()
    df = ts.pro_bar(api=pro, ts_code='000001.SZ', adj='qfq',start_date='20180601')
    df=df.sort_values('trade_date')
    df['iNum']=np.arange(len(df))
    ic.macd_index_cal(df)
    ic.kdj_index_cal(df)
    df=df.sort_values('trade_date')
    df['iNum']=np.arange(len(df))
    date_tickers=df['trade_date']
    kplot(df,'MACD')
    
    
