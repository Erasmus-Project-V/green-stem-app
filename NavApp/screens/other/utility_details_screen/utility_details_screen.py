#File name: utility_details_screen.py

from kivymd.uix.screen import MDScreen
from  kivymd.uix.boxlayout import MDBoxLayout
class Content(MDBoxLayout):
    pass

class UtilityDetailsScreen(MDScreen):
    def goto_credits(self, button):
        self.manager.goto_screen("crd")
