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



def trading(position, buyorsell):
    i = 1 if position == 'long' else 0
    if buyorsell == 'buy':
        balance[i][0] = 1
        balance[i][1] = price
    else:
        balance[i][0] = 0
        add = ((i*2)-1)*(price - balance[i][1])*qty-0.058
        balance[i][2] += add
        if i == 1:
            if add > 0:tradingcountL[0] += 1
            else: tradingcountL[1] +=1
        else:
            if add > 0:tradingcountS[0] += 1
            else: tradingcountS[1] +=1
def record_history(position,bors):
    i = 1 if position == 'long' else 0
    k = 0 if bors == 'buy' else 2
    history[i+k].append([candletime[-1]])
    history[i+k][-1].append(price)
def local_extremum(a): 
    c = a*2-1
    b = a-1
    if np.argmax(ohlc[-c:,1]) == b:
        localextrema[0].append([candletime[-a]])
        localextrema[0][-1].append(ohlc[-a,1])
        if localextrema[1][-1][0]:
            localextrema[2].append(abs(localextrema[0][-1][1] - localextrema[1][-1][1]))
    if np.argmin(ohlc[-c:,2]) == b:
        localextrema[1].append([candletime[-a]])
        localextrema[1][-1].append(ohlc[-a,2])
        if localextrema[0][-1][0]:
            localextrema[3].append(abs(localextrema[0][-1][1] - localextrema[1][-1][1]))



balance = [[0,0,100],[0,0,100]]
history = [[[0,0]],[[0,0]],[[0,0]],[[0,0]]]
localextrema = [[[0,0]],[[0,0]],[0],[0]]

ohlc_list = []
ohlc = np.empty((1,4))
candletime = []
lenofcandle = []
k = 0
trend = 0
losstimeL = 0
losstimeS = 0
stopbuyings = 1
stopbuyingl = 1
tradingcountS= [0,0]
tradingcountL= [0,0]

start = 0
last = 50
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
        tictime = float(daytics[1][0])
        minute = tictime//60
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
            local_extremum(10)

        ###### Here, U can write ur strategy. U have bundle of ticdata(got once) from bybit server 
            if not k > 120: continue
            movingaverage1 = np.mean(ohlc[-20:,3])
            movingaverage2 = np.mean(ohlc[-50:,3])
            movingaverage3 = np.mean(ohlc[-120:,3])
            if movingaverage1 > movingaverage2 > movingaverage3:
                if not trend == 'long' and 20<k-losstimeS:stopbuyings = 0
                trend = 'long'
            elif movingaverage1 < movingaverage2 < movingaverage3: 
                if not trend == 'short' and 20<k-losstimeL:stopbuyingl = 0
                trend = 'short'
            else: trend = 'None'
        if not k > 120: continue

        price = float(row[4])
        if balance[1][0]:
            if price < lossprice_L:
                trading('long','sell')
                record_history('long','sell')
                if price < lossprice_L : 
                    losstimeL = k
            elif price > profitprice_L:
                trading('long','sell')
                record_history('long','sell')


        if balance[0][0]:
            if lossprice_s < price or price < profitprice_s:
                trading('short','sell')
                record_history('short','sell')
                if lossprice_s < price: 
                    stopbuyings = 1
                    losstimeS = k

        #if balance[1][0] or balance[0][0]: continue
        if trend == 'long':
            if price < movingaverage1 and not balance[1][0] and not stopbuyingl:
                trading('long','buy')
                record_history('long','buy')
                profitprice_L = price*1.02
                lossprice_L = price*0.995
                Lreached = 0

        elif trend == 'short':
            if not balance[0][0] and not stopbuyings and price > movingaverage1:
                trading('short','buy')
                record_history('short','buy')
                profitprice_s = price*0.995
                lossprice_s = price*1.02
    p1 = int(100*tradingcountL[0]/(tradingcountL[0]+tradingcountL[1]))    
    p2 = int(100*tradingcountS[0]/(tradingcountS[0]+tradingcountS[1]))    
    print(h,'))',round(balance[1][2],2),'(',p1,')',round(balance[0][2],2),'(',p2,')',round(100*(float(daytics[-1][4])-float(daytics[0][4]))/float(daytics[0][4]),2))
    #tradingcountS= [0,0]
    #tradingcountL= [0,0]

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

for i in range(4): localextrema[i].pop(0)
for i, val in enumerate(localextrema[0]):
    ohlc_df.loc[val[0],'max'] = val[1] + 20
for i, val in enumerate(localextrema[1]):
    ohlc_df.loc[val[0],'min'] = val[1] - 20

k = 1 #select position u wanna see (0=short,1=long)
for i in range(4): history[i].pop(0)
for i, val in enumerate(history[k]):
    ohlc_df.loc[val[0],'buy_long'] = val[1] - 200
for i, val in enumerate(history[k+2]):
    ohlc_df.loc[val[0],'sell_long'] = val[1] + 200

ma10 = go.Scatter(x=ohlc_df.index, y=ohlc_df['ma10'], line=dict(color='black', width=0.8), name='ma20')
ma20 = go.Scatter(x=ohlc_df.index, y=ohlc_df['ma20'], line=dict(color='green', width=0.8), name='ma50')
ma50 = go.Scatter(x=ohlc_df.index, y=ohlc_df['ma50'], line=dict(color='red', width=0.8), name='ma120')
maxval = go.Scatter(x=ohlc_df.index, y=ohlc_df['max']+50, mode ="markers", marker=dict(color='green',symbol= '6'), name='Max')
minval = go.Scatter(x=ohlc_df.index, y=ohlc_df['min']-50, mode ="markers", marker=dict(color='red',symbol = '5'), name='Min')
history_SL = go.Scatter(x=ohlc_df.index, y=ohlc_df['sell_long'], mode ="markers", marker=dict(color='green',symbol= '6'), name='Sell long')
history_BL = go.Scatter(x=ohlc_df.index, y=ohlc_df['buy_long'], mode ="markers", marker=dict(color='red',symbol = '5'), name='Buy long')
candle = go.Candlestick(x=ohlc_df.index,open=ohlc_df['open'],high=ohlc_df['high'],low=ohlc_df['low'],close=ohlc_df['close'])

#fig = go.Figure(data=[candle,history_SL,history_BL,ma10,ma20,ma50])
fig = go.Figure(data=[candle,ma20,ma50,maxval,minval])
#fig.write_image("fig1.svg")
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














