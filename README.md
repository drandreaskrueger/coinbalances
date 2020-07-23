# coinbalances

pull balances from several exchanges, serve as CSV

### dependencies
```
python3 -m venv env
source env/bin/activate
pip3 install -U pip wheel
pip3 install requests pip bitmex bitmex-ws pandas
```

### API keys and secrets

    cd src
    python3 addAuth.py

### security
all this is highly dangerous; anyone getting their hands on your keys, can at least READ your balances, perhaps even worse things can happen. At least do this:

* use READ ONLY keys for API access to your exchanges! The `addAuth.py` prints some hints for that.  
* `chmod 600 auth.json` = to make the file readable only for this user. BUT that's also no real protection ...
    
### run app

    cd src
    python3 app.py
    
then open browser at http://localhost:8080/



### heroku
UNREADY. Be VERY careful. Use only READ ONLY keys!

Simpler approach: Simply run this as a heroku app, and check in your READ ONLY keys (APIkey, APIsecret) ... but then ... not a good idea, really.  
OR better approach: Extend the existing code with setting & reading environment variables in heroku, see https://devcenter.heroku.com/articles/config-vars#accessing-config-var-values-from-code (not implemented yet).

Or just run this on your own server, not on heroku. 

Still, always be very careful with your API keys. USE READ ONLY keys !