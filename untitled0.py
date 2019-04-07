#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 14:38:33 2019

@author: mac
"""

import tushare as ts 
ts.set_token('bf3b4e51fcc67507e8694e9a3f2bd591be93bea276f9d86f564fe28f')
pro = ts.pro_api()
df = ts.pro_bar(api=pro, ts_code='000001.SZ', adj='qfq',start_date='20180101')
df=df['trade_date'].sort()