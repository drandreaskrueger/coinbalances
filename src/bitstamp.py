'''
Created on 21 Jul 2020

@author: andreas
'''

import hashlib
import hmac
import time
import requests
import uuid
import sys
from urllib.parse import urlencode

from pprint import pprint

# if sys.version_info.major >= 3:
#    from urllib.parse import urlencode
#else:
#    from urllib import urlencode

from addAuth import credentials

# def bitstampCall(api_key = 'api_key', API_SECRET = b'api_key_secret'):
def bitstampCall(api_key = 'api_key', api_secret = 'api_secret', call='user_transactions'):
    """
    Authentication examples:
    https://www.bitstamp.net/api/#error-code-example
    and then modified by me
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
    

def bitstampWrapped(results):
    exchange_name="bitstamp"
    keys=credentials(exchange_name)
    a, s = keys["API key"], keys["SECRET key"]
    afn=keys["account friendly name"]
        
    data = bitstampCall(a, s, 'balance')
    results[exchange_name] = {afn: data}
    

if __name__ == '__main__':
    results={}
    bitstampWrapped(results)
    pprint(results)