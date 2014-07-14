# -*- coding: utf-8 -*-
import irc.bot
import irc.strings
import re
import urllib2
import htmlentitydefs
from threading import *
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from BeautifulSoup import BeautifulSoup
import os
import sys
import datetime
import time
import config


class Sender(object):

    def __init__(self, urlbot, c, url, senderId, at_time):
        self.thread = Thread(target=self.process)
        self.url = url
        self.urlbot = urlbot
        self.at_time = at_time
        self.senderId = senderId
        self.title_length = 300
        self.max_page_size = 1048576
        self.c = c

    def start(self):
        self.thread.start()

    def join(self):
        self.thread.join()

    def test(self):
        return self.thread.is_alive()

    def process(self):
        while time.time() < self.at_time:
            time.sleep(1)
        print("process %r" % self.url)
        try:
            soup = BeautifulSoup(
                urllib2.urlopen(
                    self.url).read(
                    self.max_page_size))
        except urllib2.HTTPError as e:
            print("HTTPError when fetching %s : %s\n" % (e.url, e))
            return
        if not soup.title:
            return
        if len(soup.title.string) > self.title_length:
            title = soup.title.string[0:self.title_length] + u'…'
        else:
            title = soup.title.string
            self.urlbot.say(
                self.c,
                self.senderId +
                "'s url : [ " +
                title.strip() +
                " ]")


class Bot(irc.bot.SingleServerIRCBot):

    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(
            self, [
                (server, port)], nickname, nickname)
        self.channel = channel
        self.url_regexp = re.compile(
            """((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""")

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        idName = e.source.nick
        data = e.arguments[0]
        for url in re.findall(self.url_regexp, data):
            url = url[0]
            if not url.startswith('http'):
                url = 'http://'+url
            url = url.encode('utf-8')
            Sender(self, c, url, idName, 1).start()

    def say(self, c, msg):
        c.privmsg(self.channel, msg)


def main():
    channel = config.channel
    nickname = config.nickname
    server = config.server
    port = config.port
    bot = Bot(channel, nickname, server, port)
    bot.start()

if __name__ == '__main__':
    main()
