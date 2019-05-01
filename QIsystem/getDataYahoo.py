# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 12:57:11 2018

@author: DAC001
"""

from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
yf.pdr_override() # <== that's all it takes :-)
# download dataframe
data = pdr.get_data_yahoo("GOOG", start="2013-01-01", end="2018-08-30")
data2 = pdr.get_data_yahoo("600030.ss", start="2013-01-01", end="2018-08-30")
data3 = pdr.get_data_yahoo("600456.ss", start="2013-01-01", end="2018-08-30")

import tushare as ts
data4=ts.get_hist_data('600030') #一次性获取全部日k线数据
