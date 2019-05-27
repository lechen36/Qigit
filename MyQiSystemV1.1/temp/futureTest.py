#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 20:04:57 2019

@author: mac
"""

from concurrent import futures
import time
import tushare as ts 

start_fetch_date='20180101'
start_analysis_date='20180501'
ts.set_token('bf3b4e51fcc67507e8694e9a3f2bd591be93bea276f9d86f564fe28f')
pro = ts.pro_api()
import numpy as np

MAX_WORKERS = 5

def get_symbol_data(iSymbol):
    try:
        df = ts.pro_bar(api=pro, ts_code=iSymbol, adj='qfq',start_date=start_fetch_date)   
        df=df.sort_values('trade_date')
        df.to_pickle('symbol_data/%s.pkl'%df['ts_code'][0])
        return df
    except:
        return 0

def get_symbol_data_parallel():
    workers = min(MAX_WORKERS,5)
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    data['ST']=np.char.rfind(data['name'].values.astype('str'),'*ST')#字符串操作，去掉ST的股份
    dataSafe=data[data['ST']==-1]
    
    Symbol_list=list(dataSafe['ts_code'])
    
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(get_symbol_data, Symbol_list[:10])
        print(len(list(res)))
        return list(res)

if __name__=='__main__':
    x=list(range(1000))
    t0 = time.time()
    count = get_symbol_data_parallel()
    elapsed = time.time()-t0
    msg = "\n{}  in {:.2f}s"
    print(msg.format(count,elapsed))


    

