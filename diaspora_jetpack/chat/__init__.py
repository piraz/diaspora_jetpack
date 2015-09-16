import diaspora_jetpack.chat.handlers
import firenado.core
import sleekxmpp
import logging

#https://gist.github.com/marianoguerra/4023941

logger = logging.getLogger(__name__)

OFFLINE = 'OFFLINE'
ONLINE = 'ONLINE'


class PubSubXmppClient(sleekxmpp.ClientXMPP):

    def __init__(self, handler):
        self.contacts = {}
        self.use_tls = False

        #print handler.shared_session.get('diaspora_session:%s'
        # % self.validation_token_key
        # TODO: get diaspora user data from redis session
        user = handler.component.conf['user']
        password = handler.component.conf['pass']
        logger.info("Initializing xmpp client for user %s with password "
                    "[******]" % user)
        sleekxmpp.ClientXMPP.__init__(self, user, password)
        self.register_plugin('xep_0030')  # Service Discovery
        #self.register_plugin('xep_0004')  # Data Forms
        #self.register_plugin('xep_0060')  # PubSub
        self.register_plugin('xep_0199')  # XMPP Ping
        self.recipient = ""
        self.chat_handler = handler
        # See https://github.com/fritzy/SleekXMPP/wiki/Event-Index
        self.add_event_handler("session_start", self.start, threaded=True)
        self.add_event_handler("message", self.recv_message)
        self.add_event_handler("got_online", self.got_online)
        self.add_event_handler("roster_update", self.update_roster)
        #self.add_event_handler("changed_status", self.recv_presence)

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
        logger.debug("Starting xmpp session...")
        self.send_presence()
        self.get_roster(block=False)

    def recv_message(self, msg):
        # You'll probably want to ignore error and headline messages.
        # If you want to handle group chat messages, add 'groupchat'
        # to the list.
        if msg['type'] in ('chat', 'normal'):
            self.chat_handler.recieve_message("%s says: %s" % (
                msg['from'], msg['body']))

    def got_online(self, presence):
        print presence['jid']
        print 'Got ONLINE: %s' % presence

    #def recv_presence(self, presence):
        #print presence

    def send_msg(self, msg):
        self.send_message(mto=self.recipient,
                          mbody=msg,
                          mtype='chat')

    def create_contact(self, jid, online=False):
        self.contacts[jid] = {
            'id': jid,
            'name': 'A name',
            'groups': {},
            'online': online,
            'status': 'A status',
        }

    def update_roster(self, response):
        print "\n\n\n\n*****************************************************" \
              "*************"
        print 'Recieved roster'
        print 'id: %s' % response['id']
        print 'from: %s' % response['from']
        print 'to: %s' % response['to']
        print 'type %s' % response['type']
        print 'query: %s' % response['query']
        print 'lang: %s' % response['lang']

        data = {'type': 'contacts', 'contacts': []}

        for user in response['roster']:
            id = str(user['jid'])
            if id not in self.contacts:
                self.contacts[id] = {
                    'id': id,
                    'name': None,
                    'groups': [],
                    'online': False,
                }
            if user['name']:
                self.contacts[id]['name'] = str(user['name'])
            else:
                self.contacts[id]['name'] = id
            self.contacts[id]['groups'] = user['groups']
        data['contacts'] = self.get_contatc_list()
        print "*************************************************************" \
              "*****\n\n\n\n"
        #self._handle_roster()
        """
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
        """
        #    print roster

        #print data
        self.chat_handler.send_contacts(data)

    def get_contatc_list(self):
        contacts = []
        for key, value in self.contacts.iteritems():
            contacts.append(value)
        return contacts

class XmppManager(object):

    def __init__(self):
        self.connections = {}

    def create_xmpp_connection(self, session_id, handler):
        user = handler.component.conf['user']
        logger.info("Creating xmmp connection wrapper for user %s with "
                    "password [******]" % user)
        self.connections[session_id] = {}
        self.connections[session_id]['client'] = PubSubXmppClient(handler)
        self.connections[session_id]['waiters'] = set()
        self.connections[session_id]['cache'] = []
        self.connections[session_id]['cache_size'] = 200


class DiasporaJetpackChatComponent(firenado.core.TornadoComponent):

    def __init__(self, name, application):
        self.xmpp_manager = None
        super(DiasporaJetpackChatComponent, self).__init__(
            name, application)

    def get_handlers(self):
        return [
            (r'/jetpack/chat', diaspora_jetpack.chat.handlers.ChatHandler),
            (r"/jetpack/chat/chatsocket",
                diaspora_jetpack.chat.handlers.ChatSocketHandler),
        ]

    def get_config_file(self):
        return 'chat.yaml'

    def initialize(self):
        logger.debug('Initializing chat component...')
        self.xmpp_manager = XmppManager()
        logger.debug('Xmmp manager created')

    def shutdown(self):
        print "closing connections..."
        for session_id, connection in \
                self.xmpp_manager.connections.iteritems():
            print "Closing connection from session %s." % session_id
            connection['client'].disconnect(wait=False)
