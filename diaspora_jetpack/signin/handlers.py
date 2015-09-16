import firenado.core
from captcha.image import ImageCaptcha
from firenado.util import random_string
import os
import firenado.conf
from PIL import Image
import io
import collections
#from diaspora_jetpack.signin import services
from firenado.core.service import served_by
import tornado.web


# TODO send to the config
signin_service = 'diaspora_jetpack.signin.services.SigninService'

class EmailHandler(firenado.core.TornadoHandler):

    @tornado.web.removeslash
    @served_by(signin_service)
    def get(self):
        #x_real_ip = self.request.headers.get("X-Real-IP")
        #remote_ip = self.request.remote_ip if not x_real_ip else x_real_ip
        if self.signin_service.is_ip_locked(self.request.remote_ip, 6):
            print "The ip is blocked!!!"

        self.signin_service.increment_ip(self.request.remote_ip)
        image = ImageCaptcha(fonts=[
            '/usr/share/fonts/dejavu/DejaVuSans.ttf',
            '/usr/share/calibre/fonts/liberation/LiberationSerif-Regular.ttf']
        )
        string = random_string(5)
        anti_cache = random_string(22)
        self.session.set('captcha_string', string)
        data = image.generate(string)
        if os.path.exists('%s/static/captcha/%s%s.png' % (
                firenado.conf.APP_CONFIG_ROOT_PATH, self.session.id,
                self.session.get('anti_cache'))):
            os.remove('%s/static/captcha/%s%s.png' % (
                firenado.conf.APP_CONFIG_ROOT_PATH, self.session.id,
                self.session.get('anti_cache')))
        self.session.set('anti_cache', anti_cache)

        image.write(string, 'static/captcha/%s%s.png' % (
            self.session.id, anti_cache))
        f = Image.open('%s/static/captcha/%s%s.png' % (
            firenado.conf.APP_CONFIG_ROOT_PATH, self.session.id, anti_cache))
        o = io.BytesIO()
        f.save(o, format="PNG")
        s = o.getvalue()

        #data = collections.defaultdict(lambda: collections.defaultdict(dict))
        #data['photo']=s

        self.render("jetpack:singin/email.html",
                    session_id = self.session.id, anti_cache = anti_cache)

    def post(self):
        from validate_email import validate_email
        validate_email('example@example.com') 
        errors = []
        

class EmailConfirmationHandler(firenado.core.TornadoHandler):

    @tornado.web.removeslash
    @served_by(signin_service)
    def get(self):
        self.write('Email confirmation')


class EmailConfirmationHandler(firenado.core.TornadoHandler):

    @tornado.web.removeslash
    @served_by(signin_service)
    def get(self):
        self.write('Email confirmation')


class TermsHandler(firenado.core.TornadoHandler):

    @tornado.web.removeslash
    @served_by(signin_service)
    def get(self):
        self.write('Terms confirmation')


class PersonalDataHandler(firenado.core.TornadoHandler):

    @tornado.web.removeslash
    @served_by(signin_service)
    def get(self):
        self.render("jetpack:singin/personal_data.html")
