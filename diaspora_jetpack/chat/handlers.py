#!/usr/bin/env python
# -*- coding: utf-8 -*-

import firenado.core
import logging
import tornado.escape
import uuid

import firenado.core.websocket

import sys
import getpass
import sleekxmpp

# Study this https://gist.github.com/mywaiting/4643396

if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input


class SendMsgBot(sleekxmpp.ClientXMPP):
    def __init__(self, handler):
        sleekxmpp.ClientXMPP.__init__(self, "", "")
        self.recipient = "radiovox@liberdade.digital"
        self.chat_hander = handler
        self.add_event_handler("session_start", self.start, threaded=True)
        self.add_event_handler("message", self.recv_message)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def recv_message(self, msg):
        # You'll probably want to ignore error and headline messages.
        # If you want to handle group chat messages, add 'groupchat' to the list.
        if msg['type'] in ('chat', 'normal'):
            self.chat_hander.recieve_message("%s says: %s" % (msg['from'], msg['body']))

    def send_msg(self, msg):
        self.send_message(mto=self.recipient,
                          mbody=msg,
                          mtype='chat')


class ChatHandler(firenado.core.TornadoHandler):

    def get(self):
        self.render("jetpack:chat/index.html", messages=ChatSocketHandler.cache)


class ChatSocketHandler(firenado.core.websocket.TornadoWebSocketHandler):

    waiters = set()
    cache = []
    cache_size = 200

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        logging.basicConfig(level=7,
                        format='%(levelname)-8s %(message)s')

        self.bot = SendMsgBot(self)
        #self.bot['feature_mechanisms'].unencrypted_plain = False
        self.bot.register_plugin('xep_0030')  # Service Discovery
        self.bot.register_plugin('xep_0004')  # Data Forms
        self.bot.register_plugin('xep_0060')  # PubSub
        self.bot.register_plugin('xep_0199')  # XMPP Ping
        if self.bot.connect(('liberdade.digital', 5222)):
            # If you do not have the dnspython library installed, you will need
            # to manually specify the name of the server if it does not match
            # the one in the JID. For example, to use Google Talk you would
            # need to use:
            #
            # if xmpp.connect(('talk.google.com', 5222)):
            #     ...
            self.bot.process(block=False)
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        ChatSocketHandler.waiters.remove(self)

    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    @classmethod
    def send_updates(cls, chat):
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        chat = {
            "id": str(uuid.uuid4()),
            "body": parsed["body"],
            }
        self.bot.send_msg(parsed["body"])
        chat["html"] = tornado.escape.to_basestring(
            self.render_string("jetpack:chat/message.html", message=chat))

        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)

    def recieve_message(self, message):
        logging.info("got message %r", message)
        chat = {
            "id": str(uuid.uuid4()),
            "body": message,
            }
        chat["html"] = tornado.escape.to_basestring(
            self.render_string("jetpack:chat/message.html", message=chat))

        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)