from kivymd.uix.screen import MDScreen

class SettingsScreen(MDScreen):

    def return_to_profile(self,button):
        self.manager.goto_screen("pfs")