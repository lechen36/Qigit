#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 20:07:09 2019

@author: mac
"""
import tushare as ts 
import pandas as pd
import indexCal as ic
import numpy as np
import os



start_fetch_date='20180101'
start_analysis_date='20180501'
ts.set_token('bf3b4e51fcc67507e8694e9a3f2bd591be93bea276f9d86f564fe28f')
pro = ts.pro_api()

data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
data['ST']=np.char.rfind(data['name'].values.astype('str'),'*ST')#字符串操作，去掉ST的股份
dataSafe=data[data['ST']==-1] 
dataSafe=dataSafe[dataSafe['ts_code'].str.slice(0,3)!='300']