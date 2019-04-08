#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 19:40:23 2019

@author: mac

选择策略，定义选择的策略并输出选择的结果df
"""

import pandas as pd
import dataAnalysis as da

def macd_select():
    ResultSymbols=list()
    ResultDf=pd.DataFrame()
    iNum=0
    for iSymbol in da.symbol_list():   
        print(iSymbol[:-4],':',iNum)
        iNum+=1        
        df = da.data_read(iSymbol)
        startDate='20180501'
        df1=df[df['trade_date']>startDate]
        #df2=df1[df1['MACDX']==1]
        df2=df1[df1['MACDXPre']>=1]
        df2_success=df2[(df2['ROC+1']>3)|(df2['ROC+2']>3)|(df2['ROC+3']>3)] #把预测出金叉中后三天内上涨的画出来
        if len(df2)!=0:
            success_rate=len(df2_success)/len(df2)
        else:
            continue
        if success_rate>0.6:
            ResultSymbols.append(iSymbol)
            if df.iloc[-1,:]['MACDXPre']>0:
                ResultDf=ResultDf.append(df.iloc[-1,:]) 
                print(iSymbol,':','--------------------OK----------------------')
                
    #ResultDf.to_pickle('result_data/Select_macd.pkl')
    return ResultDf
def kdj_select():
    ResultSymbols=list()
    ResultDf=pd.DataFrame()
    iNum=0
    for iSymbol in da.symbol_list():   
        print(iSymbol[:-4],':',iNum)
        iNum+=1        
        df = da.data_read(iSymbol)
        startDate='20180501'
        df1=df[df['trade_date']>startDate]     
        df2=df1[df1['kdX']==1] #满足金叉的数据
        df2_success=df2[(df2['ROC+1']>0)|(df2['ROC+2']>0)|(df2['ROC+3']>0)] #把预测出金叉中后三天内上涨的画出来
        if len(df2)!=0:
            success_rate=len(df2_success)/len(df2)
        else:
            continue
        if success_rate>0.6:
            ResultSymbols.append(iSymbol)
            if df.iloc[-1,:]['kdX']==1:
                ResultDf=ResultDf.append(df.iloc[-1,:]) 
                print(iSymbol,':','--------------------OK----------------------')
                
    #ResultDf.to_pickle('result_data/Select_macd.pkl')
    return ResultDf