'''
Created on 23 Jul 2020

@author:    Dr Andreas Krueger 
@contact:   https://github.com/drandreaskrueger/coinbalances
@copyright: (2020) by me. 
@license:   Donation ware. Free to use, but some donation would be nice too. See README.md.

'''

import os, sys, datetime
from io import StringIO

import pandas, bottle # pip3 install pandas bottle
from bottle import route, get, template, redirect, static_file, error, run
import combine

STATIC = './static/'
# perhaps the views & static folder are one up:
if "src" == os.getcwd().split(os.sep)[-1]:  
    bottle.TEMPLATE_PATH.insert(0, '../views')
    STATIC = '../static/'


# the routes for the bottle webserver app:

@route('/home')
def show_home():
    return template('home')

@route('/')
def handle_root_url():
    redirect('/home')

@get('/favicon.ico')
def get_favicon():
    return static_file('favicon.ico', root=STATIC)
    

def thisIsWhereTheMagicHappens():
    """
    The combined CSV is the result in a good case.
    Error messages and other output in a bad case.
    """

    # in case anything goes wrong, we want to see the errors instead of the CSV:
    logging=""
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    
    try:
        results = combine.call_all_exchanges_threaded()
        #results = combine.call_all_exchanges_threaded(causeTrouble=True)
        df = combine.one_table(results)
        data = df.to_csv()
        logging = mystdout.getvalue()

    except Exception as e:
        msg = "ERROR: %s %s" % (type(e), e)
        data = msg + "\n" + mystdout.getvalue()
        data = data.replace("<", "").replace(">", "")

    sys.stdout = old_stdout
    if logging:
        print (logging)
    return data

def example_data(inputfile=os.path.join("..", "examples", "coinbalances.csv" )):
    """
    only used once, to generate the files in the examples folder
    """
    with open(inputfile, "r") as f:
        data = f.read()
    df = pandas.read_csv(StringIO(data))
    df['total'] = df.drop('total', axis=1). sum(axis=1) # recalculate row sum
    data = df.to_csv(index=False)
    return data
# thisIsWhereTheMagicHappens=example_data


@route('/coinbalances.csv')
def csv():
    return thisIsWhereTheMagicHappens()

def timestring():
    """
    16 letters datetime string
    """
    dt = datetime.datetime.now()
    dtstr=("%s" % dt)[:16]
    return dtstr

@route('/coinbalances.pre')
def pre():
    data = thisIsWhereTheMagicHappens()
    return template('pre-csv', output=data, ts=timestring())

@route('/coinbalances.table')
def table():
    """
    HTML table, with a bit of formatting.
    So many zeroes --> make them have less contrast.  
    """
    data = thisIsWhereTheMagicHappens()
    df = pandas.read_csv(StringIO(data)) 
    ff=lambda x : "%.8f" % x
    ht=df.to_html(border=1, classes="tableformat", # layout 
                  justify='center', # headings 
                  float_format=ff, # right align with 8 digits
                  index=False) # drop index from dataframe
    html_string = template('html-table', output=ht, ts=timestring())
    # make zeros silver gray:
    html_with_zeros_grayed = html_string.replace("<td>0.00000000", '<td class="zero">0.00000000')
    return html_with_zeros_grayed 
    

@error(404)
def error404(error):
    return template('error', error_msg='404 error. Your fault, not mine. Lol.')


##################################################################

if "heroku" in os.environ.get('PYTHONHOME', ''):
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    #run(host='localhost', port=8080, debug=True)
    run(host='0.0.0.0', port=8080)

