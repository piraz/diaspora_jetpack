import firenado.core
import firenado.core.data as data


class JetpackHandler(object):

    def init_jetpack(self):
	self.diaspora_session = self.get_cookie('_diaspora_session')
	self.validation_token_key = self.get_cookie('_validation_token_key')
	self.shared_session = self.application.data_sources['shared_session'].get_connection()
	self.chat_cache = self.application.data_sources['chat_cache'].get_connection()
	
	# self.request.headers['Remote_addr']

class IndexHandler(firenado.core.TornadoHandler, JetpackHandler):

    def get(self):
	self.init_jetpack()
	print self.shared_session.get('diaspora_session:%s' % self.validation_token_key)
	print self.chat_cache
        self.render("index.html", message="Hello world!!!")

class SessionHandler(firenado.core.TornadoHandler):

    def get(self):
        reset = details=self.get_argument("reset", False, True)
        if reset:
            self.session.delete('counter')
            self.redirect('/jetpack/session')
            return None
        counter = 0
        if self.session.has('counter'):
            counter = self.session.get('counter')
        counter += 1
        self.session.set('counter', counter)
        self.render("session.html", session_value=counter)
