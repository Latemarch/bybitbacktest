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



ohlc_list = []
minute = 0
tictime = 0
ohlc = np.empty((1,4))
start = 0
last = 1
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


positionl = 0
history_l = []
history_l_v = []
history_ls = []
history_ls_v = []
positions = 0
history_s = []
history_ss = []
asset = 100
assets = 100

kj = 0 #kj is the index to check what is the data like.
for h in range(start,last):
    print(int(h/(last-start)*100),'%')

    with gzip.open('/Users/jun/btcusd/%03d.gz' % h, 'rb') as f:
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

            if np.argmax(ohlc[-c:,1]) == b:
                localmaxval.append(ohlc[-a,1])
                localmaxpoint.append(candletime[-a])
                if localminval:
                    mintomax.append(abs(localmaxval[-1] - localminval[-1]))
                    count_itoa += 1
                    if count_itoa >1 and mintomax[-1] > 2*sum(mintomax[-count_itoa:-1])/(count_itoa-1):
                        #print(count_itoa,'//',mintomax[-1],int(2*sum(mintomax[-count_itoa:-1])/count_itoa))
                        overshooting_long.append(count_itoa)
                        count_itoa = 0
            if np.argmin(ohlc[-c:,2]) == b:
                localminval.append(ohlc[-a,2])
                localminpoint.append(candletime[-a])
                if localmaxval:
                    maxtomin.append(abs(localmaxval[-1] - localminval[-1]))
                    count_atoi += 1
                    if maxtomin[-1] > 300:
                        overshooting_short.append(count_atoi)
                        count_atoi = 0
        # 1 min candle ===================================================================

        ###### Here, U can write ur strategy. U have bundle of ticdata(got once) from bybit server 
            if not k > 120: continue
        #if not mintomax or not maxtomin : continue
            movingaverage1 = np.mean(ohlc[-20:,3])
            movingaverage2 = np.mean(ohlc[-50:,3])
            movingaverage3 = np.mean(ohlc[-120:,3])
        if not k > 120: continue

        price = float(row[4])
        if positionl:
            if price < lossprice_L or profitprice_L < price:
                positionl = 0
                history_ls.append([candletime[-1]])
                history_ls[-1].append(price)
                asset = asset*price_l/price - asset*0.00058
                print(round(asset,2),'/',price_l, price,'Profit')


        if movingaverage1 > movingaverage2 > movingaverage3: 
            if price < movingaverage2 and not positionl:
                positionl = 1
                history_l.append([candletime[-1]])
                history_l[-1].append(price)
                price_l = price
                profitprice_L = price*1.005
                lossprice_L = price*0.995
                print('buy_L')

        elif movingaverage1 < movingaverage2 < movingaverage3: 
            if price > movingaverage2 and not positions:
                positions = 1
                history_s.append([candletime[-1]])
                history_s[-1].append(price)
                price_s = price
                print('buy_s')
            if positionl: 
                positionl = 0
                history_ls.append([candletime[-1]])
                history_ls[-1].append(price)
                asset = asset*price_l/price - asset*0.00058
                print(round(asset,2),'/',price_l, price)

        else:
            if positionl: 
                positionl = 0
                history_ls.append([candletime[-1]])
                history_ls[-1].append(price)
                asset = asset*price_l/price - asset*0.00058
                print(round(asset,2),'/',price_l, price)
            if positions: 
                positions = 0
        



            
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

for i, val in enumerate(history_l):
    ohlc_df.loc[val[0],'buy_long'] = val[1] - 100
for i, val in enumerate(history_ls):
    ohlc_df.loc[val[0],'sell_long'] = val[1] + 100

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



















