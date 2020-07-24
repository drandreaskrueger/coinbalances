'''
Created on 21 Jul 2020

@author:    Dr Andreas Krueger 
@contact:   https://github.com/drandreaskrueger/coinbalances
@copyright: (2020) by me. 
@license:   Donation ware. Free to use, but some donation would be nice too. See README.md.

'''

import hashlib
import hmac
import time
import requests # pip3 install requests
import uuid
from urllib.parse import urlencode
from pprint import pprint

# python 2 is dead, but just in case:
# if sys.version_info.major >= 3:
#    from urllib.parse import urlencode
#else:
#    from urllib import urlencode

from authentication import credentials


def parseData(data):
    """
    takes in exchange answer, selects the *_balance entries, shortens the name, and returns as dict
    """
    balances = dict([(n.split("_")[0].upper(), 
                      b) 
                     for n, b in data.items() 
                     if n.endswith("_balance")])
    return balances


def bitstampCall(api_key = 'api_key', api_secret = 'api_secret', call='user_transactions'):
    """
    Authentication examples:
        https://www.bitstamp.net/api/#error-code-example
    and then modified a little bit by me; already gave them feedback how to simplify this a bit.
    """
    
    API_SECRET=api_secret.encode('UTF-8') # turn string to bytes, for hmac.new(API_SECRET, ...) function
    
    timestamp = str(int(round(time.time() * 1000)))
    nonce = str(uuid.uuid4())
    content_type = 'application/x-www-form-urlencoded'
    payload = {'offset': '1'}
    
    payload_string = urlencode(payload)

    # '' (empty string) in message represents any query parameters or an empty string in case there are none
    message = 'BITSTAMP ' + api_key + \
        'POST' + \
        'www.bitstamp.net' + \
        '/api/v2/%s/' % call + \
        '' + \
        content_type + \
        nonce + \
        timestamp + \
        'v2' + \
        payload_string
        
    message = message.encode('utf-8')
    
    signature = hmac.new(API_SECRET, msg=message, digestmod=hashlib.sha256).hexdigest()
    headers = {
        'X-Auth': 'BITSTAMP ' + api_key,
        'X-Auth-Signature': signature,
        'X-Auth-Nonce': nonce,
        'X-Auth-Timestamp': timestamp,
        'X-Auth-Version': 'v2',
        'Content-Type': content_type
    }
    r = requests.post(
        'https://www.bitstamp.net/api/v2/%s/' % call,
        headers=headers,
        data=payload_string
        )
    if not r.status_code == 200:
        raise Exception('Status code not 200')
    
    string_to_sign = (nonce + timestamp + r.headers.get('Content-Type')).encode('utf-8') + r.content
    signature_check = hmac.new(API_SECRET, msg=string_to_sign, digestmod=hashlib.sha256).hexdigest()
    if not r.headers.get('X-Server-Auth-Signature') == signature_check:
        raise Exception('Signatures do not match')
    
    # return r.content
    # return r.content.decode('UTF-8')
    return r.json()
    

def bitstampWrapped(results, exchange_name="bitstamp"):
    """
    The "no parameters needed" wrapped version of the balances call.
    Can later easily be stuck into a multithreaded combine thingy.
    Inserts its results in results dict. Python dicts are threadsafe.
    """
    try:
        keys=credentials(exchange_name)
        a, s = keys["API key"], keys["SECRET key"]
        afn=keys["account friendly name"]
            
        data = parseData ( bitstampCall(a, s, 'balance') )
    except Exception as e:
        print ("ERROR: (%s) %s ... returning EMPTY answer instead." % (type(e), e))
        afn, data= "", {}
    results[exchange_name] = {afn: data}
    

if __name__ == '__main__':
    results={}
    bitstampWrapped(results)
    pprint(results)
    
    