import diaspora_jetpack.chat.handlers
import firenado.core
import os


class DiasporaJetpackChatComponent(firenado.core.TornadoComponent):

    def get_handlers(self):
        return [
            (r'/jetpack/chat', diaspora_jetpack.chat.handlers.ChatHandler),
            (r"/jetpack/chatsocket", diaspora_jetpack.chat.handlers.ChatSocketHandler),
        ]
