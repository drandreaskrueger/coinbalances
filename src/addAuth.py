'''
Created on 21 Jul 2020

@author: andreas

@TODO: (not my problem but) if there are several accounts at the same exchange, 
       turn the dict into a list, or use the 'account friendly name' as main key.
'''

import os, json
from pprint import pprint
AUTHFILE=os.path.join("..", "auth.json")

def printURLs():
    createKeys={"bitstamp": "https://www.bitstamp.net/account/security/api/",
                "bittrex" : "https://global.bittrex.com/Manage?view=api"}
    print("create READ ONLY keys in these places:")
    pprint(createKeys)
    print()

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
    exchange_name = input("exchange name: ")
    keys=[]
    for q in ("API key", "SECRET key", "account friendly name"):
        keys.append((q, input("%s: " % q)))
       
    return exchange_name, keys


def writeAndFeedback(d, authfile):
    with open(authfile, "w") as f:
        json.dump(d, f)
        
    print("Written %d entries to file: %s" % (len(d), authfile))


def askAndAddOne(authfile=AUTHFILE):

    d = loadOrNew(authfile)
    
    print ("Tell me details about one new exchange, and I will append them to the '%s' conf file." % authfile)
    exchange_name, keys = ask()
    d[exchange_name] = dict(keys)
    # pprint(d)
    
    writeAndFeedback(d, authfile)
    print("Repeat with the next one, if you want to.")


def credentials(exchange_name=None, authfile=AUTHFILE):
    """
    read all credentials, return all of them, or only for one exchange 
    """
    try:
        with open(authfile) as f:
            A = json.load(f)
        if not exchange_name:
            keys=A
        else:
            keys=A[exchange_name]
    except:
        msg="credentials for '%s' missing from auth file, or no auth file. Call addAuth.py." % exchange_name
        raise Exception(msg)
    
    return keys


if __name__ == '__main__':
    printURLs()
    askAndAddOne()
    
    