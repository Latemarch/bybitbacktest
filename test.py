import hmac
import json
import time
import websocket

ws_url = "wss://stream.bybit.com/realtime"

api_key = "DRxm8XPTcsmXhQV2A8"
api_secret = "ws9UYb5A4ZNS08ZSDLPEwLG2glEwQTVmeFEv"

# Generate expires.
expires = int((time.time() + 1) * 1000)

# Generate signature.
signature = str(hmac.new(
    bytes(api_secret, "utf-8"),
    bytes(f"GET/realtime{expires}", "utf-8"), digestmod="sha256"
).hexdigest())

param = "api_key={api_key}&expires={expires}&signature={signature}".format(
    api_key=api_key,
    expires=expires,
    signature=signature
)
url = ws_url + "?" + param

ws = websocket.WebSocketApp(url=url)

ws.send('{"op": "subscribe", "args": ["orderBookL2_25.BTCUSD"]}')

from time import sleep
from pybit import inverse_perpetual
ws_inverseP = inverse_perpetual.WebSocket(
    test=False,
    ping_interval=30,  # the default is 30
    ping_timeout=10,  # the default is 10
    domain="bybit"  # the default is "bybit"
)
def handle_message(msg):
    print(msg)
# To subscribe to multiple symbols,
# pass a list: ["BTCUSD", "ETHUSD"]
ws_inverseP.orderbook_25_stream(
    handle_message, "BTCUSD"
)
while True:
    sleep(1)