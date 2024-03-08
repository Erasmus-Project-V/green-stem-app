from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty
from kivymd.uix.button import MDIconButton
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.textfield import MDTextField

class InputWidget(MDRelativeLayout):
    field: MDTextField
    placeholder_text = StringProperty("Piši ovdje")
    field: MDTextField

    def __init__(self, **kwargs):
        super(InputWidget, self).__init__(**kwargs)
        Clock.schedule_once(self.post_init, .1)

    def post_init(self, clc):
        self.field = self.ids["text_field"]
        self.check_box = self.ids["checkbox"]
        self.field.bind(text=self.text_change)

    def check_text(self,widget,text):
        # ovdje implementat da text ne overshoota
        return


    def return_text(self):
        return self.field.text

    def exit_error_mode(self):
        self.field.helper_text = ""
        self.check_box.error_mode = False

    def enter_error_mode(self, error_message):
        self.field.error = True
        self.field.helper_text = error_message
        self.check_box.error_mode = True

    def clear_text(self):
        self.field.text = ""

