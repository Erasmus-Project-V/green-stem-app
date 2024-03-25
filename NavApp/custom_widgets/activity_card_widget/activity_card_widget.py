from kivy.clock import Clock
from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatButton
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.properties import StringProperty
from scripts.utilities import find_manager


class ActivityCardWidget(MDRelativeLayout):
    img_path = StringProperty("")
    text = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hero_ref = None
        Clock.schedule_once(self.build_self, 0)

    def build_self(self, dt):
        self.hero_ref = self.ids["hero_from"]
        if self.hero_ref.tag == "placeholder":
            raise RuntimeError('Hero not assigned a unique tag!!!!')

    def clicked(self, button):
        print("please implement custom press command!")

