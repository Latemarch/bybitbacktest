from pybit import inverse_perpetual
import time
import pandas as pd
import numpy as np
import datetime
import asyncio 
import websockets
import json
import time
import hmac

apikey = "EvW4IWaiFzWJDgFmGz"
apisec = "ctzpTH1LJcldPna4JU0WGGl8lV3yt3qtgOVt"
def get_args_secret(_api_key, _api_secrete):
        expires = str(int(round(time.time())+5000))+"000"
        _val = 'GET/realtime' + expires
        signature = str(hmac.new(bytes(_api_secrete, "utf-8"), bytes(_val, "utf-8"), digestmod="sha256").hexdigest())
        auth = {}
        auth["op"] = "auth"
        auth["args"] = [_api_key, expires, signature]
        args_secret = json.dumps(auth)
        return  args_secret

session_auth = inverse_perpetual.HTTP(
    endpoint="https://api.bybit.com",
    api_key=apikey,
    api_secret=apisec
)
active_order = session_auth.get_active_order(symbol = "BTCUSD",order_status ="New")["result"]['data']
data = active_order#['data']
if not active_order:
    print('Nothing order')
print(data)
print(len(data))
for val in data:
    print(val['side'],val['price'])


