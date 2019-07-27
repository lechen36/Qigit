#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 11:09:31 2019

@author: zlw
"""

from __future__ import print_function
from abc import ABCMeta, abstractmethod
import os, os.path
import numpy as np
import pandas as pd
import fix_yahoo_finance as yf
import tushare as ts
import matplotlib.pyplot as plt

class FetchData(object):
    """
    Fetch Data from yahoo or tushare

    """
    __metaclass__ = ABCMeta
    @abstractmethod
    def _get_data(self, symbol):
        """
        Returns data.
        """
        raise NotImplementedError("Should implement _get_data()")

class YFetchData(FetchData):
    def __init__(self,symbol, start_date):
        self.symbol = symbol
        self._rename_symbol()
        self.start_date = start_date #'2018-01-01'
        self.data=self._get_data()
        
    def _rename_symbol(self):
        if self.symbol[0]=='6':
            self._symbol_name = self.symbol[:6]+'.SS'
        elif self.symbol[0]=='0':
            self._symbol_name = self.symbol[:6]+'.SZ'
        else:
            print('input symbol err')
            
    def _get_data(self):
        try:
            df=yf.download(self._symbol_name, start=self.start_date,auto_adjust=True)
            df.columns=['open', 'high', 'low', 'close', 'vol']
            df.loc[:,'ts_code']=self.symbol
            df.loc[:,'trade_date']=df.index.strftime('%Y%m%d').values
            df=df[['ts_code','trade_date','open','high','low','close','vol']]
            return df
        except:
            pass
  
class TFetchData(FetchData):
    def __init__(self,symbol, start_date):
        self.symbol = symbol
        self._rename_symbol()
        self.start_date = start_date #'2018-01-01'
        self.data=self._get_data()
    
    def _rename_symbol(self):
        if self.symbol[0]=='6':
            self._symbol_name = self.symbol[:6]+'.SH'
        elif self.symbol[0]=='0':
            self._symbol_name = self.symbol[:6]+'.SZ'
        else:
            print('input symbol err')
        
    def _get_data(self):
        try:
            ts.set_token('bf3b4e51fcc67507e8694e9a3f2bd591be93bea276f9d86f564fe28f')
            pro = ts.pro_api()
            df = ts.pro_bar(api=pro, ts_code=self._symbol_name, adj='qfq',start_date=self.start_date)
            df.loc[:,'ts_code']=self.symbol
        except:
            pass
        return df
    
def hist_corr(symbol_data,goal_data):
    """
        symbol_data: DataFrame
            columns:       example:
            ts_code         600015
            trade_date    20190611
            open              7.58
            high              7.67
            low               7.56
            close             7.66
            pre_close         7.57
            change            0.09
            pct_chg           1.19
            vol             313194
            amount          238978 
    """
    r_coff=[]
    dateNum=len(goal_data)
    y=goal_data.loc[:,['open','high','low','close']].values
    y=y.reshape(-1).tolist()
    for i in range(0,len(symbol_data)-len(goal_data)):
        x=symbol_data.loc[i:i+dateNum-1,['open','high','low','close']].values
        x=x.reshape(-1).tolist()
        print(len(x),len(y))
        r=np.corrcoef(x,y)
        r_coff.append(r[0,1])
        
    return r_coff


if __name__=='__main__': 
#    array_list=[]
#    for i in ['600015','600016','600017']:
#        td=TFetchData(i,'2018-01-01').data
#        td_array=td.loc[:,['open','high','low','close']].values
#        td_array=td_array.reshape(-1).tolist()
#        array_list.append(td_array)
    
    i='600015'
    symbol_data=TFetchData(i,'2018-01-01').data
    goal_data=symbol_data.iloc[-10:,:]
    
    r_coff=hist_corr(symbol_data,goal_data)

 
    #print(td.data.head(5))
