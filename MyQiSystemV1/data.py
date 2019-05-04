#!/usr/bin/python
# -*- coding: utf-8 -*-

# data.py

from __future__ import print_function
from abc import ABCMeta, abstractmethod
import datetime
import os, os.path
import numpy as np
import pandas as pd
import tushare as ts
class DataHandler(object):
    """
    DataHandler is an abstract base class providing an interface for
    all subsequent (inherited) data handlers (both live and historic).

    The goal of a (derived) DataHandler object is to output a generated
    set of bars (OHLCVI) for each symbol requested. 

    This will replicate how a live strategy would function as current
    market data would be sent "down the pipe". Thus a historic and live
    system will be treated identically by the rest of the backtesting suite.
    """

    __metaclass__ = ABCMeta



    @abstractmethod
    def get_latest_bars(self, symbol, N=1):
        """
        Returns the last N bars updated.
        """
        raise NotImplementedError("Should implement get_latest_bars()")

    @abstractmethod
    def get_latest_bars_values(self, symbol, val_type, N=1):
        """
        Returns the last N bar values from the 
        latest_symbol list, or N-k if less available.
        input:
            symbol:str eg:'600000.sh'
        output:
            dataframe:'datetime','symbol','close','open',...

        """
        raise NotImplementedError("Should implement get_latest_bars_values()")

    @abstractmethod
    def update_bars(self):
        """
        Pushes the latest bars to the bars_queue for each symbol
        in a tuple OHLCVI format: (datetime, open, high, low, 
        close, volume, open interest).
        """

        raise NotImplementedError("Should implement update_bars()")

class TSPro_DataHandler(DataHandler):

    def __init__(self, ts_pkl_dir, symbol_list, start_date):
        
        self.ts_pkl_dir = ts_pkl_dir #tushare 生成的文件的目录
        self.symbol_list = symbol_list #需要分析的股票列表
        self.start_date = start_date #开始分析日期
        self.symbol_data_all = {}
        self.symbol_data = {}#已字典形式存储股票数据{'600000.sh':(dataframe),'600000.sh':(dataframe)}
        self.latest_symbol_data = {}#已字典形式存储最新的
        self.continue_backtest = True  #数据Update到最新后就达到数据结尾标记，停止backtest 
        self.bar_index = 0    
        self._import_ts_files()
        self.update_bars()#首先初始化一次update



    def _import_ts_files(self):#把需要的数据读入symbol_data
        for iSymbol in self.symbol_list:
            df=pd.read_pickle('%s/%s.pkl'%(self.ts_pkl_dir,iSymbol))
            
            self.symbol_data_all[iSymbol]=df
        
        self.bar_index=len(df[df['trade_date']<self.start_date])  #从开始的计算的起开始做数据按日更新【以最后一个为参考】
        
    
        
    def get_latest_bars(self, symbol, N=1):
        df=self.symbol_data[symbol].iloc[-N:,:]
        return df

    def get_latest_bars_values(self, symbol,value_list, N=1):
        df=self.symbol_data[symbol].loc[:,value_list].iloc[-N:,:]
        return df  #dataframe 格式 
        
    def get_latest_bars_values_list(self, symbol):
        return self.symbol_data[symbol].columns.tolist()  #list格式 

    def get_latest_bar_datetime(self,symbol):
        df=self.get_latest_bars_values(symbol,['trade_date'])
        return df['trade_date'].iloc[0]  #时间字符串
    
    def update_bars(self):
        self.bar_index += 1
        for iSymbol in self.symbol_list:
            self.symbol_data[iSymbol]=self.symbol_data_all[iSymbol].iloc[:self.bar_index,:]
        
        if self.bar_index>=len(self.symbol_data_all[iSymbol]):
            self.continue_backtest=False
           


if __name__=='__main__': #本模块的测试程序
    td=TSPro_DataHandler('/Users/mac/Qigit/symbol_data',['000001.SZ'],'20180604')
    td1=td.get_latest_bars_values('000001.SZ',['trade_date','close','open'])
    td2=td.get_latest_bars('000001.SZ')
    print(td.get_latest_bar_datetime('000001.SZ'),td.get_latest_bars_values('000001.tdSZ',['trade_date','close','open'],10))
    td.update_bars()
    print(td.get_latest_bar_datetime('000001.SZ'),td.get_latest_bars_values('000001.SZ',['trade_date','close','open'],10))
    td.update_bars()
    print(td.get_latest_bar_datetime('000001.SZ'),td.get_latest_bars_values('000001.SZ',['trade_date','close','open'],10))
    

    0
    


    
    
    



