from kivy.properties import StringProperty, BooleanProperty
from kivymd.uix.button import MDIconButton
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.textfield import MDTextField


class InputWidget(MDRelativeLayout):
    placeholder_text = StringProperty("Piši ovdje")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def return_text(self):
        return self.ids["text_field"].text

