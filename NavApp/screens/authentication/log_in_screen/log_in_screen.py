from kivy.storage.jsonstore import JsonStore
from kivymd.uix.screen import MDScreen
from kivy.network.urlrequest import UrlRequest


class LogInScreen(MDScreen):
    max_email_len = 32
    max_password_len = 64

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        print(button)
        self.ids["login_button"].button_disabled = True
        self.send_login(email_text, password_text)

    def send_login(self, email, password):
        payload = {
            "identity": email,
            "password": password,
        }

        UrlRequest(url="http://localhost:8090/api/collections/users/auth-with-password", req_body=payload,
                   on_success=lambda a, b: self.successful_sign_in(a, b),
                   on_error=lambda a, b: self.error_sign_in(a, b))

    def successful_sign_in(self, thread, text):
        self.ids["login_button"].button_disabled = False
        print(text)
        self.manager.goto_screen("hme")

    def error_sign_in(self, thread, text):
        print("error", text)
        ## u budućnosti napraviti popup custom widget koji će reći da nema konekcije?
        self.ids["login_button"].button_disabled = False

    def forgotten_password(self):
        self.manager.goto_screen("fgp")
