import json
import re

from kivy.network.urlrequest import UrlRequest
from kivymd.uix.screen import MDScreen


class SignUpScreen(MDScreen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.user_id = None

    def start_up_screen(self):
        self.top_menu = self.ids["top_menu"]
        self.top_menu.animate_underscore(self.name)

    def create_new_user(self, button):

        username = self.ids["new_user_name_text"]
        email = self.ids["new_email_text"]
        password = self.ids["new_password_text"]
        password_repeat = self.ids["new_password_repeat_text"]

        pass_holder = None
        is_good = 0

        for comp in (username, email, password, password_repeat):
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
                if not re.match(".+@.+\..+", comp_text):
                    comp.enter_error_mode("Email nije ispravno napisan!")
                    continue
            is_good += 1
            comp.exit_error_mode()
        if is_good < 4:
            return
        self.send_new_user(username, email, password)
        self.ids["signup_button"].button_disabled = True

    def send_new_user(self, username, email, password):
        # napraviti client
        self.payload = {
            "username": username.return_text(),
            "email": email.return_text(),
            "password": password.return_text(),
            "passwordConfirm": password.return_text(),
            "emailVisibility": True,
        }

        self.manager.active_user.send_request(path="/api/collections/users/records",
                                              method="POST",
                                              body=json.dumps(self.payload),
                                              error_func=self.error_sign_up,
                                              success_func=self.successful_sign_up)

    def successful_sign_up(self, thread, response_text):
        self.user_id = response_text["id"]
        new_payload = {
            "identity": self.payload["username"],
            "password": self.payload["password"]
        }

        self.manager.active_user.send_request(path="/api/collections/users/auth-with-password",
                                              method="POST",
                                              body=json.dumps(new_payload),
                                              error_func=self.error_sign_up,
                                              success_func=self.successful_post_sign_up)

        self.manager.active_user.send_request(path="/api/collections/users/request-verification",
                                              method="POST",
                                              body=json.dumps({
                                                  "email": self.payload["email"]
                                              }),
                                              success_func=lambda a, b: print("sucess! (mail verification request)"),
                                              error_func=self.error_sign_up,
                                              )

    def successful_post_sign_up(self, thread, response_text):
        self.manager.active_user.write_user_data(response_text["token"], response_text["record"])
        self.ids["signup_button"].button_disabled = False
        self.manager.goto_screen("sss")

    def error_sign_up(self, thread, response_text):
        print(f"error: {response_text} {thread}")
        self.ids["signup_button"].button_disabled = False
