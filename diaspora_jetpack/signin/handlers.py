import firenado.core
from captcha.image import ImageCaptcha
from firenado.util import random_string
import os
import firenado.conf
from PIL import Image
import io
import collections


class EmailHandler(firenado.core.TornadoHandler):

    def get(self):
        image = ImageCaptcha(fonts=['/usr/share/fonts/dejavu/DejaVuSans.ttf', '/usr/share/calibre/fonts/liberation/LiberationSerif-Regular.ttf'])
        string = random_string(5)
        anti_cache = random_string(22)

        data = image.generate(string)
        if os.path.exists('%s/static/captcha/%s%s.png' % (firenado.conf.APP_CONFIG_ROOT_PATH, self.session.id, self.session.get('anti_cache'))):
            os.remove('%s/static/captcha/%s%s.png' % (firenado.conf.APP_CONFIG_ROOT_PATH, self.session.id, self.session.get('anti_cache')))
        self.session.set('anti_cache', anti_cache)

        image.write(string, 'static/captcha/%s%s.png' % (self.session.id, anti_cache))
        f = Image.open('%s/static/captcha/%s%s.png' % (firenado.conf.APP_CONFIG_ROOT_PATH, self.session.id, anti_cache))
        o = io.BytesIO()
        f.save(o, format="PNG")
        s = o.getvalue()

        data = collections.defaultdict(lambda: collections.defaultdict(dict))
        data['photo']=s

        self.render("jetpack:signin/email.html", session_id = self.session.id, anti_cache = anti_cache)
