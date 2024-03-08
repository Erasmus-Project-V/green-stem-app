from kivy.uix.screenmanager import Screen


class ProfileScreen(Screen):

    def sign_out(self, button):
        self.manager.active_user.erase_user_data()
        self.manager.goto_screen("lgn")
