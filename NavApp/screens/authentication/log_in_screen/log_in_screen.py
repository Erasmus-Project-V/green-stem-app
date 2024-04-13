import json

import kivy.utils
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.screen import MDScreen
from kivy.network.urlrequest import UrlRequest


class LogInScreen(MDScreen):
    max_email_len = 32
    max_password_len = 64

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.open_loading, 0)
        self.waiter = Clock.schedule_interval(self.start_up_screen,.2)
        self.procedure_case = 0

    def open_loading(self,dt):
        ls = self.manager.get_screen("uls")
        self.check_local_sign_in(0)
        delay = 5 if kivy.utils.platform == "android" else 0.5
        ls.start(None,self.finish_procedure,delay)
        self.manager.goto_screen("uls")

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
        if self.procedure_case == 1:
            ls = self.manager.get_screen("uls")
            ls.start(None,self.finish_procedure,4)
            self.manager.goto_screen("uls")
        else:
            self.finish_procedure(0)

    def finish_procedure(self,dt):
        refs = {0:"lgn",1:"sss",2:"hme"}
        self.manager.goto_screen(refs[self.procedure_case])

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
            self.procedure_case = 1
            sss = self.manager.get_screen("sss")
            Clock.schedule_once(sss.initialize_widgets, 1)
        elif not self.manager.active_user.get_user_attribute("weight"):
            self.procedure_case = 1
        else:
            self.procedure_case = 2
            hs = self.manager.get_screen("hme")
            Clock.schedule_once(hs.set_up_user_data,0.1)


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
