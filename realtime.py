from pybit import inverse_perpetual
import time
import pandas as pd
import numpy as np
import datetime
import asyncio 
import websockets
import json
import time
import bybit

apikey = "DRxm8XPTcsmXhQV2A8"
apisec = "ws9UYb5A4ZNS08ZSDLPEwLG2glEwQTVmeFEv"
Order = inverse_perpetual.HTTP(
    endpoint="https://api.bybit.com",
    api_key=apikey,
    api_secret=apisec
)
def oorder(qty_):
    Order.place_active_order(
        symbol="BTCUSD",
        side="Buy",
        order_type="Market",
        qty=qty_,
        time_in_force="GoodTillCancel"
    )
oorder(1)

#Got the data past 100 mins
ohlc = np.empty((1,5))
ohlc = np.append(ohlc,[[10,10,10,10,10]],axis =0)
ohlc = np.delete(ohlc,0, axis = 0)
macd = np.empty((0))



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
    volume = float(df.iloc[i]['volume'])
    ohlc = np.append(ohlc,[[open,high,low,close,volume]],axis=0)

ohlc = np.delete(ohlc,-1, axis = 0)
ma1 = []
ma2 = []
macd_osc = []
macd = np.empty((0))
for i in range(30,0,-1):
    ma1.append(float(np.mean(ohlc[-12-i:,3])))
    ma2.append(float(np.mean(ohlc[-26-i:,3])))
    macd = np.append(macd,ma1[-1]-ma2[-1])
macd_sig = np.mean(macd[-9:])
macd_osc.append(macd[-1] - macd_sig)


#=============================
async def my_loop_WebSocket_bybit(macd,ohlc,ma1,ma2,macd_osc):
    async with websockets.connect("wss://stream.bybit.com/realtime") as websocket:
        print("Connected to bybit WebSocket")
        await websocket.send('{"op":"subscribe","args":["klineV2.1.BTCUSD"]}')
        data_rcv_response = await websocket.recv() 
        print("response for subscribe req. : " + data_rcv_response)

        while True:
            data_rcv_strjson = await websocket.recv() 
            data_rcv_dict = json.loads(data_rcv_strjson)
            data_trade_list = data_rcv_dict.get('data',0) 
            if data_trade_list == 0:
                continue
            for data_trade_dict in data_trade_list:
                if data_trade_dict['confirm'] == True:
                    print(datetime.datetime.now())
                    data = data_trade_dict
                else: continue 
                #Finding "confirm == Ture" and, once finding, following code is working but 'break' makes following code doesn't work twice in same 'data bundle' 
                #print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(data['start']))))
                ohlc=np.append(ohlc,[[float(data['open']),float(data['high']),float(data['low']),float(data['close']),float(data['volume'])]],axis=0)
                #========= Trading Strategy ============#
                ma1.append(float(np.mean(ohlc[-12-i:,3])))
                ma2.append(float(np.mean(ohlc[-26-i:,3])))
                macd = np.append(macd,ma1[-1]-ma2[-1])
                macd_sig = np.mean(macd[-9:])
                macd_osc.append(macd[-1] - macd_sig)
                p_macd0=-25.0714*(0.889*(ma1[-1]-ma2[-1]-ohlc[-12,3]/12+ohlc[-26,3]/26)-macd_sig+macd[-9]/9)
                print('Made Limit reduceonly')
                
                #========= Trading Strategy ============#
                break#prevent finding "confirm == True" in same data bundle 


            

##### main exec 
my_loop = asyncio.get_event_loop();  
my_loop.run_until_complete(my_loop_WebSocket_bybit(macd,ohlc,ma1,ma2,macd_osc)); # loop for connect to WebSocket and receive data. 
my_loop.close(); 