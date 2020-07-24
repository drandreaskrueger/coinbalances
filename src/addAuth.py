'''
Created on 21 Jul 2020

@author: andreas

@TODO: (not my problem but) if there are several accounts at the same exchange, 
       turn the dict into a list, 
       or use the 'account friendly name' as main key of the dict.
'''

import os, json
from pprint import pprint
AUTH_ENV="COINBALANCES_AUTH" # this overrides the following file
AUTH_FILE=os.path.join("..", "auth.json") # only read if AUTH_ENV doesn't exist.

############################################
# read access:
# EITHER environment variable OR auth file
############################################

def credentials(exchange_name=None, env_variable=AUTH_ENV, authfile=AUTH_FILE):
    """
    first try environment variable, only if that is not set, read file.
    
    read all credentials, return all of them, or only for one exchange 
    """
    j = os.getenv(env_variable)
    print (j); 
    k =  os.getenv(env_variable+"x")
    print(k)
    
    return j
    
    try:
        with open(authfile) as f:
            A = json.load(f)
        if not exchange_name:
            keys=A
        else:
            keys=A[exchange_name]
    except:
        msg="credentials for '%s' missing from auth file / env variable, or there is no auth file / variable. Call addAuth.py." % exchange_name
        raise Exception(msg)
    
    return keys


###########################
# all this is file based:

def printURLs():
    """
    printed when adding new creds
    """
    exchanges={"bitstamp": {"keys": "https://www.bitstamp.net/account/security/api/",
                            "rights suggested" : "Account balance, User transactions",
                            "API infos" : "https://www.bitstamp.net/api/"},
               "bittrex" : {"keys": "https://global.bittrex.com/Manage?view=api",
                            "rights suggested": "READ INFO yes, TRADE no, WITHDRAW no",
                            "API infos" : "https://bittrex.github.io/api/v3"},
               "bitmex" : {"API infos" : "https://www.bitmexApi.com/api/explorer/#!/User/User_getWallet",
                           "keys" : "https://www.bitmexApi.com/app/apiKeys",
                           "rights suggested" : "- (read only)"},
               "binance" : {"keys" : "https://www.binance.com/en/usercenter/settings/api-management",
                            "rights suggested": "Edit restrictions ... DISABLE Enable Trading ... Save",
                            "API infos": "https://binance-docs.github.io/apidocs/spot/en/#query-open-oco-user_data"},
               }
    
    print("create READ ONLY keys in these places:")
    pprint(exchanges, width=100)
    print()
    return exchanges

def loadOrNew(authfile):
    try:
        with open(authfile) as f:
            d = json.load(f)
    except Exception as e:
        print("Assuming empty config, because encountered error (%s) %s" % (type(e), e))
        print("(Interrupt now, if you don't want to start new. Or continue, by answering 3 questions per exchange)")
        d={}
    else:
        print("Loaded %d exchanges: %s" % (len(d.keys()), list(d.keys())))
        
    return d


def ask():
    """
    none of the answers is allowed to be empty
    """
    
    answer = ""
    while not answer:
        answer = input("exchange name: ")
    exchange_name = answer 
    
    keys=[]
    for q in ("API key", "SECRET key", "account friendly name"):
        answer=""
        while not answer:
            answer = input("%s: " % q)
        keys.append((q, answer))
       
    return exchange_name, keys


def writeAndFeedback(d, authfile):
    with open(authfile, "w") as f:
        json.dump(d, f)
        
    print("Written %d entries to file: %s" % (len(d), authfile))


def askAndAddOne(authfile=AUTH_FILE):

    d = loadOrNew(authfile)
    
    print ("Tell me details about one new exchange, and I will append them to the '%s' conf file." % authfile)
    print()
    exchange_name, keys = ask()
    d[exchange_name] = dict(keys)
    # pprint(d)
    
    writeAndFeedback(d, authfile)
    print("Repeat with the next one, if you want to.")



if __name__ == '__main__':
    c=credentials(exchange_name="bittrex"); print(c); exit()
    
    printURLs()
    askAndAddOne()
    
    