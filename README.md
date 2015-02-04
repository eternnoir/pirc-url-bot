pirc-url-bot
============

The Irc url bot write by python

## How to install

Clone repo from github.
```
$ git clone git@github.com:eternnoir/pirc-url-bot.git
```

Install package use pip
```
$  pip install -r /src/requirements.txt
```

Run
```
$ python urlBot.py -c "CHANNEL" -n "NICK NAME" -P "PORT" -s "IRCHOST"
```

## Run on Docker
```
$ docker run -it -d -e HOST=irc_host_ip -e PORT=port -e CHANNEL=channelName -e NICK=botNickName eternnoir/pirc-url-bot
```
