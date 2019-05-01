import tushare as ts 
import pandas as pd 


def BBANDS(data, ndays):
    
    MA = pd.Series(data['close'].rolling(ndays).mean())
    SD = pd.Series(data['close'].rolling(ndays).std())
    b1 = MA + (2 * SD)
    B1 = pd.Series(b1, name = 'Upper BollingerBand') 
    data = data.join(B1) 
    b2 = MA - (2 * SD)
    B2 = pd.Series(b2, name = 'Lower BollingerBand') 
    data = data.join(B2) 
 
    return data
 
# Retrieve the Nifty data from Yahoo finance:
data=ts.get_hist_data('600036',start='2016-1-1')
data = pd.DataFrame(data)
dataClose=pd.Series(data['close'],name='adjClose')
data=data.join(dataClose)
data=data.sort_index()
print(data.head(5))
print(data.columns.values)