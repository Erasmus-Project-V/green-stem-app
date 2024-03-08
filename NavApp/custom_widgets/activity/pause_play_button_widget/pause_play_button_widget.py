from kivy.clock import Clock
from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatButton
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.properties import StringProperty


class PausePlayButtonWidget(MDRelativeLayout):
    center_pos = {"center_x": 0.5, "center_y": 0.5}
    button_type = StringProperty("play")
    possible_button_types = ["play", "pause", "stop", "restore"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.md_bg_color = (1, 1, 1, 1)
        self.checker = None
        self.hold_timeout = 3

    def hold_complete(self, dt):
        print("Implement custom hold command! (or just placeholder)")

    def pressed(self, button):
        if self.checker: self.checker.cancel()
        self.checker = Clock.schedule_once(self.hold_func, self.hold_timeout)

    # ne ovo overrideati!
    def release_inline(self, button):
        self.checker.cancel()
        self.button_type = {"play": "pause", "pause": "play", "stop": "stop", "check": "check"}[self.button_type]

    def set_button_type(self, type):
        self.button_type = type

    def get_button_type(self):
        return self.button_type

    def button_released(self, button):
        print("implement custom button_released method!")

    def change_color(self, color):
        self.ids["btn_in"].md_bg_color = color
