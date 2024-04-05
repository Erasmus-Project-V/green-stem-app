from kivy.animation import Animation
from kivy.metrics import dp
from kivy.properties import ListProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.label import Label
from kivymd.uix.relativelayout import MDRelativeLayout
from scripts.utilities import find_manager
from kivy.clock import Clock


class TopMenuWidget(MDBoxLayout):
    top_widgets = ListProperty()
    selected = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_refs = {}
        self.button_callbacks = {}

        self.animation_active = False
        self.built = False

        Clock.schedule_once(self.add_units, .1)

    def build_unit(self, text, screen_ref, callback):
        unit = Button(text=text,
                      font_name=self.font_ref,
                      background_color=(0, 0, 0, 0),
                      on_press=self.callback_intermediary
                      )
        if screen_ref:
            unit.name = screen_ref
        else:
            unit.name = text
        sub = Image(source="assets/images/sprites/top_menu_underline.png",
                    size_hint=(0.6, 0.08),
                    pos_hint={"center_y": 0.1, "center_x": 0.5},
                    opacity=self.login,
                    fit_mode="fill")
        self.image_refs[unit.name] = sub
        self.button_callbacks[unit.name] = callback
        wrapper = MDRelativeLayout()
        wrapper.add_widget(unit)
        wrapper.add_widget(sub)
        # self.top_widgets.append(unit)
        return wrapper

    def add_units(self, clc):
        for unit in self.top_widgets:
            btn_text = unit[0]
            screen_ref = None
            if callable(unit[1]):
                button_func = unit[1]
            else:
                screen_ref = unit[1]
                button_func = self.transfer_screen
            self.add_widget(self.build_unit(btn_text, screen_ref, button_func))
        self.animate_underscore(self.top_widgets[self.selected][0])
        self.built = True

    def finish_animation(self,a,b):
        self.animation_active = False

    def animate_underscore(self, name,animate = False):
        animation_fade_out = Animation(opacity=0, duration=1)
        animation_fade_in = Animation(opacity=1, duration=1)
        self.animation_active = True
        animation_fade_in.bind(on_complete=self.finish_animation)
        if self.selected.__class__ != int and animate:
            animation_fade_out.start(self.image_refs[self.selected])
        for ref in self.image_refs.keys():
            if ref == name:
                animation_fade_in.start(self.image_refs[ref])
            else:
                self.image_refs[ref].opacity = 0
        self.selected = name

    def callback_intermediary(self, button):
        if self.animation_active:
            return
        name = button.name
        self.animate_underscore(name,animate=True)
        self.button_callbacks[name](button)

    def placeholder(self):
        print("not implemented!")

    def transfer_screen(self, btn):
        parent = find_manager(btn.parent)
        if parent:
            parent.goto_screen(btn.name)
        else:
            print("parent couldn't be found, error")
