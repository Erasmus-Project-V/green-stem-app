from kivymd.uix.screen import MDScreen

class UtilityAboutUsScreen(MDScreen):
    def return_to_settings(self, button):
        self.manager.goto_screen("stg")

    def goto_credits_screen(self, button):
        self.manager.goto_screen("crd")

