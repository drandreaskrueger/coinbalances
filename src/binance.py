'''
Created on 23 Jul 2020

@author:    Dr Andreas Krueger 
@contact:   https://github.com/drandreaskrueger/coinbalances
@copyright: (2020) by me. 
@license:   Donation ware. Free to use, but some donation would be nice too. See README.md.

'''

from pprint import pprint
import time, hmac, hashlib
import requests # pip install requests

from authentication import credentials


def parseData(data):
    """
    e.g. kick out empty balances
    """
    nonempty = [(b['asset'].upper(), 
                 float(b['free'])+float(b['locked'])
                 ) 
                for b in data['balances'] 
                if (float(b['free']) > 0 or float(b['locked']) > 0)]
    return dict(nonempty) 


def binance_example_given_by_support(api_key, api_secret, call='account'):
    """
    from support ticket:
    For learning and communication purposes, you might check the attachment for a brief and dirty demo.
    You might want to check the line, where I signed the query string qs
    signature = hmac.new(bytes(sc,'latin-1'), msg=bytes(qs,'latin-1'), digestmod=hashlib.sha256).hexdigest().upper()
    If you have further questions, feel free to contact us at any time.
    """
    ts = lambda x: int(1000*x)
    
    base = "https://api.binance.com/api/v3/%s?" % call
    qs = "timestamp=%s"%ts(time.time()) 
    signature = hmac.new(bytes(api_secret,'latin-1'), msg=bytes(qs,'latin-1'), digestmod=hashlib.sha256).hexdigest().upper()
    h = {"X-MBX-APIKEY": api_key}
    c = requests.get(base + qs + "&signature=%s"%signature, headers=h)
    result = c.json()
    return result
    

def binanceWrapped(results, exchange_name="binance"):
    """
    The "no parameters needed" wrapped version of the balances call.
    Can later easily be stuck into a multithreaded combine thingy.
    Inserts its results in results dict. Python dicts are threadsafe.
    """
    try:
        keys=credentials(exchange_name)
        a, s = keys["API key"], keys["SECRET key"]
        # print(a), print(s)
        afn=keys["account friendly name"]
        # data = testing_README(a, s, 'balance')
        # data=bitmex_funds(a, s)
        data=parseData( binance_example_given_by_support(a, s) )
    except Exception as e:
        print ("ERROR: (%s) %s ... returning EMPTY answer instead." % (type(e), e))
        afn, data= "", {}
        
    results[exchange_name] = {afn: data}


if __name__ == '__main__':
    results={}
    binanceWrapped(results)
    pprint(results)
