from kivy.properties import ColorProperty
from kivymd.uix.boxlayout import MDBoxLayout


class TopMenuWidget(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def button_pressed(self,btn):
        parent = self.parent
        try:
            while parent.name != "manager" and parent.parent:
                parent = parent.parent
        except AttributeError:
            print("error occured while trying to locate screen manager from top_menu_widget")
        if btn.name == parent.current:
            return
        parent.goto_screen(btn.name)