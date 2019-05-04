# -*- coding: utf-8 -*-
'''
利用tushre的接口获取数据并对各种指标进行计算。
'''
import tushare as ts 
import pandas as pd
import indexCal as ic
import numpy as np
import os



start_fetch_date='20180101'
start_analysis_date='20180501'
ts.set_token('bf3b4e51fcc67507e8694e9a3f2bd591be93bea276f9d86f564fe28f')
pro = ts.pro_api()

def data_check():#测试下数据是否需要重新计算
    try:
        symbol_files_list=symbol_list()
        df000=data_read(symbol_files_list[-1])
        dateLatest=df000['trade_date'][-1]
        df111 = ts.pro_bar(api=pro, ts_code=symbol_files_list[-1][:-4], adj='qfq',start_date=start_fetch_date)
        dateLatestOnline=df111['trade_date'][0]
        if dateLatest==dateLatestOnline:
            return False
        else:
            return True
    except:
        return True

def data_cal_index():#把所有的数据进行分析并存储到一个文件中
    if data_check()==True:
        data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        data['ST']=np.char.rfind(data['name'].values.astype('str'),'*ST')#字符串操作，去掉ST的股份
        dataSafe=data[data['ST']==-1] 
        iNum=0
        for iSymbol in dataSafe.loc[:,'ts_code']:
            print(iSymbol,':',iNum)
            iNum+=1
            
            try:
                single_data_cal_index(iSymbol)
            except:
                continue
        
def single_data_cal_index(iSymbol):
    df = ts.pro_bar(api=pro, ts_code=iSymbol, adj='qfq',start_date=start_fetch_date)   
    df=df.sort_values('trade_date')
    
    df=ic.macd_index_cal(df)
    df=ic.kdj_index_cal(df)
    df=ic.ema_index_cal(df)
    df=ic.roc_index_cal(df)
    df=df.fillna(0)
    startDate=start_analysis_date
    df1=df[df['trade_date']>=startDate]
    df1.to_pickle('symbol_data/%s.pkl'%df1['ts_code'][0])

    
    
    
def symbol_list():#读取分析后的股票列表 
    symbol_files_list=[]
    for ifile in os.listdir('symbol_data'):
        if ifile[-4:]=='.pkl':
            symbol_files_list.append(ifile[:-4])
    
    symbol_files_list.sort()
    return symbol_files_list

def data_read(symbol):#读取数据的方法  symbol 为000002.SZ 或者 000002.SZ.pkl
    try:
        if symbol[-4:]=='.pkl':
            df=pd.read_pickle('symbol_data/%s'%symbol)
        else:
            df=pd.read_pickle('symbol_data/%s.pkl'%symbol)
        return df
    except:
        return 0
        
if __name__== '__main__':
    data_cal_index()

    

