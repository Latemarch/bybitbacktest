import numpy as np
import pandas as pd
import gzip
import math
import mplfinance as mpf
import pandas as pd
import time
import datetime
import plotly.graph_objects as go

from pandas.core.frame import DataFrame
#mac



def traiding(position, buyorsell):
    i = 1 if position == 'long' else 0
    if buyorsell == 'buy':
        balance[i][0] = 1
        balance[i][1] = price
    else:
        balance[i][0] = 0
        add = ((i*2)-1)*(price - balance[i][1])*qty-0.058
        balance[i][2] += add

def record_history(position,bors):
    i = 1 if position == 'long' else 0
    k = 0 if bors == 'buy' else 2
    history[i+k].append([candletime[-1]])
    history[i+k][-1].append(price)


ohlc_list = []
minute = 0
tictime = 0
ohlc = np.empty((1,4))
start = 0
last = 30
aam = 0
mean = []
balance = [[0,0,100],[0,0,100]]
candletime = []
lenofcandle = []
k = 0

# Constants for getting local maxima/minima 
a = 5 # Half of the local length
b = a - 1 
c = 2*a - 1 # Local length  
localmaxval = []
localminval = []
mintomax = []
maxtomin = []
localmaxpoint =[]
localminpoint =[]
overshooting_long= []
overshooting_short= []
count_itoa = 0
count_atoi = 0

losstimeL = 0
losstimeS = 0

history = [[[0,0]],[[0,0]],[[0,0]],[[0,0]]]
stopbuyings = 1
stopbuyingl = 1
kj = 1

for h in range(start,last):

    with gzip.open('/Users/jun/btcusd/%03d.gz' % h, 'rb') as f:
        data = f.readlines()

    daytics = []
    for row in data:
        daytics.append(row.decode('utf-8').split(','))
    
    del daytics[0]
    daytics.reverse()

    if h == start:

        price = float(daytics[1][4])
        candletime.append(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(daytics[1][0]))))
        ohlc = np.append(ohlc,[[price,price,price,price]],axis =0)
        ohlc = np.delete(ohlc,0, axis = 0)

    qty = 100/price

    for i, row in enumerate(daytics):
        ohlc_list.append(float(row[4]))
        #tprice = float(row[4])

        # To make bundle of ticdatas having "same" time
        if tictime == float(row[0]): 
            continue
        else:
            tictime = float(row[0])
        # Now, I got the data from the server, 
        # server give me the data bundle which regards datas made similar time as same time 

        # 1 min candle ==================================================
        if minute != tictime//60:
            k+=1
            minute = tictime//60
            candletime.append(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(tictime))))
            ohlc = np.append(ohlc,[[ohlc_list[0],max(ohlc_list),min(ohlc_list),ohlc_list[-1]]],axis = 0)
            lenofcandle.append(max(ohlc_list)-min(ohlc_list))
            ohlc_list = []
        # 1 min candle ==================================================

        ###### Here, U can write ur strategy. U have bundle of ticdata(got once) from bybit server 
            if not k > 120: continue
            movingaverage1 = np.mean(ohlc[-20:,3])
            movingaverage2 = np.mean(ohlc[-50:,3])
            movingaverage3 = np.mean(ohlc[-120:,3])
            if movingaverage1 > movingaverage2 > movingaverage3:
                if not trend == 'long' and 15<k-losstimeS:stopbuyings = 0
                trend = 'long'
            elif movingaverage1 < movingaverage2 < movingaverage3: 
                if not trend == 'short' and 15<k-losstimeL:stopbuyingl = 0
                trend = 'short'
            else: trend = 'None'
        if not k > 120: continue

        price = float(row[4])
        if balance[1][0]:
            if price < lossprice_L:
                traiding('long','sell')
                record_history('long','sell')
                #print(round(balance[1][2],2))
                if price < lossprice_L : 
                    stopbuyingl = 1
                    losstimeL = k
            elif price > profitprice_L and trend != 'long':
                traiding('long','sell')
                record_history('long','sell')


        if balance[0][0]:
            if price < profitprice_s or lossprice_s < price:
                traiding('short','sell')
                record_history('short','sell')
                #print(round(balance[0][2],2),'--')
                #stopbuyings = 1
                if lossprice_s < price: 
                    stopbuyings = 1
                    losstimeS = k

        if balance[1][0] or balance[0][0]: continue
        if trend == 'long':
            if price < movingaverage1 and not balance[1][0] and not stopbuyingl:
                traiding('long','buy')
                record_history('long','buy')
                profitprice_L = price*1.01
                lossprice_L = price*0.995
                continue

        elif trend == 'short':
            if not balance[0][0] and not stopbuyings and price > movingaverage1:
                traiding('short','buy')
                record_history('short','buy')
                profitprice_s = price*0.99
                lossprice_s = price*1.005
        
    print(h,'/',last-start,'))',round(balance[0][2],2),round(balance[1][2],2), round(100*(float(daytics[0][4])-float(daytics[-1][4]))/float(daytics[0][4]),2))


'''            
#=============== Candle Chart =================
index = pd.DatetimeIndex(candletime)
ohlc_df = DataFrame(data=ohlc, index=index, columns=['open','high','low','close'])
ohlc_df = ohlc_df.astype(float)
ohlc_df['ma10'] = ohlc_df['close'].rolling(20).mean()
ohlc_df['ma20'] = ohlc_df['close'].rolling(50).mean()
ohlc_df['ma50'] = ohlc_df['close'].rolling(120).mean()
ohlc_df['max'] = np.nan
ohlc_df['min'] = np.nan
ohlc_df['buy_long'] = np.nan
ohlc_df['sell_long'] = np.nan
ma10 = go.Scatter(x=ohlc_df.index, y=ohlc_df['ma10'], line=dict(color='black', width=0.8), name='ma10')
ma10 = go.Scatter(x=ohlc_df.index, y=ohlc_df['ma10'], line=dict(color='black', width=0.8), name='ma10')
ma20 = go.Scatter(x=ohlc_df.index, y=ohlc_df['ma20'], line=dict(color='green', width=0.8), name='ma20')
ma50 = go.Scatter(x=ohlc_df.index, y=ohlc_df['ma50'], line=dict(color='red', width=0.8), name='ma50')

for i, val in enumerate(localmaxval):
    ohlc_df.loc[localmaxpoint[i],'max'] = val + 20
for i, val in enumerate(localminval):
    ohlc_df.loc[localminpoint[i],'min'] = val - 20
maxval = go.Scatter(x=ohlc_df.index, y=ohlc_df['max'], mode ="markers", marker=dict(color='green',symbol= '6'), name='Max')
minval = go.Scatter(x=ohlc_df.index, y=ohlc_df['min'], mode ="markers", marker=dict(color='red',symbol = '5'), name='Min')

for i in range(4): history[i].pop(0)

k = 1 #select position u wanna see (0=short,1=long)
for i, val in enumerate(history[k]):
    ohlc_df.loc[val[0],'buy_long'] = val[1] - 200
for i, val in enumerate(history[k+2]):
    ohlc_df.loc[val[0],'sell_long'] = val[1] + 200

history_SL = go.Scatter(x=ohlc_df.index, y=ohlc_df['sell_long'], mode ="markers", 
                        marker=dict(color='green',symbol= '6'), name='Sell long')
history_BL = go.Scatter(x=ohlc_df.index, y=ohlc_df['buy_long'], mode ="markers", 
                        marker=dict(color='red',symbol = '5'), name='Buy long')

candle = go.Candlestick(
    x=ohlc_df.index,
    open=ohlc_df['open'],
    high=ohlc_df['high'],
    low=ohlc_df['low'],
    close=ohlc_df['close']
    )

fig = go.Figure(data=[candle,history_SL,history_BL,ma10,ma20,ma50])
fig.write_image("fig1.svg")
fig.show()

mintomax = np.array(mintomax)
mintomax = DataFrame(data=mintomax, columns =['mintomax'])
maxtomin = np.array(maxtomin)
maxtomin = DataFrame(data=maxtomin, columns =['maxtomin'])
minmax = pd.concat([mintomax,maxtomin],axis=1)
minmax.to_excel('minmax1.xlsx')
ohlc_df.to_excel('ohlc.xlsx')

#print(overshooting_short)
#print(overshooting_long)
'''

















