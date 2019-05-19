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

if __name__=='__main__': 
    td1=TFetchData('600000','2018-01-01').data
    td2=TFetchData('600004','2018-01-01').data
    td3=YFetchData('600006','2018-01-01').data
    0
 
    #print(td.data.head(5))
