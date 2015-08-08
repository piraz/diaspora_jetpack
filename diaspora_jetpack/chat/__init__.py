import diaspora_jetpack.chat.handlers
import firenado.core
import sleekxmpp


class PubSubXmppClient(sleekxmpp.ClientXMPP):
    def __init__(self, handler):
        sleekxmpp.ClientXMPP.__init__(self, "", "")
        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0004')  # Data Forms
        self.register_plugin('xep_0060')  # PubSub
        self.register_plugin('xep_0199')  # XMPP Ping
        self.recipient = ""
        self.chat_hander = handler
        self.add_event_handler("session_start", self.start, threaded=True)
        self.add_event_handler("message", self.recv_message)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def recv_message(self, msg):
        # You'll probably want to ignore error and headline messages.
        # If you want to handle group chat messages, add 'groupchat'
        # to the list.
        if msg['type'] in ('chat', 'normal'):
            self.chat_hander.recieve_message("%s says: %s" % (
                msg['from'], msg['body']))

    def send_msg(self, msg):
        self.send_message(mto=self.recipient,
                          mbody=msg,
                          mtype='chat')


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
            (r"/jetpack/chatsocket",
                diaspora_jetpack.chat.handlers.ChatSocketHandler),
        ]

    def shutdown(self):
        print "Disconecting connections..."
        for session_id, connection in \
                self.xmpp_manager.connections.iteritems():
            print "Closing connection from session %s." % session_id
            print connection
            connection['client'].disconnect(wait=True)
