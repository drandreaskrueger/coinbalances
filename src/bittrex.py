'''
Created on 21 Jul 2020

@author: andreas
'''

from addAuth import AUTHFILE

import json
import hmac
import time
import hashlib
import requests
from pprint import pprint

def auth(authfile=AUTHFILE):
    """
    read all credentials
    """
    with open(authfile) as f: # if this fails, then the AUTHFILE is missing. Call addAuth.py to create it.
        d = json.load(f)
    return d

def parseData(data):
    """
    e.g. kick out empty balances
    TODO: 
    * what is available what is total
    * rename keys to standardized naming
    """
    return [d for d in data if (float(d["available"])>0 or float(d["total"])>0)] 


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
    
    data = parseData(data)
    
    return data
    
def bittrexWrapped(results):
    """
    The "no parameters needed" wrapped version of the balances call.
    Can later easily be stuck into a threaded thingy. 
    Inserts its results in results dict. Python dicts are threadsafe.
    """
    A=auth()
    exchange_name="bittrex"
    try:
        keys=A[exchange_name]
    except:
        print("credentials for '' missing from auth file. Call addAuth.py.")
    else:
        afn=keys["account friendly name"]
        a, s = keys["API key"], keys["SECRET key"]
        data=bittrexAuthenticatedCall(a, s, call="balances")
        results[exchange_name] = {afn: data}
    
if __name__ == '__main__':
    results={}
    bittrexWrapped(results)
    pprint(results)
    