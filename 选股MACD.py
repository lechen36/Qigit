import tushare as ts 
import pandas as pd
import indexCal as ic
import dataAnalysis as da
import numpy as np
import matplotlib.pyplot as plt

ts.set_token('bf3b4e51fcc67507e8694e9a3f2bd591be93bea276f9d86f564fe28f')
pro = ts.pro_api()
# 股票处理，去除风险股票，去除ST股票
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
data['ST']=np.char.rfind(data['name'].values.astype('str'),'*ST')#字符串操作，去掉ST的股份
dataSafe=data[data['ST']==-1]


# 数据获取及分析，分析今日出现MACD金叉，金叉Pre的股票
ResultSymbols=list()
ResultDf=pd.DataFrame()
iNum=0
for iSymbol in dataSafe.loc[0:20,'ts_code']:
    try:
        print(iSymbol,':',iNum)
        iNum+=1
        
        df = ts.pro_bar(pro_api=pro, ts_code=iSymbol, adj='qfq',start_date='2018-01-01')   
        df=df.sort_index()
        df=ic.macd_index_cal(df)
        df=ic.kdj_index_cal(df)
        df=ic.ema_index_cal(df)
        df=ic.roc_index_cal(df)
        df=df.fillna(0)


        startDate='20180501'
        df1=df[df.index>startDate]
        #df2=df1[df1['MACDX']==1]
        df2=df1[df1['MACDXPre']>=1]
        df2_success=df2[(df2['ROC+1']>0)|(df2['ROC+2']>0)|(df2['ROC+3']>0)] #把预测出金叉中后三天内上涨的画出来
        if len(df2)!=0:
            success_rate=len(df2_success)/len(df2)
        else:
            continue
        if success_rate>0.6:
            ResultSymbols.append(iSymbol)
            if df.iloc[-1,:]['MACDXPre']>0:
                ResultDf=ResultDf.append(df.iloc[-1,:]) 
                print(iSymbol,':','--------------------OK----------------------')
            
    except:
        continue
    
ResultDf.to_pickle('ResultDf.pkl')

    
# 数据绘图，把利用MACD指标选出来的股进行绘图确认。

    
