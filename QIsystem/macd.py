import datetime
import numpy as np

import tushare as ts
import pandas as pd
from backtest import Backtest
from data import HistoricTsDataHandler
from event import SignalEvent
from execution import SimulatedExecutionHandler
from portfolio import Portfolio
from strategy import Strategy

a1=[]
b1=[]
class MACDStrategy(Strategy):
    """
    Carries out a basic Moving Average Crossover strategy with a
    short/long simple weighted moving average. Default short/long
    windows are 100/400 periods respectively.
    """
   
    

    def __init__(self, bars, events, short_window=100, long_window=400):
        """
        Initialises the buy and hold strategy.

        Parameters:
        bars - The DataHandler object that provides bar information
        events - The Event Queue object.
        short_window - The short moving average lookback.
        long_window - The long moving average lookback.
        """
       
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events
        self.short_window = short_window
        self.long_window = long_window

        # Set to True if a symbol is in the market
        self.bought = self._calculate_initial_bought()

    def _calculate_initial_bought(self):
        """
        Adds keys to the bought dictionary for all symbols
        and sets them to 'OUT'.
        """
        bought = {}
        for s in self.symbol_list:
            bought[s] = 'OUT'
        return bought

    def calculate_signals(self, event):
        """
        Generates a new set of signals based on the MAC
        SMA with the short window crossing the long window
        meaning a long entry and vice versa for a short entry.    

        Parameters
        event - A MarketEvent object.
        
        """
        
        if event.type == 'MARKET':
            for symbol in self.symbol_list:
                bars = self.bars.get_latest_bars_values(symbol, "close", N=self.long_window) 
                global b1
                b1=bars

                if bars is not None and bars != []:
                                    
                    df=pd.DataFrame(bars)
                    df['DIFF'],df['DAE'],df['MACD'] = talib.MACD(bars,12,26,9)   
                    df['MACD']*=2
                    df['MACDdiff']=df['MACD'].diff()
                  

                    dt = self.bars.get_latest_bar_datetime(symbol)
                    sig_dir = ""
                    strength = 1.0
                    strategy_id = 1
                    
                    global a1
                    a1.append(self.bought[symbol])
                   
                    

                    if df['MACD'].iloc[-1] > 0  and df['MACD'].iloc[-2] < 0 and self.bought[symbol] == "OUT":
                        sig_dir = 'LONG'
                        signal = SignalEvent(strategy_id, symbol, dt, sig_dir, strength)
                        self.events.put(signal)
                        self.bought[symbol] = 'LONG'

                    elif df['MACD'].iloc[-1] < 0  and df['MACD'].iloc[-2] > 0  and self.bought[symbol] == "LONG":
                        sig_dir = 'EXIT'
                        signal = SignalEvent(strategy_id, symbol, dt, sig_dir, strength)
                        self.events.put(signal)
                        self.bought[symbol] = 'OUT'
                        
                  


if __name__ == "__main__":
    
    csv_dir = ''
    #symbol_list = ['600036','601398','601988','600519']
    symbol_list = ['000001']
     
    initial_capital = 100000.0
    start_date = datetime.datetime(2018,5,11,0,0,0)
    heartbeat = 0.0
    

    backtest = Backtest(csv_dir, 
                        symbol_list, 
                        initial_capital, 
                        heartbeat,
                        start_date,
                        HistoricTsDataHandler, 
                        SimulatedExecutionHandler, 
                        Portfolio, 
                        MACDStrategy)
    
    backtest.simulate_trading()
