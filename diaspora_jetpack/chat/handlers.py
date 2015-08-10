#!/usr/bin/env python
# -*- coding: utf-8 -*-

import firenado.core
import firenado.core.websocket
import logging
import tornado.escape
import uuid
import sys
from diaspora_jetpack.handlers import JetpackHandler

# Study this https://gist.github.com/mywaiting/4643396

if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input


class ChatHandler(firenado.core.TornadoHandler):

    def get(self):
        cache = []
        if self.session.id in self.component.xmpp_manager.connections:
            cache = self.component.xmpp_manager.connections[
                self.session.id]['cache']
        self.render("jetpack:chat/demo.html", messages=cache)


class ChatSocketHandler(firenado.core.websocket.TornadoWebSocketHandler, JetpackHandler):

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
	self.init_jetpack()
        logging.basicConfig(level=logging.WARNING,
                        format='%(levelname)-8s %(message)s')
 
        self.component.xmpp_manager.create_xmpp_connection(
            self.session.id, self)
        connection = self.component.xmpp_manager.connections[self.session.id]
        #self.component.xmpp_manager.bot[
        # 'feature_mechanisms'].unencrypted_plain = False
        if connection['client'].connect(('liberdade.digital', 5222)):
            # If you do not have the dnspython library installed, you will need
            # to manually specify the name of the server if it does not match
            # the one in the JID. For example, to use Google Talk you would
            # need to use:
            #
            # if xmpp.connect(('talk.google.com', 5222)):
            #     ...
            connection['client'].process(block=False)
        connection['waiters'].add(self)

    def on_close(self):
        if self.session.id in self.component.xmpp_manager.connections:
            self.component.xmpp_manager.connections[
                self.session.id]['waiters'].remove(self)

    def update_cache(self, chat):
        connection = self.component.xmpp_manager.connections[self.session.id]
        connection['cache'].append(chat)
        if len(connection['cache']) > connection['cache_size']:
            connection['cache'] = connection[
                                      'cache'][-connection['cache_size']:]

    def send_contacts(self, contacts):
	connection = self.component.xmpp_manager.connections[self.session.id]
	for waiter in connection['waiters']:
	    try:
                waiter.write_message(contacts)
            except:
                logging.error("Error sending contacts", exc_info=True)

    def send_updates(self, chat):
        connection = self.component.xmpp_manager.connections[self.session.id]
        logging.info(
            "sending message to %d waiters", len(connection['waiters']))
        for waiter in connection['waiters']:
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
        self.component.xmpp_manager.connections[
            self.session.id]['client'].send_msg(parsed["body"])
        chat["html"] = tornado.escape.to_basestring(
            self.render_string("jetpack:chat/message.html", message=chat))

        self.update_cache(chat)
        self.send_updates(chat)

    def recieve_message(self, message):
        logging.info("got message %r", message)
        chat = {
            "id": str(uuid.uuid4()),
            "body": message,
            }
        chat["html"] = tornado.escape.to_basestring(
            self.render_string("jetpack:chat/message.html", message=chat))

        self.update_cache(chat)
        self.send_updates(chat)

