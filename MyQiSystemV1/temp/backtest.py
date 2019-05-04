# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 20:47:27 2019
@author: MI
macd_select_backtest
策略：macd 预测
"""
import pandas as pd
import numpy as np
from data import TSPro_DataHandler
from strategy import MACDPro_Strategy
import matplotlib.pyplot as plt



symbol_list=['000004.SZ']
start_date='20180604'
value_list=['ts_code','trade_date','close','MACDXPre','ROC+1','ROC+2','ROC+3']

td=TSPro_DataHandler('/Users/mac/Qigit/MySelectSymbolsV1/symbol_data',symbol_list,start_date)
iStrategy=MACDPro_Strategy(td,symbol_list[0])
signals_hist=[]

while(iStrategy.bars.continue_backtest):
    iStrategy.calculate_signals()
    df=iStrategy.signals

data_df=iStrategy.bars.symbol_data[iStrategy.symbol]
data_df=data_df.set_index('trade_date')

df=df.set_index('trade_date',drop=False)
0   