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
    
    def submitt_clicked(self, button):
        self.title = self.ids["title_label"]
        self.subtitle = self.ids["subtitle_label"]
        self.confirm_code = self.ids["button_title"]
        self.button = self.ids["blue_button"]

        self.title.text = "Confirmation"
        self.title.pos_hint = {'center_x': 0.23, 'center_y': 0.7}
        self.subtitle.text = "Check your email for the code"
        self.subtitle.pos_hint = {'center_x': 0.3, 'center_y': 0.5}
        self.confirm_code.text = "Confirm code"
        self.button.button_text = "Confirm"
        self.button.release_func = self.confirm_clicked
    
    def confirm_clicked(self, button):
        print("confirm clicked")
        self.title.text = "Change password"
        self.title.pos_hint = {'center_x': 0.3, 'center_y': 0.7}
        self.subtitle.text = "Enter new password"
        self.subtitle.pos_hint = {'center_x': 0.22, 'center_y': 0.5}
        
        self.new_pass = self.ids["new_password_text"]
        self.confirm_new_pass = self.ids["confirm_new_password_text"]
        self.code_enty = self.ids["code_entry_widget"]
        
        self.code_enty.opacity = 0

        self.new_pass.opacity = 1
        self.confirm_new_pass.opacity = 1

        self.button.release_func = self.return_home
    
    def return_home(self, button):
        self.manager.goto_screen("hme")