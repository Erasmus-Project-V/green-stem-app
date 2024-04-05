import json

from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.screen import MDScreen
from kivy.network.urlrequest import UrlRequest


class LogInScreen(MDScreen):
    max_email_len = 32
    max_password_len = 64

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.check_local_sign_in, 0.01)
        self.waiter = Clock.schedule_interval(self.start_up_screen,.2)

    def check_local_sign_in(self, dt):
        if self.manager.active_user.load_user_data():
            self.check_for_unfinished_sign_up()

    def start_up_screen(self,*args):
        self.top_menu = self.ids["top_menu"]
        if self.top_menu.built:
            self.waiter.cancel()
            self.top_menu.animate_underscore(self.name)

    def validate_login(self, button):

        email = self.ids["email_text"]
        password = self.ids["password_text"]
        email_text = email.return_text()
        password_text = password.return_text()
        e_len = len(email_text)
        p_len = len(password_text)

        # nije najljepše ali funkcionira
        if not 0 < e_len < self.max_email_len or not 0 < p_len < self.max_password_len:
            if p_len > self.max_password_len:
                password.enter_error_mode("Lozinka je predugačka!")
            elif not p_len:
                password.enter_error_mode("Upiši lozinku!")
            if e_len > self.max_email_len:
                email.enter_error_mode("Email je predugačak!")
            elif not e_len:
                email.enter_error_mode("Upiši Email!")
            return

        print("sending")
        self.ids["login_button"].button_disabled = True
        self.send_login(email_text, password_text)

    def send_login(self, email, password):
        payload = {
            "identity": email,
            "password": password,
        }

        self.manager.active_user.send_request(path="/api/collections/users/auth-with-password",
                                              method="POST",
                                              body=json.dumps(payload),
                                              success_func=self.successful_sign_in,
                                              error_func=self.error_sign_in,
                                              )

    def successful_sign_in(self, thread, response_text):
        self.ids["login_button"].button_disabled = False
        self.ids["email_text"].clear_text()
        self.manager.active_user.write_user_data(response_text["token"], response_text["record"])
        self.ids["password_text"].clear_text()
        self.check_for_unfinished_sign_up()

    def check_for_unfinished_sign_up(self):
        if not self.manager.active_user.get_user_attribute("verified"):
            self.manager.active_user.send_request(path="/api/collections/users/request-verification",
                                                  method="POST",
                                                  body=json.dumps({
                                                      "email": self.manager.active_user.get_user_attribute("email")
                                                  }),
                                                  success_func=lambda a, b: print(
                                                      "sucess! (mail verification request)"),
                                                  error_func=self.error_sign_in,
                                                  )
            self.manager.goto_screen("sss")
        elif not self.manager.active_user.get_user_attribute("weight"):
            self.manager.goto_screen("sss")
        else:
            self.manager.goto_screen("hme")


    def error_sign_in(self, thread, text):
        print("error", text)
        if text.__class__ == dict:
            self.ids["email_text"].enter_error_mode("wrong email/username or password!")
            self.ids["password_text"].enter_error_mode("wrong email/username or password!")
            self.ids["password_text"].clear_text()
        ## u budućnosti napraviti popup custom widget koji će reći da nema konekcije?
        self.ids["login_button"].button_disabled = False

    def forgotten_password(self):
        self.manager.goto_screen("fgp")
