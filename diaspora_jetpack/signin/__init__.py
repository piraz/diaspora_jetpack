import diaspora_jetpack.signin.handlers
import firenado.core


class DiasporaJetpackSingInComponent(firenado.core.TornadoComponent):

    def get_handlers(self):
        return [
            (r'/jetpack/sing_in', diaspora_jetpack.signin.handlers.EmailHandler),
        ]


