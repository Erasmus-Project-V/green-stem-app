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
sys.path.append('/NavApp/custom_widgets')

from custom_widgets.input_widget.input_widget import InputWidget
from custom_widgets.oval_blue_button_widget.oval_blue_button_widget import OvalBlueButtonWidget 

Window.softinput_mode = "below_target"
class ForgotPasswordScreen(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.relative_layout = MDRelativeLayout(pos_hint={"center_x":0.6,"center_y":0.9})
        self.title_stack_layout = MDStackLayout(pos_hint={"center_x":0.2,"center_y":0.5}, size_hint=(0.85,0.2), spacing=-200)
        self.button_stack_layout = MDStackLayout(pos_hint={"center_x":0.4,"center_y":-0.3}, size_hint=(0.85,0.2), spacing=-100)

        self.label1 = Label(text="Forgot password?", font_size=50, size_hint_x=1)
        self.label2 = Label(text='Enter your email address.', font_size=30, size_hint_x=0.9)
        self.title_stack_layout.add_widget(self.label1)
        self.title_stack_layout.add_widget(self.label2)

        self.above_button_label = Label(text="Send the code to my email address:", font_size=25, color=(95 / 255, 163 / 255, 201 / 255, 1))
        self.button_stack_layout.add_widget(self.above_button_label)

        self.relative_layout.add_widget(self.title_stack_layout)
        self.input_widget = InputWidget(placeholder_text="Email")
        self.relative_layout.add_widget(self.input_widget)
        self.relative_layout.add_widget(self.button_stack_layout)
        self.add_widget(self.relative_layout)

    def create_code_conformation_screen(self,button):
        self.relative_layout.remove_widget(self.input_widget)

        self.label1.text = "Conformation"
        self.label2.text = "Check your email for the code"

        self.label1.size_hint_x = 0.85
        self.label2.size_hint_x = 1

        self.code_stack_layout = MDStackLayout(orientation='tb-lr', pos_hint={"center_x":0.1,"center_y":0.2}, adaptive_height=False, size_hint=(0.13,0), spacing=10, padding=10)

        for i in range(6):
            self.code_stack_layout.add_widget(InputWidget(placeholder_text="•"))

        self.above_button_label.text = "Confirm code:"

        self.button = self.ids["blue_button"]
        self.button.button_text = "Confirm"
        self.button.release_func = self.create_change_password_screen

        self.top_return_button = self.ids["top_return_button"]
        self.top_return_button.release_func = self.return_to_forgot_pass

        self.relative_layout.add_widget(self.code_stack_layout)

    def create_change_password_screen(self, button):
        self.label1.text = "Change password"
        self.label2.text = "Enter new password"

        self.label1.size_hint_x = 1
        self.label2.size_hint_x = 0.83

        self.relative_layout.remove_widget(self.code_stack_layout)

        self.new_pass_layout = MDStackLayout(pos_hint={"center_x":0.4,"center_y":0.2}, size_hint=(0.85,0.2), spacing=10)

        self.new_pass_layout.add_widget(InputWidget(placeholder_text="New password", is_password=True))
        self.new_pass_layout.add_widget(InputWidget(placeholder_text="Confirm new password", is_password=True))

        self.relative_layout.add_widget(self.new_pass_layout)

        self.top_return_button = self.ids["top_return_button"]
        self.top_return_button.release_func = self.return_to_forgot_pass

        self.above_button_label.text = "Confirm new password:"
        self.button.release_func = self.return_to_login
        
    def send_password_code(self,sender):
        
        self.manager.goto_screen("lgn")

    def return_to_login(self,button):
        self.clear_widgets()
        self.__init__()
        self.manager.goto_screen("lgn")
    
    def return_to_forgot_pass(self, button):
        self.clear_widgets()
        self.__init__()
    
    def toggle_labels(self, instance):
        # Toggle visibility of labels
        if self.label1.parent:
            self.remove_widget(self.label1)
            self.add_widget(self.label2)
        else:
            self.remove_widget(self.label2)
            self.add_widget(self.label1)