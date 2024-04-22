from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout

class Content(MDBoxLayout):
    pass

class UtilityCreditsScreen(MDScreen):
    def goto_about_us(self, button):
        self.manager.goto_screen("abt")

    def show_details(self, text, source):
        # Accessing the dtl screen and modifying its top_text label text
        dtl_screen = self.manager.get_screen("dtl")
        dtl_screen.ids.top_text.text = text
        dtl_screen.ids.pfp_image.source = source
        self.manager.goto_screen("dtl")
