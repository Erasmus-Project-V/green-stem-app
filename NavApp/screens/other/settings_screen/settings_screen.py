from kivymd.uix.screen import MDScreen

class SettingsScreen(MDScreen):

    def return_to_profile(self,button):
        self.manager.goto_screen("pfs")

    def open_notifications(self,*args):
        self.manager.goto_screen("uss")

    def open_about_us(self,*args):
        self.manager.goto_screen("abt")
