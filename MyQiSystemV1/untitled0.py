#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 22:51:25 2019

@author: mac
"""

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
dateNum=len(goal_data)
y=goal_data.reshape(-1).tolist()
for i in range(0,len(symbol_data)-len(goal_data)):
    x=symbol_data.loc[i:i+dateNum,['open','high','low','close']].values
    x=x.reshape(-1).tolist()
    r=np.corrcoef(x,y)
    r_coff.append(r[0,1])

if '__name__'=='__main__':
    
    