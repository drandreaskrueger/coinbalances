# coinbalances v0.5.0

pull my balances from several exchanges, serve combined table as CSV, in a simple webserver.

### dependencies
```
python3 -m venv env
source env/bin/activate
pip3 install -U pip wheel
pip3 install requests pip bitmex bitmex-ws pandas bottle
```

### API keys and secrets
Keys are added to the `auth.py` file, one by one:

    cd src
    python3 addAuth.py
    
That  `auth.py` is human readable, open it in any text editor. 

### security
All this is dangerous; anyone holding your keys, can READ your balances, and perhaps worse things can happen. Some incomplete ideas how to protect yourself:

* ONLY use READ ONLY keys for API access to your exchanges (so no trading or withdrawal can be done). The `addAuth.py` prints some hints which settings to choose when generating the keys at the exchanges.  
* `chmod 600 auth.json` = to make the file readable only for this user.

You should also read up on how to harden bottle apps. Perhaps not have it listen to 0.0.0.0 but the specific ip address, etc. - whatever you find out, please raise an issue, or make a pull request, to tell us.

### run app

    cd src
    python3 app.py
    
then open browser at http://localhost:8080/ or at your webserver's domain.

### heroku
Be VERY careful. Not sure whether I would trust heroku with my exchange keys. But I wanted to try out if I can make it work. See these instructions: [README_heroku.md](README_heroku.md). Please give feedback, and suggestions; I am new to this.

## support me
This was fun, but it also costed a bit of my precious life. Feel free to show me that you like it:

[BTC] 1N65GAaeamWLutNqfXoau8zfYFVjWzh7CU  

Contact me for other currencies. Thank you very much. 

