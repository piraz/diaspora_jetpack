from firenado.core.service import FirenadoService


class SigninService(FirenadoService):

    def configure_service(self):
        self.data_source = self.get_data_source('register')

    def increment_ip(self, ip):
        number = self.data_source.get_connection().get("ip:%s"%ip)
        if number:
            number = int(number) + 1
        else:
            number = 1
        self.data_source.get_connection().set("ip:%s"%ip, number)

    def generate_captcha(self):
        pass

    def is_ip_locked(self, ip, times):
        number = self.data_source.get_connection().get("ip:%s"%ip)
        number = int(number)
        if number >= times:
            return True
        return False


    def receive_email(self, register, email):
        pass

    def set_terms_read(self, register):
        pass

    def set_personal_data(self, register, username, first_name, last_name):
        pass
