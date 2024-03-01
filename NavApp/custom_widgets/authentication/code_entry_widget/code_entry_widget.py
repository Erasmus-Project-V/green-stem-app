from kivy.metrics import dp
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout


class CodeEntryWidget(MDRelativeLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.no_of_characters = 6
        self.unit_width = 32
        self.build_self()

    def build_self(self):
        for i in range(1, self.no_of_characters + 1):
            tc = MDLabel(pos_hint={"center_x": 0.5, "center_y": 0.5},
                         size_hint=(1, 1),
                         text="Y",
                         halign="center")
            uc = MDLabel(pos_hint={"center_x":0.5, "center_y": 0.2},
                         text="_" * (self.unit_width // self.no_of_characters),
                         halign="center")
            LT = MDRelativeLayout(size_hint=(1 / self.no_of_characters, 1),
                                  pos_hint={"center_x": i / (self.no_of_characters + 1), "center_y": 0.5})
            LT.add_widget(tc)
            LT.add_widget(uc)
            tc.font_size = dp(64)
            self.add_widget(
                LT
            )