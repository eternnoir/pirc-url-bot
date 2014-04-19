# -*- coding: utf-8 -*-
import irc.bot
import irc.strings
import re
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from BeautifulSoup import BeautifulSoup

class Sender(object):
    def __init__(self, urlbot, to, url,senderId, at_time):
        self.thread = Thread(target=self.process)
        self.to = to
        self.url = url
        self.urlbot=urlbot
        self.at_time=at_time
        self.senderId = senderId

    def start(self):
        self.thread.start()

    def join(self):
        self.thread.join()

    def test(self):
        return self.thread.is_alive()

    def process(self):
        while time.time() < self.at_time:
            time.sleep(1)
        myprint("process %r" % self.url)
        try:
            soup = BeautifulSoup(urllib2.urlopen(self.url).read(self.urlbot.max_page_size))
        except urllib2.HTTPError as e:
            sys.stderr.write("HTTPError when fetching %s : %s\n" % (e.url, e))
            return
        if not soup.title:
            return
        if len(soup.title.string) > self.urlbot.title_length:
            title=soup.title.string[0:self.urlbot.title_length] + u'…'
        else:
            title=soup.title.string
            self.urlbot.say(self.to, self.senderId+"'s url : [ "+ html_entity_decode(title.replace('\n', ' ').strip())+" ]")

class Bot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.url_regexp=re.compile("""((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""")

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        print e.source.nick
        data = e.arguments[0]
        for url in re.findall(self.url_regexp, data):
            url=url[0]
            if not url.startswith('http'):
                url='http://'+url
            print url
            #Sender(self, to, url,idName, self.last_message).start()


    def say(self,c,msg):
        c.privmsg(self.channel,msg)

def main():
    channel= '#CS_RDSS'
    nickname= 'urlBot2'
    server='chat.freenode.net'
    bot = Bot(channel, nickname, server)
    bot.start()

if __name__ == '__main__' :
    main()
