
from __future__ import print_function

from abc import ABCMeta, abstractmethod
import datetime
try:
    import Queue as queue
except ImportError:
    import queue

import numpy as np
import pandas as pd
from data import TSPro_DataHandler
import dataAnalysis as da
all_return_info=pd.DataFrame(columns=['ts_code','hold_day_num','return_final'])
all_return_info['ts_code']=da.symbol_list()
all_return_info.set_index('ts_code',inplace=True)
class Strategy(object):
    """
    Strategy is an abstract base class providing an interface for
    all subsequent (inherited) strategy handling objects.

    The goal of a (derived) Strategy object is to generate Signal
    objects for particular symbols based on the inputs of Bars 
    (OHLCV) generated by a DataHandler object.

    This is designed to work both with historic and live data as
    the Strategy object is agnostic to where the data came from,
    since it obtains the bar tuples from a queue object.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def calculate_signals(self):
        """
        Provides the mechanisms to calculate the list of signals.
        """
        raise NotImplementedError("Should implement calculate_signals()")

class MACDPro_Strategy(Strategy):

    def __init__(self, bars,iSymbol): 
        """
        Initialises the buy and hold strategy.
        Parameters:
        bars - The DataHandler object that provides bar information 数据处理的类
        events - The Event Queue object. 事件
        short_window - The short moving average lookback.
        long_window - The long moving average lookback.
        """
        self.symbol = iSymbol
        self.analysis_dates=90
        self.bars = bars  #bars数据操作类
        self.value_list=['ts_code','trade_date','close','MACDXPre','ROC+1','ROC+2','ROC+3']
        self.signals= pd.DataFrame() #历史的signal 信息
        self.datetime=self.bars.get_latest_bar_datetime       
    
    def calculate_signals(self): #计算初始化的 买卖 方向 ，初始都是0:OUT  1:BUY
        self.bars.update_bars() #增加一条新的数据
        df_bars=self.bars.get_latest_bars_values(self.symbol,self.value_list,self.analysis_dates)

        if df_bars.iat[-1,df_bars.columns.get_loc('MACDXPre')]>=1: #看当前是否是MACDPre买点

            df_bars_select=df_bars[df_bars['MACDXPre']>=1]
            df_bars_select_success=df_bars_select[(df_bars_select['ROC+1']>1)|(df_bars_select['ROC+2']>1)|(df_bars_select['ROC+3']>2)] #把预测出金叉中后三天内上涨的画出来
            if len(df_bars_select)!=0:
                success_rate=len(df_bars_select_success)/len(df_bars_select)
            else:
                success_rate=0

            if success_rate>=0.5:
                res_signals=1
            else:
                res_signals=0
        else:
            res_signals=0

        df=pd.DataFrame({ 
            'trade_date':[self.bars.get_latest_bar_datetime(self.symbol)],
            'close':self.bars.get_latest_bars_values(self.symbol,['close']).values[0],
            'close_base':[0.0],
            'signals':[res_signals],
            'return_rate_day':[0.0],
            'return_rate_cum':[0.0],
            })
        

        self.signals=self.signals.append(df)

        index_signals=self.signals.columns.get_loc('signals')
        index_close=self.signals.columns.get_loc('close')
        index_close_base=self.signals.columns.get_loc('close_base')
        index_rrd=self.signals.columns.get_loc('return_rate_day')
        #index_rrc=self.signals.columns.get_loc('return_rate_cum')

        if len(self.signals)>=5:
            if list((self.signals.iloc[-2:,index_signals]).values)==[0,1]: #如果是由0-1新买入信号
                self.signals.iat[-1,index_close_base]=self.signals.iat[-1,index_close] #记录买入的价格


            elif list((self.signals.iloc[-2:,index_signals]).values)==[1,1]: #如果是已经买入的情况，继续买入信号
                self.signals.iat[-1,index_close_base]=self.signals.iat[-2,index_close_base]
                self.signals.iat[-1,index_rrd]=(self.signals.iat[-1,index_close]-self.signals.iat[-2,index_close])/self.signals.iat[-1,index_close_base]*100.0

            elif list((self.signals.iloc[-2:,index_signals]).values)==[1,0]: #如果出现卖出信号
                self.signals.iat[-1,index_close_base]=self.signals.iat[-2,index_close_base]
                self.signals.iat[-1,index_rrd]=(self.signals.iat[-1,index_close]-self.signals.iat[-2,index_close])/self.signals.iat[-1,index_close_base]*100.0 
                
                if list((self.signals.iloc[-3:,index_signals]).values)==[0,1,0]: #刚刚持有1天，出现卖出情况
                    if self.signals.iat[-1,index_rrd]>8.0:
                        self.signals.iat[-1,index_signals]=0
                    elif self.signals.iat[-1,index_rrd]>-2.0:
                        self.signals.iat[-1,index_signals]=1

                elif list((self.signals.iloc[-4:,index_signals]).values)==[0,1,1,0]:
                    if self.signals.iat[-1,index_rrd]>8.0:
                        self.signals.iat[-1,index_signals]=0
                    elif self.signals.iat[-1,index_rrd]>-1.0:
                        self.signals.iat[-1,index_signals]=1

                elif list((self.signals.iloc[-5:,index_signals]).values)==[0,1,1,1,0]:
                    if self.signals.iat[-1,index_rrd]>8.0:
                        self.signals.iat[-1,index_signals]=0
                    elif self.signals.iat[-1,index_rrd]>1.0:
                        self.signals.iat[-1,index_signals]=1

                elif list((self.signals.iloc[-6:,index_signals]).values)==[0,1,1,1,1,0]:
                    if self.signals.iat[-1,index_rrd]>8.0:
                        self.signals.iat[-1,index_signals]=0
                    elif self.signals.iat[-1,index_rrd]>3.0:
                        self.signals.iat[-1,index_signals]=1
        self.signals.loc[:,'return_rate_cum']=np.cumsum(self.signals.loc[:,'return_rate_day'].values)

def backtest(symbol):
    global all_return_info

   # try:
    symbol_list=[symbol]
    start_date='20180604'
    td=TSPro_DataHandler('/Users/mac/Qigit/MySelectSymbolsV1/symbol_data',symbol_list,start_date)
    iStrategy=MACDPro_Strategy(td,symbol_list[0])
    while(iStrategy.bars.continue_backtest):
        iStrategy.calculate_signals()
        
    res_df=iStrategy.signals
    res_df.to_csv('res/%s.csv'%symbol)
    all_return_info.loc[symbol,'return_final']=res_df['return_rate_cum'].iloc[-1]
    all_return_info.loc[symbol,'hold_day_num']=len(res_df[res_df['return_rate_day']!=0])
    all_return_info.loc[symbol,'return_day_max']=res_df['return_rate_day'].max()
    all_return_info.loc[symbol,'return_day_min']=res_df['return_rate_day'].min()
    return res_df
    #except:
       # return 0

if __name__=='__main__':
    import multiprocessing as mp
    from multiprocessing import Pool
    mp.set_start_method('spawn')
    
    import time
    t0 = time.time()
    #symbol_lists=da.symbol_list()
    symbol_lists=['002829.SZ','002552.SZ','002237.SZ']
    symbol_lists=da.symbol_list()
    #symbol_lists=pd.read_pickle('/Users/mac/Qigit/MySelectSymbolsV1/Symbollist.pkl')


    
    # with Pool(2) as p:
    #    res_df=p.map(backtest, symbol_lists[:10]) #采用多进程进行并行计算
    
    for i in symbol_lists[:]:
        try:
            backtest(i)
            all_return_info.to_csv('all_return_info.csv')
        except:
            print('err:%s'%i)
            continue
        print('suc:%s'%i)

    all_return_info.to_csv('all_return_info.csv')
    elapsed = time.time()-t0
    msg = "{:.2f}s"
    print(msg.format(elapsed))
    0

    



    











   
        

   
        
