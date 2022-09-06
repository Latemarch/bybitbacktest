import bybit
import asyncio 
import websockets
import json
import pymysql
import hmac
import time
import math
import numpy as np

'''
conn = pymysql.connect(
    host="localhost",user = "root",
    password = "ghfkddl1", db = "testdb", charset = "utf8"
)
curs = conn.cursor()
'''

apikey ='HkXvY2ig38HAGMrfHw'
apisec = 'SCbxuKuwMl94fqWPiitJzdbqPbtxBuGiRw0D'
apikeyt = 'Yy9dTzzJhz5m5oU6zl'
apisect = 'xE90RRdzJoyay9m4eSsI3KWOIiRJbrGgCZVE'
client = bybit.bybit(test = False, api_key = apikey, api_secret = apisec)

i = 0
def get_args_secret(_api_key, _api_secrete):
        expires = str(int(round(time.time())+5000))+"000"
        _val = 'GET/realtime' + expires
        signature = str(hmac.new(bytes(_api_secrete, "utf-8"), bytes(_val, "utf-8"), digestmod="sha256").hexdigest())
        auth = {}
        auth["op"] = "auth"
        auth["args"] = [_api_key, expires, signature]
        args_secret = json.dumps(auth)

        return  args_secret

def Order_Market_reduce_only(side,qty):
    return client.Order.Order_new(
        side=side,
        symbol = "BTCUSD", 
        order_type=  "Market",
        qty = qty,
        time_in_force = 'GoodTillCancel',
        reduce_only = True,
        close_on_trigger = False
    ).result()
def Order_Limit(side,price,qty,stop_loss):
    return client.Order.Order_new(
        side= side,
        symbol = "BTCUSD", 
        order_type=  "Limit",
        qty = qty,
        price = price,
        time_in_force = 'PostOnly',
        stop_loss = stop_loss,
        reduce_only = False,
        close_on_trigger = False
    ).result()
def Order_Limit_reduceonly(side,price,qty):
    return client.Order.Order_new(
        side= side,
        symbol = "BTCUSD", 
        order_type=  "Limit",
        qty = qty,
        price = price,
        time_in_force = 'PostOnly',
        reduce_only = True,
        close_on_trigger = False
    ).result()

bpoint = 0
spoint = 0


async def my_loop_WebSocket_usdt_public_bybit():
    global position
    global bbdown
    global bbup
    global safediffer
    global tic
    global bpoint
    global spoint
    global margin
    global margincut
    global ohlc
    global k
    position = client.Positions.Positions_myPosition(symbol="BTCUSD").result()[0]['result']
    size = 100 
    safe = 200 
    tic = 100 
    mass = 0
    localmaxval = []
    localminval = []
    minmax = []
    maxmin = []

    ma = 50
    ohlc_list = []
    lenofcandle = []
    std_c = []
    ohlc = np.array([[0,0,0,0]])

    safediffer = 0
    rows = []

    i = -1 
    k = 0
    async with websockets.client.Connect("wss://stream.bybit.com/realtime") as ws_usdt_public:
        print("Connected to bybit USD WebSocket Public")

        await ws_usdt_public.send('{"op": "subscribe", "args": ["trade.BTCUSD"]}')

        while True:
            data_rcv_strjson = await ws_usdt_public.recv() 
                
            data_rcv_dict = json.loads(data_rcv_strjson) # convert to Pyhton type dict 
            data = data_rcv_dict.get('data') 

            if data:
                i += len(data)
                for row in data:
                    rows.append(row)
                price = float(data[0]['price'])
                ohlc_list.append(price)
                #tictime.append(float(data[0]['trade_time_ms'])//1000)
                if i >= tic:
                    i = i - tic
                    if len(rows) >= 10000:
                        tic = min([int(200000/(float(rows[-1]['trade_time_ms'])//1000 - float(rows[-10000]['trade_time_ms'])//1000)),800])
                        rows = rows[-10000:]
                        ma = int(20*math.log(tic))
                        safe = 2*ma
                        if k < 1000:
                            k += 1
                        
                    if tic < 100:
                        if mass == 0:
                            mass = 1
                            print('STOP',time.strftime('%m-%d %I:%M:%S',time.localtime()),tic)
                    if mass == 1: 
                        if tic >= 100:
                            mass = 0
                            print('RESTART',time.strftime('%m-%d %I:%M:%S',time.localtime()),tic)
                        
                    if np.argmax(ohlc[-19:,1]) == 10:
                        localmaxval.append(ohlc[-10,1])
                        if localminval:
                            minmax.append(localmaxval[-1]-localminval[-1])
                            if len(minmax) > 5:
                                margins = sum(maxmin[-5:])/5
                    
                    if np.argmin(ohlc[-19:,2]) == 10:
                        localminval.append(ohlc[-10,2])
                        if localmaxval:
                            maxmin.append(localmaxval[-1] - localminval[-1])

                    ohlc = np.append(ohlc,[[ohlc_list[0],max(ohlc_list),min(ohlc_list),ohlc_list[-1]]],axis = 0)
                    lenofcandle.append(max(ohlc_list)-min(ohlc_list))
                    lenofcandle = lenofcandle[-ma:]
                    ohlc_list = []
                    if k >= ma:
                        candlestd = np.array(lenofcandle)
                        std_c.append(np.mean(candlestd))
                        std_c = std_c[-ma:]
                        aa = np.array(std_c)
                        aam = np.mean(aa)
                        mean   = np.mean(ohlc[-ma:,3])
                        std_p  = np.std(ohlc[-ma:,3])
                        width = std_p*std_c[-1]/aam
                        bbup   = mean + 1.5*width
                        bbdown = mean - 1.5*width
                        bbups   = mean + 1.5*width
                        bbdowns = mean - 1.5*width
                    if k < safe:
                        print(time.strftime('%m-%d %I:%M:%S',time.localtime()),k, tic)
                    if k > safe:
                        ohlc = ohlc[-1000:]

                        safediffer = np.mean(ohlc[-safe:,3]) - np.mean(ohlc[-safe-1:-2,3])
                        Order = client.Order.Order_cancelAll(symbol = 'BTCUSD').result()


                        if position['side'] == 'None': 
                            if tic > 99:
                                if safediffer > 0:
                                    Order = Order_Limit('Buy', int(bbdown), size, int(bbdown*0.99335))
                                if safediffer < 0:
                                    Order = Order_Limit('Sell', int(bbup), size, int(bbup*1.00665))

                        elif position['side'] == 'Buy':
                            if safediffer < 0:
                                Order = Order_Limit_reduceonly('Sell', price + 0.5 , position['size'])
                                if tic > 99:
                                    Order = Order_Limit('Sell', int(bbup), size, int(bbup*1.00665))
                            else:
                                Order = Order_Limit_reduceonly('Sell', int(min([bbups,float(position['entry_price'])*1.009])), position['size'])
                        else:
                            if safediffer > 0:
                                Order = Order_Limit_reduceonly('Buy', price - 0.5 , position['size'])
                                if tic > 99:
                                    Order = Order_Limit('Buy', int(bbdown), size, int(bbdown*0.99335))
                            else:
                                Order = Order_Limit_reduceonly('Buy', int(max([bbdowns,float(position['entry_price'])*0.991])), position['size'])
                                if Order[0]['ret_code']:#
                                    print(Order[0]['ret_code'])

                                
                        



async def my_loop_WebSocket_usdt_private_bybit():
    global position
    global tic
    global bpoint
    global spoint
    async with websockets.client.Connect("wss://stream.bybit.com/realtime") as ws_usdt_private:
        await ws_usdt_private.send(get_args_secret(apikey, apisec)) # secret 
        await ws_usdt_private.send('{"op": "subscribe", "args": ["execution"]}')
        print("Connected to bybit USD WebSocket Private with secret key")

        while True:
            data_rcv_strjson = await ws_usdt_private.recv()
            data_rcv_dict = json.loads(data_rcv_strjson) # convert to Pyhton type dict 
            data = data_rcv_dict.get('data') 
            if data:
                position = client.Positions.Positions_myPosition(symbol="BTCUSD").result()[0]['result']
                print('side',position['side'],tic)
                print('sise',position['size'])
                print('price',position['entry_price'])
                
            

try:
    my_loop = asyncio.get_event_loop()  
    my_loop.run_until_complete(asyncio.gather(*[my_loop_WebSocket_usdt_private_bybit(),
                                                my_loop_WebSocket_usdt_public_bybit()
                                                ]))
    my_loop.close() 
except:
    time.sleep(20)

    my_loop = asyncio.get_event_loop()  
    my_loop.run_until_complete(asyncio.gather(*[my_loop_WebSocket_usdt_private_bybit(),
                                                my_loop_WebSocket_usdt_public_bybit()
                                                ]))
    my_loop.close() 