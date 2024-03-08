from kivy.metrics import dp
from kivy.properties import ColorProperty
from kivy.uix.button import Button
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout
from scripts.utilities import find_manager


class TopMenuWidget(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.top_widgets = []

    def build_unit(self,screen_ref,text):
        unit = Button(name=screen_ref,text=text,
                      font_name=self.font_ref,
                      background_color= (0,0,0,0)
        )
        sub = MDLabel(text= "____",
                      font_size=dp(24))
        wrapper = MDRelativeLayout()
        wrapper.add_widget(unit)
        self.top_widgets.append(unit)
        self.add_widget(wrapper)

    def button_pressed(self, btn):
        parent = find_manager(btn.parent)
        if parent:
            parent.goto_screen(btn.name)
        else:
            print("parent couldn't be found, error")
