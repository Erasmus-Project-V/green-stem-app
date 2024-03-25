from kivy.metrics import dp
from kivy.properties import ListProperty, StringProperty
from kivy.uix.button import Button
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.label import Label
from kivymd.uix.relativelayout import MDRelativeLayout
from scripts.utilities import find_manager
from kivy.clock import Clock


class TopMenuWidget(MDBoxLayout):
    top_widgets = ListProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.top_widgets = []
        Clock.schedule_once(self.add_units, .1)

    def build_unit(self, text, screen_ref, callback):
        unit = Button(text=text,
                      font_name=self.font_ref,
                      background_color= (0,0,0,0),
                      on_press=callback
        )
        unit.name = screen_ref
        sub = MDLabel(text= "____",
                      font_size=dp(24),
                      pos_hint={"y":-0.2},
                      halign="center",
                      theme_text_color="Custom",
                      opacity=self.login,
                      text_color=self.underscore_color)
        wrapper = MDRelativeLayout()
        wrapper.add_widget(unit)
        wrapper.add_widget(sub)
        # self.top_widgets.append(unit)
        return wrapper

    def add_units(self, clc):
        for unit in self.top_widgets:
            btn_text = unit[0]
            button_func = self.button_pressed
            screen_ref = None
            if callable(unit[1]):
                button_func = unit[1]
            else:
                screen_ref = unit[1]
            self.add_widget(self.build_unit(btn_text, screen_ref, button_func))

    def button_pressed(self, btn):
        parent = find_manager(btn.parent)
        if parent:
            parent.goto_screen(btn.name)
        else:
            print("parent couldn't be found, error")

