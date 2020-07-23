'''
Created on 23 Jul 2020

@author: andreas
'''

import os, sys
from io import StringIO

import bottle # pip3 install bottle
from bottle import route, get, template, redirect, static_file, error, run
import combine

STATIC = './static/'
# perhaps the views folder is one up:
if "src" == os.getcwd().split(os.sep)[-1]:  
    bottle.TEMPLATE_PATH.insert(0, '../views')
    STATIC = '../static/'

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


@route('/coinbalances.csv')
def csv():
    return thisIsWhereTheMagicHappens()
    # return template('csvtest', output=data)

@route('/coinbalances.pre')
def pre():
    data = thisIsWhereTheMagicHappens()
    return template('pre-csv', output=data)

@error(404)
def error404(error):
    return template('error', error_msg='404 error. Your fault, not mine. Lol.')


##################################################################

if "heroku" in os.environ.get('PYTHONHOME', ''):
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    #run(host='localhost', port=8080, debug=True)
    run(host='0.0.0.0', port=8080)

