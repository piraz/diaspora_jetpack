import diaspora_jetpack.handlers
import firenado.core
import tornado.web
import os


class DiasporaJetpackComponent(firenado.core.TornadoComponent):

    def get_handlers(self):
        return [
            (r'/jetpack', diaspora_jetpack.handlers.IndexHandler),
            (r'/jetpack/session', diaspora_jetpack.handlers.SessionHandler),
            (r"/jetpack/static/(.*)", tornado.web.StaticFileHandler,
             {"path": os.path.join(self.get_component_path(),
                                   'static')}),
            (r"/jetpack/bower_components/(.*)", tornado.web.StaticFileHandler,
             {"path": os.path.join(self.get_component_path(),
                                   'bower_components')}),
        ]
