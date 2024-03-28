from kivy.clock import Clock
from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatButton
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.properties import StringProperty
from scripts.utilities import find_manager


class ActivityCardWidget(MDRelativeLayout):
    img_path = StringProperty("")
    text = StringProperty()

    def __init__(self,hero_tag=None,activity_type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hero_ref = None
        self.build_self(hero_tag,activity_type)

    def build_self(self, hero_tag,activity_type):
        self.hero_ref = self.ids["hero_from"]
        self.hero_ref.tag = hero_tag
        self.ids.rel_two.hero_tag = hero_tag
        self.ids.rel_two.activity_type = activity_type

    def clicked(self, button):
        print("please implement custom press command!")

