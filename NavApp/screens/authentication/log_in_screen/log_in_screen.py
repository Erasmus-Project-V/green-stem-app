from kivy.core.window import Window
from kivymd.uix.screen import MDScreen


class LogInScreen(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_login(self,button):
        print("login validation....")
        email = self.ids["email_text"].return_text()
        password = self.ids["password_text"].return_text()
        if "" in (email,password):
            print("Please input something!")
            return
        elif len(email) > 50 or len(password) > 50:
            print("email/password too long!")
            return
        log, is_good = self.send_login(email,password)
        print(log)
        if is_good:
            self.manager.goto_screen("hme")
    def send_login(self,email,password):
        # šalje se email i password u backend te se onda dalje ide s tim
        return "login info recieved from backend",True

    def forgotten_password(self):
        print("password forgotten...")