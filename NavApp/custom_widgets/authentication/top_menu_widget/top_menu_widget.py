from kivy.properties import ColorProperty
from kivymd.uix.boxlayout import MDBoxLayout
# from NavApp.scripts.utilities import find_manager
from scripts.utilities import find_manager
class TopMenuWidget(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def button_pressed(self,btn):
        parent = find_manager(btn.parent)
        if parent:
            parent.goto_screen(btn.name)
        else:
            print("parent couldn't be found, error")