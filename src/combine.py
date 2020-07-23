'''
Created on 23 Jul 2020

@author: andreas
'''

import threading, time
import pandas, numpy # pip install pandas
from pprint import pprint

import binance, bitstamp, bittrex, bitmexApi
CALLS=[binance.binanceWrapped,
       bitstamp.bitstampWrapped,
       bittrex.bittrexWrapped,
       bitmexApi.bitmexWrapped]

def call_all_exchanges_threaded(calls=CALLS, timeout=10):
    """
    multi-threaded execution of calls, waiting at most 'timeout' seconds.
    returns combined results dict.
    """
    threads, results = [], {}
    for c in calls:
        t=threading.Thread(target=c, args=(results,))
        threads.append(t)
    for t in threads:
        t.start()
        time.sleep(0.001) # call them sequentially, better printing if APIkey/secret reading goes wrong
    for t in threads:
        t.join(timeout=timeout)
    return results
        
        
def pandas_whole_table():
    pandas.set_option('display.max_columns', None)
    pandas.set_option('display.max_rows', None)
    pandas.set_option('display.width', 300)


def one_table(API_results):
    """
    pass 1:  collect all exchanges and coin names
             ignore results if friendly_name =""
    pass 2:  insert all balances into large table filled with zeroes
    finally: 'total' column
    """
    columns, coins = [], []
    for exchange, friendly_name_and_balances in API_results.items():
        for friendly_name, balances in friendly_name_and_balances.items():
            if friendly_name=="":
                continue
            column_header = exchange + " " + friendly_name # make up column title by concatenation
            columns.append(column_header)
            coins.extend( balances.keys() )
            
    coins = sorted(list(set(coins))) # make coins list unique and sort alphabetically
    #print (columns); print (coins)
    
    # empty table:
    df = pandas.DataFrame(numpy.zeros((len(coins), len(columns))), 
                          index=coins, columns=columns)
    
    for exchange, friendly_name_and_balances in API_results.items():
        for friendly_name, balances in friendly_name_and_balances.items():
            if friendly_name=="":
                continue
            column = exchange + " " + friendly_name
            for coin, balance in balances.items():
                # print(coin, balance)
                df.at[coin, column] = balance

    # sum over all columns, and resort the columns
    df["total"] = df.sum(axis=1)
    df = df [["total"] + sorted(columns)]
    return df

if __name__ == '__main__':
    results=call_all_exchanges_threaded()
    df=one_table(results)
    pandas_whole_table(); print(df)
