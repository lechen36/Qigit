# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 20:47:27 2019
@author: MI
macd_select_backtest
策略：macd 预测
"""
import pandas as pd
import numpy as np
import dataAnalysis as da
import kplot as kp
import matplotlib.pyplot as plt
symbols=da.symbol_list()
df_symbols_income=pd.DataFrame()

    
#for iSymbol in symbols[50:100]:
Symbollist=pd.read_pickle('Symbollist.pkl')
for iSymbol in Symbollist[:10]:

    df = da.data_read(iSymbol)
    df.loc[:,'Long']=0
    #for i in df.loc['trade_date']:
    Long_columns_index=df.columns.get_loc('Long')
    for i in range(30,len(df)):
        df_hist=df.iloc[:i,:]
        df2=df_hist[df_hist['MACDXPre']>=1]
        df2_success=df2[(df2['ROC+1']>1)|(df2['ROC+2']>1)|(df2['ROC+3']>2)] #把预测出金叉中后三天内上涨的画出来
        if len(df2)!=0:
            success_rate=len(df2_success)/len(df2)
        else:
            continue
        
        if (success_rate>0.6) & (df_hist.iloc[-1,:]['MACDXPre']>0) & (df['Long'].iloc[i-1]==0):
           # df['Long'].iloc[i]=1
            df.iat[i,Long_columns_index]=1
            
        elif df['Long'].iloc[i-1]==1: #如果昨天已经是1了
            
            if df['ROC-1'].iloc[i]>-2.0:
           #     df['Long'].iloc[i]=2
                df.iat[i,Long_columns_index]=2
                
        elif df['Long'].iloc[i-1]==2: #如果昨天已经是1了
            if df['ROC-2'].iloc[i]>-1.0:
                
            #    df['Long'].iloc[i]=3
                df.iat[i,Long_columns_index]=3
                
        elif df['Long'].iloc[i-1]==3: #如果昨天已经是1了
            if df['ROC-3'].iloc[i]>1.0:
                
             #   df['Long'].iloc[i]=4
             df.iat[i,Long_columns_index]=4
        
        elif df['Long'].iloc[i-1]==4: #如果昨天已经是1了
            if df['ROC-3'].iloc[i]>1.0:
              #  df['Long'].iloc[i]=5 
              df.iat[i,Long_columns_index]=5
                
        elif df['Long'].iloc[i-1]==5: #如果昨天已经是1了
               # df['Long'].iloc[i]=0 
                df.iat[i,Long_columns_index]=0
        else:
           # df['Long'].iloc[i]=0 
            df.iat[i,Long_columns_index]=0
            
    df['income']=0
    iClosePrice=1.0
    df['iClosePrice']=0
    for i in range(30,len(df)):
        if (df['Long'].iloc[i]==1) & (df['Long'].iloc[i-1]==0):
            iClosePrice=df['close'].iloc[i]
            
        if (df['Long'].iloc[i]>0) & (df['Long'].iloc[i-1]>0):  #如果今天和昨天买入指标都大于0
            
#            df['income'].iloc[i]=(df['close'].iloc[i]-df['close'].iloc[i-1])/iClosePrice*100 #收益率
#            df['iClosePrice'].iloc[i]=iClosePrice
            
            df.iat[i,df.columns.get_loc('income')]=(df['close'].iloc[i]-df['close'].iloc[i-1])/iClosePrice*100 #收益率
            df.iat[i,df.columns.get_loc('iClosePrice')]=iClosePrice

            
    
    df['incomeSum']=np.cumsum(df['income'].values)     
    dfnew=df.loc[:,['ts_code','trade_date','close','iClosePrice','Long','income','incomeSum']]  
    
    kp.kplot(df,'incomeSum')
    df_symbols_income=df_symbols_income.append(dfnew.iloc[-1,:])
    print(iSymbol)
    
df_symbols_income=df_symbols_income[['ts_code','incomeSum','close','trade_date']]
df_symbols_income.mean()
    
