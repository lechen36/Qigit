import datetime
import numpy as np
import pandas as pd 

from backtest import Backtest
from data import HistoricTsDataHandler
from event import SignalEvent
from execution import SimulatedExecutionHandler
from portfolio import Portfolio
from strategy import Strategy
from sklearn.externals import joblib

class svmStrategy(Strategy):
    """
    Carries out a basic Moving Average Crossover strategy with a
    short/long simple weighted moving average. Default short/long
    windows are 100/400 periods respectively.
    """

    def __init__(self, bars, events, portfolio,short_window=15, long_window=30): 
        """
        Initialises the buy and hold strategy.

        Parameters:
        bars - The DataHandler object that provides bar information 数据处理的类
        events - The Event Queue object. 事件
        short_window - The short moving average lookback.
        long_window - The long moving average lookback.
        """
        self.bars = bars  #数据处理的类，回测类中使用，实际是 HistoricTsDataHandler 这个类
        self.symbol_list = self.bars.symbol_list #股票列表，从数据类里面取出来
        self.events = events #策略的事件、  回测的事件  即一个队列
        self.short_window = short_window
        self.long_window = long_window
        self.portfolio = portfolio #资产组合类传递
        self.model=self._load_model() #载入训练好的模型
        # Set to True if a symbol is in the market
        self.bought = self._calculate_initial_bought()
                        
           #
    
    def _load_model(self):
        model = joblib.load('model001.pkl') 
        return model


    def _calculate_initial_bought(self): #计算初始化的 买卖 方向 ，初始都是OUT
        """
        Adds keys to the bought dictionary for all symbols
        and sets them to 'OUT'.
        """
        bought = {}
        for s in self.symbol_list:  
            bought[s] = 'OUT'
        return bought

    def calculate_signals(self, event):  #计算信号，输入： 事件  输出：
        """
        Generates a new set of signals based on the MAC
        SMA with the short window crossing the long window
        meaning a long entry and vice versa for a short entry.    

        Parameters
        event - A MarketEvent object. 
        """
        if event.type == 'MARKET':
            for symbol in self.symbol_list:
                 #策略类 利用self.bars 类来获取数据
                df=pd.DataFrame()
                slabel=['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'pre_close',\
                         'change', 'pct_chg', 'vol', 'amount', 'ema5', 'ema10', 'ema20', 'ema60',\
                         'DIFF', 'DEA', 'MACD', 'MACDX', 'kdj_k', 'kdj_d', 'kdj_j', 'ROC_1',\
                         'ROC_2', 'ROC_3', 'ROC_5']
                for iLabel in slabel:
                    df[iLabel]=self.bars.get_latest_bars_values(symbol, iLabel,N=self.long_window) 
                
                
                x=df.drop(columns=['trade_date','ts_code'])
                trainX=x.iloc[:,0:19]

                predictY=self.model.predict(trainX)
                predictY=predictY[-1]


                bars = self.bars.get_latest_bars_values(symbol, 'close',N=self.long_window) 
                #bars = self.bars.get_latest_bars_values(symbol, 'close', N=self.long_window)
                #a1=self.portfolio.all_holdings[0]
                #print(a1)

                if bars is not None and bars != []:

                    dt = self.bars.get_latest_bar_datetime(symbol)
                    sig_dir = ""
                    strength = 1.0
                    strategy_id = 1

                    if predictY==1 and self.bought[symbol] == "OUT":
                        sig_dir = 'LONG'
                        signal = SignalEvent(strategy_id, symbol, dt, sig_dir, strength) #策略ID，symbol，datetime，LONG，1.0
                        self.events.put(signal)  #把这个signal（代码、）放到 策略.队列中
                        self.bought[symbol] = 'LONG'  #策略的买卖  记录为 LONG
                        

                    elif predictY==0 and self.bought[symbol] == "LONG":
                        sig_dir = 'EXIT'
                        signal = SignalEvent(strategy_id, symbol, dt, sig_dir, strength)
                        self.events.put(signal)
                        self.bought[symbol] = 'OUT'


if __name__ == "__main__":
    csv_dir = '' #csv 文件的目录
    symbol_list = ['600088.SH'] #股票代码列表
    initial_capital = 100000.0 #初始资本
    start_date = datetime.datetime(2018,1,1,0,0,0) #开始事件
    heartbeat = 0.0 #while循环 暂停时间

#初始化一个回测的类
    backtest = Backtest(csv_dir,  
                        symbol_list, 
                        initial_capital, 
                        heartbeat,
                        start_date,
                        HistoricTsDataHandler, #类，data中，处理数据
                        SimulatedExecutionHandler,  #类，execution
                        Portfolio, #类，资产组合处理
                        svmStrategy) #类，移动平均 策略
#模拟交易    
    backtest.simulate_trading()
