#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 00:48:02 2019

@author: zlw
"""

"""
Spyder Editor

This is a temporary script file.
"""

start_fetch_date='20180101'

import tushare as ts
import numpy as np
import indexCal as ic
start_analysis_date='20180501'
ts.set_token('bf3b4e51fcc67507e8694e9a3f2bd591be93bea276f9d86f564fe28f')
pro = ts.pro_api()

data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
data.loc[:,'ST']=np.char.rfind(data['name'].values.astype('str'),'*ST')#字符串操作，去掉ST的股份
dataSafe=data[data['ST']==-1] 
dataSafe=dataSafe[dataSafe['ts_code'].str.slice(0,3)!='300']#去掉创业板的数据
symbol_list=list(dataSafe['ts_code'])

import fix_yahoo_finance as yf
def download_data(iSymbol):
    try:
        df=yf.download(iSymbol, start="2018-01-01",auto_adjust=True)
        df.columns=['open', 'high', 'low', 'close', 'volume']
        df.loc[:,'ts_code']=iSymbol
        df.loc[:,'trade_date']=df.index.strftime('%Y%m%d').values
        df=df[['ts_code','trade_date','open','high','low','close','volume']]

        df=ic.macd_index_cal(df)
        df=ic.kdj_index_cal(df)
        df=ic.ema_index_cal(df)
        df=ic.roc_index_cal(df)
        df=df.fillna(0)
        df.to_pickle('symbol_data_yahoo/%s.pkl'%iSymbol)
        #print(df.head())
    except:
        pass
if __name__=='__main__':   
    import multiprocessing as mp
    from multiprocessing import Pool
    mp.set_start_method('spawn')

    import time
    t0 = time.time()
    symbol_list = [i.replace('.SH','.SS') for i in symbol_list]
    with Pool(8) as p:
        p.map(download_data, symbol_list[:]) #采用多进程进行并行计算

    elapsed = time.time()-t0
    msg = "{:.2f}s"
    print(msg.format(elapsed))