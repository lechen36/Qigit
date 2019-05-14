import numpy as np 
import pandas as pd 
import tushare as ts 

start_fetch_date='20180101'
start_analysis_date='20180501'
ts.set_token('bf3b4e51fcc67507e8694e9a3f2bd591be93bea276f9d86f564fe28f')
pro = ts.pro_api()

df111 = ts.pro_bar(api=pro, ts_code='000001.SZ', adj='qfq',start_date=start_fetch_date)
df = pro.index_daily(ts_code='000001.SH')
print(df.head(5))
0