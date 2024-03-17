from kivymd.uix.screen import MDScreen


class ProfileScreen(MDScreen):

    def sign_out(self, button):
        self.manager.active_user.erase_user_data()
        self.manager.goto_screen("lgn")
