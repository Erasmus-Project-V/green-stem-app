from kivymd.uix.screen import MDScreen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivymd.uix.label import MDLabel
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.core.window import Window

import sys

from NavApp.custom_widgets.input_widget.input_widget import InputWidget

sys.path.append('/NavApp/custom_widgets')

Window.softinput_mode = "below_target"
class ForgotPasswordScreen(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.top_label_one_text = None
        self.top_label_one = None

    def start_up_screen(self):
        print("starting_up_pass")