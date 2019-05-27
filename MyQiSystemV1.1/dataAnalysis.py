# -*- coding: utf-8 -*-
'''
利用tushre的接口获取数据并对各种指标进行计算。
'''
import tushare as ts 
import pandas as pd
import indexCal as ic
import numpy as np
import os
from fetchData import TFetchData,YFetchData
import multiprocessing as mp
from multiprocessing import Pool
#if mp.get_start_method()!='spawn':
#    mp.set_start_method('spawn')
    
START_ANALYSIS_DATE='2018-01-01'

def data_cal_index(symbol_list,method='yahoo',pallel=False):#把所有的数据进行分析并存储到一个文件中
    if pallel==False:#是否并行计算
        iNum=0
        for iSymbol in symbol_list:
            print(iSymbol,':',iNum)
            iNum+=1
    #        single_data_cal_index(iSymbol,method)
            try:
                single_data_cal_index(iSymbol,method)
            except:
                continue
    else:
        with Pool(4) as p:
            p.map(single_data_cal_index,symbol_list) #采用多进程进行并行计算
        
        

def single_data_cal_index(iSymbol,method='yahoo'):
    if method=='yahoo':
        df=YFetchData(iSymbol,START_ANALYSIS_DATE).data
    elif method=='tushare':
        df=TFetchData(iSymbol,START_ANALYSIS_DATE).data
    else:
        pass
    df=ic.macd_index_cal(df)
    df=ic.kdj_index_cal(df)
    df=ic.ema_index_cal(df)
    df=ic.roc_index_cal(df)
    df=df.fillna(0)
    df.to_pickle('symbol_data/%s.pkl'%df['ts_code'][0][:6])

    
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
            df=pd.read_pickle('symbol_data/%s'%symbol[:6])
        else:
            df=pd.read_pickle('symbol_data/%s.pkl'%symbol[:6])
        return df
    except:
        return 0
        
if __name__== '__main__':
    data_cal_index(['600000.SH','600004','600008','600060'],'tushare') #从tushare下载数据并计算
    df000=data_read('600000') #读取某个文件数据
    df111=symbol_list() #获取应分析过的列表

    

