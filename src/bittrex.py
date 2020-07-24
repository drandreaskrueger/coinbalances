'''
Created on 21 Jul 2020

@author: andreas
'''

import json
import hmac
import time
import hashlib
import requests
from pprint import pprint

from authentication import credentials

def parseData(data):
    """
    e.g. kick out empty balances
    TODO: 
    * what is available what is total
    * rename keys to standardized naming
    """
    return dict([(b['currencySymbol'], float(b['total'])) 
                 for b in data 
                 if (float(b["available"])>0 or float(b["total"])>0)]) 


def bittrexAuthenticatedCall(apiKey, apiSecret, call="orders", method = "GET", timeout=10):
    """
    bittrex support: We do not offer an official python wrapper, 
    but here is some example code for an authenticated GET request. 
    
    Then modified by me.
    """
    timestamp = str(round(time.time()*1000))
    payload = ""
    contentHash = hashlib.sha512(payload.encode()).hexdigest()
    
    subaccountId = "" 
    uri = 'https://api.bittrex.com/v3/%s/' % call
    
    array = [timestamp, uri, method, contentHash, subaccountId]
    s= '' # no separator !
    preSign = s.join(str(v) for v in array)
    # print(preSign)
    signature = hmac.new(apiSecret.encode(), preSign.encode(), hashlib.sha512).hexdigest()
    
    header = {
        'Accept':'application/json',
        'Api-Key':apiKey,
        'Api-Timestamp':timestamp,
        'Api-Content-Hash':contentHash,
        'Api-Signature':signature,
        'Content-Type':'application/json'
    }
    
    data = requests.get(uri,data = payload, headers = header,timeout=timeout).json()
    
    return data
    
def bittrexWrapped(results):
    """
    The "no parameters needed" wrapped version of the balances call.
    Can later easily be stuck into a combine thingy. 
    Inserts its results in results dict. Python dicts are threadsafe.
    """
    exchange_name="bittrex"
    try:
        
        keys=credentials(exchange_name)
        
        afn=keys["account friendly name"]
        a, s = keys["API key"], keys["SECRET key"]
        data = parseData( bittrexAuthenticatedCall(a, s, call="balances") )
    except Exception as e:
        print ("ERROR: (%s) %s ... returning EMPTY answer instead." % (type(e), e))
        afn, data= "", {}
    results[exchange_name] = {afn: data}
    
if __name__ == '__main__':
    results={}
    bittrexWrapped(results)
    pprint(results)
    