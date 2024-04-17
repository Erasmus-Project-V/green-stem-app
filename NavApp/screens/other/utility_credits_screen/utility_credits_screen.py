from kivymd.uix.screen import MDScreen
from  kivymd.uix.boxlayout import MDBoxLayout
class Content(MDBoxLayout):
    pass

class UtilityCreditsScreen(MDScreen):
    def goto_about_us(self, button):
        self.manager.goto_screen("abt")