from kivymd.uix.screen import MDScreen


class SecondSignUpScreen(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def return_to_signup(self,button):
        self.manager.goto_screen("sgn")