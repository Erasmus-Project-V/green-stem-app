import requests
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.screen import MDScreen


class LogInScreen(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_login(self, button):
        print("login validation....")
        email = self.ids["email_text"].return_text()
        password = self.ids["password_text"].return_text()
        ## OVO TREBA LJEPŠE NAPISATI!!!!!!!!!!!!!!!!!!!!!
        if len(email) > 50 or len(password) > 50 or "" in (email, password):
            if len(password) > 50:
                self.ids["password_text"].enter_error_mode("Lozinka je predugačka!")
            elif not password:
                self.ids["password_text"].enter_error_mode("Upiši lozinku!")
            if len(email) > 50:
                self.ids["email_text"].enter_error_mode("Email je predugačak!")
            elif not email:
                self.ids["email_text"].enter_error_mode("Upiši Email!")
            return
        log, is_good = self.send_login(email, password)
        print(log)
        if is_good:
            self.manager.goto_screen("hme")

    def send_login(self, email, password):
        payload = {
            "identity": email,
            "password": password,
        }
        resp = requests.post("http://localhost:8090/api/collections/users/auth-with-password", json=payload)
        jso = resp.json()
        print(jso)
        if not resp.ok:
            return

        store = JsonStore("fitness_tracker.json")
        store.put("access_token", token=jso.get('token'))

        return "login info recieved from backend", True

    def forgotten_password(self):
        print("password forgotten...")
        self.manager.goto_screen("fgp")
