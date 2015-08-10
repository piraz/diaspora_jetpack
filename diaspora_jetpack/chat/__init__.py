import diaspora_jetpack.chat.handlers
import firenado.core
import sleekxmpp


class PubSubXmppClient(sleekxmpp.ClientXMPP):
    def __init__(self, handler):
	#print handler.shared_session.get('diaspora_session:%s' % self.validation_token_key
        sleekxmpp.ClientXMPP.__init__(self, "", "")
        self.register_plugin('xep_0030')  # Service Discovery
        #self.register_plugin('xep_0004')  # Data Forms
        #self.register_plugin('xep_0060')  # PubSub
        self.register_plugin('xep_0199')  # XMPP Ping
        self.recipient = ""
        self.chat_handler = handler
        self.add_event_handler("session_start", self.start, threaded=True)
        self.add_event_handler("message", self.recv_message)

    #'presence_available'
    #'presence_dnd'
    #'presence_xa',
    #'presence_chat',
    #'presence_away',
    #'presence_unavailable',
    #'presence_subscribe',
    #'presence_subscribed',
    #'presence_unsubscribe',
    #'presence_unsubscribed',
    #'roster_subscription_request',
    def start(self, event):
        self.send_presence()
        self.get_roster(block=False, callback=self.update_roster)

    def recv_message(self, msg):
        # You'll probably want to ignore error and headline messages.
        # If you want to handle group chat messages, add 'groupchat'
        # to the list.
        if msg['type'] in ('chat', 'normal'):
            self.chat_handler.recieve_message("%s says: %s" % (
                msg['from'], msg['body']))

    def send_msg(self, msg):
        self.send_message(mto=self.recipient,
                          mbody=msg,
                          mtype='chat')

    def update_roster(self, iq):
	self._handle_roster(iq)
	data = {'type': 'contacts', 'contacts':[]}
        for key in self.client_roster.keys():
            print self.client_roster[key]
            if self.client_roster[key]['name']!='':
		self.send_presence(pto=key, ptype='subscribe')
                print self.client_roster[key]
                contact = {}
                contact['id'] = key
                contact['name'] = self.client_roster[key]['name']
                contact['groups'] = self.client_roster[key]['groups']
                contact['online'] = False
                data['contacts'].append(contact)

        #    print roster
        #print self.client_roster
        self.chat_handler.send_contacts(data)


class XmppManager(object):

    def __init__(self):
        self.connections = {}

    def create_xmpp_connection(self, session_id, handler):
        self.connections[session_id] = {}
        self.connections[session_id]['client'] = PubSubXmppClient(handler)
        self.connections[session_id]['waiters'] = set()
        self.connections[session_id]['cache'] = []
        self.connections[session_id]['cache_size'] = 200


class DiasporaJetpackChatComponent(firenado.core.TornadoComponent):

    def __init__(self, name, application, config={}):
        self.xmpp_manager = XmppManager()
        super(DiasporaJetpackChatComponent, self).__init__(
            name, application, config)

    def get_handlers(self):
        return [
            (r'/jetpack/chat', diaspora_jetpack.chat.handlers.ChatHandler),
            (r"/jetpack/chat/chatsocket",
                diaspora_jetpack.chat.handlers.ChatSocketHandler),
        ]

    def shutdown(self):
        print "Disconecting connections..."
        for session_id, connection in \
                self.xmpp_manager.connections.iteritems():
            print "Closing connection from session %s." % session_id
            print connection
            connection['client'].disconnect(wait=True)

