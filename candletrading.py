from pybit import inverse_perpetual
import time
import pandas as pd
import numpy as np

ohlc = np.empty((1,4))
ohlc = np.append(ohlc,[[10,10,10,10]],axis =0)
ohlc = np.delete(ohlc,0, axis = 0)

session_unauth = inverse_perpetual.HTTP(endpoint="https://api.bybit.com")
ohlc_data= session_unauth.query_kline(
    symbol="BTCUSD",
    interval="1",
    from_time= str(int(time.time() - 60*100))
)
df = pd.DataFrame.from_dict(ohlc_data['result'])
df.set_index('open_time',inplace=True)
for i in range(len(df)):
    open= float(df.iloc[i]['open'])
    high= float(df.iloc[i]['high'])
    low= float(df.iloc[i]['low'])
    close= float(df.iloc[i]['close'])
    ohlc = np.append(ohlc,[[open,high,low,close]],axis=0)
print(len(ohlc))
print(df)
print(ohlc[0])
print(ohlc[-1])# [-2]까지 조사해야함. [-1]은 완성 캔들이 아님
print(time.time())

'''
opentime0 = ohlc[0]['open_time']
opentime1 = ohlc[-1]['open_time']
print(ohlc['result'][0]['open_time'])
print(ohlc['result'][-1]['open_time'])
print(type(ohlc['result'][0]['close']))
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(opentime0))))
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(opentime1))))
'''