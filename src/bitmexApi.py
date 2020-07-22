'''
Created on 21 Jul 2020

@author: andreas

@info If you would like to get the Available and Wallet Balance from our API, 
      you can use the /user/margin endpoint as it returns a value for both walletBalance and availableMargin.
      In the following link, your can find our official Python API connectors. 
      https://github.com/BitMEX/api-connectors/tree/master/official-ws/python
      yes but. initially worked, but then not anymore.
      
      switching to http RPC instead:

'''
from pprint import pprint
# import json
import bitmex # pip3 install bitmex
# from bitmex_websocket import BitMEXWebsocket # pip3 install bitmex-ws

import warnings

from addAuth import credentials

"""
# websockets 
# Initially it worked well, but after a dozen or so attempts it locked me out. No answers anymore.

def testing_README_ws(api_key, api_secret, call=None):
    '''
    https://github.com/BitMEX/api-connectors/blob/master/official-ws/python/README.md#quickstart
    '''
    ws = BitMEXWebsocket(endpoint="https://www.bitmex.com/api/v1", 
                         symbol="XBTUSD", api_key=api_key, api_secret=api_secret)
    pprint([m for m in dir(ws) if not m.startswith("__")])


def bitmex_funds_ws(api_key, api_secret, symbol="BTCUSD"):
    ws = BitMEXWebsocket(endpoint="https://www.bitmex.com/api/v1", 
                         symbol=symbol, api_key=api_key, api_secret=api_secret)
    print(dir(ws))
    # return ws.funds()
    return ws.funds()
"""

def bitmex_http(api_key, api_secret):
    """
    https://github.com/BitMEX/api-connectors/tree/master/official-http/python-swaggerpy#quickstart
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        client = bitmex.bitmex(test=False, api_key=api_key, api_secret=api_secret)
        
    # print(dir(client))
    # res=client.Position.Position_get(filter=json.dumps({'symbol': 'XBTUSD'})).result()
    # pprint(res)
    # res=client.User
    # pprint(dir(res))
    
    res=client.User.User_getWallet().result()
    # pprint(res)
    BTC=res[0]['amount']/100000000.0
    # print(BTC)
    return {'BTC' : BTC}
    

def bitmexWrapped(results):
    exchange_name="bitmex"
    keys=credentials(exchange_name)
    a, s = keys["API key"], keys["SECRET key"]
    # print(a), print(s)
    afn=keys["account friendly name"]
    # data = testing_README(a, s, 'balance')
    # data=bitmex_funds(a, s)
    data=bitmex_http(a, s)
    results[exchange_name] = {afn: data}


if __name__ == '__main__':
    results={}
    bitmexWrapped(results)
    pprint(results)
