from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatButton
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.properties import StringProperty

class PausePlayButtonWidget(MDRelativeLayout):
    center_pos = {"center_x": 0.5, "center_y": 0.5}
    button_type = StringProperty("start")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.md_bg_color = (1, 1, 1, 1)

    def clicked(self, button):
        print("please implement custom press command!")

    def change_color(self,color):
        self.ids["btn_in"].md_bg_color = color