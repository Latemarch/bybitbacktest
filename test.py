import asyncio 
import websockets
import json

import time
import hmac

api_key = "DRxm8XPTcsmXhQV2A8"
api_secret = "ws9UYb5A4ZNS08ZSDLPEwLG2glEwQTVmeFEv"
url = "wss://stream.bybit.com/realtime"

def proc_klineV2_usd(str_json):
    data_dict = json.loads(str_json);
    data_list = data_dict.get('data',0)
    if data_list == 0: # not key 'data' in string. 
        print('proc_klineV2_usd : not found data')
        return

    num_data_list = len(data_list)

    # Detecting the complete the one minute candle. 
    for data_dict_one in data_list:
        data_confirm = data_dict_one.get('confirm',0)
        if data_confirm == True: # If confirm is True, the data is the final tick for the interval. Otherwise, it is a snapshot.!!!CAUTION : Duplicated same data received.
            TimeOpen_Candle_1M_Now = data_dict_one.get('start')
            if TimeOpen_Candle_1M_Now > proc_klineV2_usd.TimeOpen_Candle_1M_Prev: # 중복데이터 제거처리. 오픈시각이 직전보다 큰것만 골라. 
                print(str(data_dict_one)) # completed the one minute candle.
                proc_klineV2_usd.TimeOpen_Candle_1M_Prev = TimeOpen_Candle_1M_Now
            

proc_klineV2_usd.TimeOpen_Candle_1M_Prev =0 # 


def processing_all_usd(str_json):

    if '"success":true' in str_json: # subscrive 한것에 대한 응답 수신된것. 
        print('response : ' + str_json);
    elif '"topic":"klineV2.1.EOSUSD"' in str_json:        
        #print(str_json)
        proc_klineV2_usd(str_json)
    else: 
        print('processing_all_usd. not supporting type : ' + str_json)

def get_args_secret(api_key, api_secrete):
        expires = str(int(round(time.time())+5000))+"000"
        _val = 'GET/realtime' + expires
        signature = str(hmac.new(bytes(api_secrete, "utf-8"), bytes(_val, "utf-8"), digestmod="sha256").hexdigest())
        auth = {}
        auth["op"] = "auth"
        auth["args"] = [api_key, expires, signature]
        args_secret = json.dumps(auth)

        return  args_secret

        
####################### for bybit Inverse .  BTCUSD, ETHUSD, EOSUSD, XRPUSD


async def my_loop_WebSocket_bybit():

    async with websockets.client.Connect("wss://stream.bybit.com/realtime") as websocket:
        await websocket.send(get_args_secret(api_key, api_secret)); # secret 
        while True:
            data_rcv_strjson = await websocket.recv()
            if 'success' in data_rcv_strjson: 
                break # exit while

        await websocket.send('{"op":"subscribe","args":["klineV2.1.BTCUSD"]}'); # candle 1minute EOSUSD

        print('entry while websocket receive for usd')
        while True: # main while. read from websocket
            data_rcv_strjson = await websocket.recv()
            #print(data_rcv_strjson)
            processing_all_usd(data_rcv_strjson)
                
              
my_loop = asyncio.get_event_loop();  
my_loop.run_until_complete(my_loop_WebSocket_bybit());
#my_loop.run_until_complete(asyncio.gather(*[my_loop_WebSocket_bybit(),my_loop_WebSocket_usdt_private_bybit(),my_loop_WebSocket_usdt_public_bybit()]));
my_loop.close();               
