from kivy.network.urlrequest import UrlRequest
from kivymd.uix.screen import MDScreen
import requests


class SignUpScreen(MDScreen):

    def __init__(self, **kw):
        super().__init__(**kw)

    def create_new_user(self, button):
        print("Creating a new user")
        username = self.ids["new_user_name_text"].return_text()
        email = self.ids["new_email_text"].return_text()
        password = self.ids["new_password_text"].return_text()
        password_repeat = self.ids["new_password_repeat_text"].return_text()

        if "" in (email, password, username):
            print("Please input something!")
            self.ids["new_user_name_text"].enter_error_mode("Upiši username!")
            return
        elif len(email) > 24 or len(password) > 64 or len(username) > 32:
            print("username/email/password too long!")
            return
        if password != password_repeat:
            print("Passwords are not matching")
            return
        log, is_good = self.send_new_user(username, email, password)
        print(log)
        # if is_good:
        #     self.manager.goto_screen("sss")

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

    def successful_sign_up(self,thread,text):
        pass

    def error_sign_up(self,thread,text):
        pass