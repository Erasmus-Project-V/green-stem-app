from kivymd.uix.screen import MDScreen


class ForgotPasswordScreen(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def send_password_code(self,sender):
        self.manager.goto_screen("lgn")

    def return_to_login(self,button):
        self.manager.goto_screen("lgn")