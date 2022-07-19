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



ohlc_list = []
minute = 0
tictime = 0
ohlc = np.empty((1,4))
start = 0
last = 20
aam = 0
mean = []
candletime = []
lenofcandle = []
std_c = []
std_p = []
bol_up = [np.nan]
bol_down = [np.nan]
ma = 50
k = 0

# Constants for getting local maxima/minima 
a = 10 # Half of the local length
b = a - 1 
c = 2*a - 1 # Local length  
localmaxval = []
localminval = []
mintomax = []
maxtomin = []

positionl = 0
positions = 0
asset = 100
assets = 100

kj = 0 #kj is the index to check what is the data like.
for h in range(start,last):
    print(round(start/(last-start),2,'%'))

    with gzip.open('D:/tbproject/BTCUSD/DATA/%03d.gz' % h, 'rb') as f:
        data = f.readlines()

    daytics = []
    for row in data:
        daytics.append(row.decode('utf-8').split(','))
    
    del daytics[0]
    daytics.reverse()

    if h == start:
        if kj == 0: #Using kj, we can see how is the data like
            #print(row)
            kj = 1

        price = float(daytics[1][4])
        candletime.append(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(daytics[1][0]))))
        ohlc = np.append(ohlc,[[price,price,price,price]],axis =0)
        ohlc = np.delete(ohlc,0, axis = 0)


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

        # 1 min candle ===================================================================
        # with bolband
        if minute != tictime//60:
            k+=1
            minute = tictime//60
            candletime.append(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(tictime))))
            ohlc = np.append(ohlc,[[ohlc_list[0],max(ohlc_list),min(ohlc_list),ohlc_list[-1]]],axis = 0)
            lenofcandle.append(max(ohlc_list)-min(ohlc_list))
            ohlc_list = []

            if k >= ma:
                candlestd = np.array(lenofcandle[-ma:])
                std_c.append(np.std(candlestd))
                std_c = std_c[-ma:]
                aa = np.array(std_c)
                aam = np.mean(aa)
                std_p = np.std(ohlc[-ma:,3])
                mean.append(np.mean(ohlc[-10:,3]))

            if np.argmax(ohlc[-c:,2]) == a:
                localmaxval.append(ohlc[-a,2])
                if localminval:
                    mintomax.append(abs(localmaxval[-1] - localminval[-1]))
            if np.argmin(ohlc[-c:,3]) == a:
                localminval.append(ohlc[-a,3])
                if localmaxval:
                    maxtomin.append(abs(localmaxval[-1] - localminval[-1]))
        # 1 min candle ===================================================================

        ###### Here, U can write ur strategy. U have bundle of ticdata(got once) from bybit server 
        if not aam:
            continue

        price = float(row[4])

        if positionl:
            if price > bol_up[-1]:# or 2*mintomax[-1] < price -lpoint:
                positionl = 0
                temp = asset
                asset = asset*price/lpoint
                print('Selling longposition',k,round(asset,2),round(asset - temp,2))
        else:
            if price < bol_down[-1] - 30:
                positionl = 1
                lpoint = price
                print('buying longposition',k)

        if positions:
            if price < bol_down[-1]:# or 2*mintomax[-1] < price -lpoint:
                positions = 0
                temp = assets
                asset = assets*price/spoint
                print('#Selling short position',k,round(asset,2),round(asset - temp,2))
        else:
            if price > bol_up[-1] + 30:
                positions = 1
                spoint = price
                print('#buying short position',k)

            
#=============== Candle Chart =================
index = pd.DatetimeIndex(candletime)
ohlc_df = DataFrame(data=ohlc, index=index, columns=['open','high','low','close'])
ohlc_df = ohlc_df.astype(float)
ohlc_df['ma5'] = ohlc_df['close'].rolling(20).mean()

with open('ma.txt','w') as f:
    f.writelines(str(mean))
ma5 = go.Scatter(x=ohlc_df.index, y=ohlc_df['ma5'], line=dict(color='black', width=0.8), name='ma5')
'''
colorset = mpf.make_marketcolors(up='tab:red', down='tab:blue', volume='tab:blue')
s = mpf.make_mpf_style(marketcolors = colorset)
mpf.plot(ohlc_df,type = 'candle',style=s)
'''
candle = go.Candlestick(
    x=ohlc_df.index,
    open=ohlc_df['open'],
    high=ohlc_df['high'],
    low=ohlc_df['low'],
    close=ohlc_df['close']
    )
    
mintomax = np.array(mintomax)
mintomax = DataFrame(data=mintomax, columns =['mintomax'])
maxtomin = np.array(maxtomin)
maxtomin = DataFrame(data=maxtomin, columns =['maxtomin'])
minmax = pd.concat([mintomax,maxtomin],axis=1)
minmax.to_excel('minmax.xlsx')


'''
ohlc_df.to_excel('ohlc.xlsx')
fig = go.Figure(data=[candle])
fig.write_image("fig1.svg")
#fig = go.Figure(data=candle)
fig.show()
'''

























