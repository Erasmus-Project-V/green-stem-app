import re

from kivy.network.urlrequest import UrlRequest
from kivymd.uix.screen import MDScreen
import requests


class SignUpScreen(MDScreen):

    def __init__(self, **kw):
        super().__init__(**kw)

    def create_new_user(self, button):

        username = self.ids["new_user_name_text"]
        email = self.ids["new_email_text"]
        password = self.ids["new_password_text"]
        password_repeat = self.ids["new_password_repeat_text"]

        pass_holder = None
        is_good = 0

        for comp in (username, email, password,password_repeat):
            comp_text = comp.return_text()
            if comp.name == "password":
                pass_holder = comp
            if len(comp_text) < 4:
                comp.enter_error_mode(f"{comp.name.capitalize()} je prazan ili prekratak!")
                continue
            elif len(comp_text) > 24:
                comp.enter_error_mode(f"{comp.name.capitalize()} je predugačak!")
                continue
            elif comp.name == "password_repeat":
                if pass_holder.return_text() != comp_text:
                    pass_holder.enter_error_mode(f"Šifre se ne poklapaju!")
                    comp.enter_error_mode("Šifre se ne poklapaju!")
                else:
                    is_good += 1
                    pass_holder.exit_error_mode()
                    comp.exit_error_mode()
                continue
            if comp.name == "email":
                if not re.match(".+@.+\..+",comp_text):
                    comp.enter_error_mode("Email nije ispravno napisan!")
                    continue
            is_good += 1
            comp.exit_error_mode()
        if is_good < 4:
            return
        self.send_new_user(username, email, password)
        self.ids["signup_button"].button_disabled = True


    def send_new_user(self, username, email, password):
        payload = {
            "username": username,
            "email": email,
            "password": password,
            "passwordConfirm": password,
            "emailVisibility": True,
        }

        UrlRequest(url="http://localhost:8090/api/collections/users/auth-with-password", req_body=payload,
                   on_success=lambda a, b: self.successful_sign_up(a, b),
                   on_error=lambda a, b: self.error_sign_up(a, b))

    def successful_sign_up(self, thread, text):
        print(text)
        self.ids["signup_button"].button_disabled = False


    def error_sign_up(self, thread, text):
        print(text)
        self.ids["signup_button"].button_disabled = False

