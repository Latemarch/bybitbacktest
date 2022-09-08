import numpy as np
################ bybit WebSocket example. 
import datetime
import asyncio 
import websockets
import json
import time

ohlc = np.empty((1,5))
ohlc = np.append(ohlc,[[10,10,10,10,10]],axis =0)
ohlc = np.delete(ohlc,0, axis = 0)
async def my_loop_WebSocket_bybit():
    global ohlc
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
                #print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(data['start']))))
                ohlc=np.append(ohlc,[[float(data['open']),float(data['high']),float(data['low']),float(data['close']),float(data['volume'])]],axis=0)
                #========= Trading Strategy ============#

                #========= Trading Strategy ============#
                break#confirm == True인 경우가 중복되어 나타날 수 있다. 이 경우, 앞의 값을 선택


            

##### main exec 
my_loop = asyncio.get_event_loop();  
my_loop.run_until_complete(my_loop_WebSocket_bybit()); # loop for connect to WebSocket and receive data. 
my_loop.close(); 