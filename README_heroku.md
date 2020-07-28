# coinbalances can run on heroku

### attention: Possible loss of funds or privacy ahead.
Be VERY careful. Not sure whether I would trust heroku with my exchange keys. But I wanted to try out if I can make it work. Please give feedback, and suggestions; I am new to this.

Use only READ ONLY keys! Be VERY careful. Or even better - do NOT do this. If you are a risk taker, continue, lol ... 

Probably best: Just run this on your own server, not on heroku. 

### changes for heroku
Setting & reading environment variables in heroku, see https://devcenter.heroku.com/articles/config-vars#accessing-config-var-values-from-code. I got that working.

## steps I took for heroku
Before you do this, have it sucessfully running on your local machine first, see [README.md##run-app](README.md##run-app), incl your keys etc. Only then ...
### create heroku app

Create your account at https://www.heroku.com/ the **free tier** will work for this!

Then on the commandline, inside your fork of this repo: login, create, view, add a remote to this repo, view; then push the code, and watch what they are printing.

```
heroku login --interactive
heroku create coinbalances
heroku apps
heroku git:remote -a coinbalances
git remote -v
git push heroku master
```

Then comes the clever move, so that we never have to check in the `auth.json` with your credentials anywhere - we set its contents as an environment variable.

Then just open the app, WHILE you watch the logs:
```
heroku config:set COINBALANCES_AUTH="$(cat auth.json)"

heroku open
heroku logs --tail
```

Good?

Feedback?

## support me
See bottom of [README.md](README.md).