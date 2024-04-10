from kivymd.uix.screen import MDScreen

class UtilitySettingsScreen(MDScreen):

    def return_to_settings(self,button):
        self.manager.goto_screen("stg")