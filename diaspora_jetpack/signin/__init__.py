import diaspora_jetpack.signin.handlers
import firenado.core


class DiasporaJetpackSingInComponent(firenado.core.TornadoComponent):

    def get_handlers(self):
        return [
            (r'/jetpack/sign_in/?',
             diaspora_jetpack.signin.handlers.EmailHandler),
            (r'/jetpack/sign_in/email_confirmation/?',
             diaspora_jetpack.signin.handlers.EmailConfirmationHandler),
            (r'/jetpack/sign_in/terms/?',
             diaspora_jetpack.signin.handlers.TermsHandler),
            (r'/jetpack/sign_in/personal_data/?',
             diaspora_jetpack.signin.handlers.PersonalDataHandler),
        ]
