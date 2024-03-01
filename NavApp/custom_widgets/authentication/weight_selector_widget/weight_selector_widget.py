from kivy.metrics import dp
from kivymd.effects.roulettescroll import RouletteScrollEffect
from kivymd.uix.label import MDLabel
from NavApp.custom_widgets.authentication.selector_behavior_widget.selector_behavior_widget import *


class WeightSelectorWidget(SelectorBehaviorWidget):

    def __init__(self, **kwargs):
        self.do_scroll_y = False
        self.do_scroll_x = True
        self.button_num = 200
        self.component_width = dp(20)
        self.component_height = dp(58.5)

        super().__init__(**kwargs)

        self.widget_type = (MDLabel, {"text": "|", "halign": "center",
                                      "pos_hint": {"center_x": 0.5, "center_y": 0.5},
                                      "size_hint": (1, 1), "font_size": dp(80),
                                      "text_color": self.blue_color_container
            , "theme_text_color": "Custom"})

        self.enumerate = False
        self.enumeration_min = 30

    def build_self(self, null):
        self.layout.bind(minimum_width=self.layout.setter('width'))
        self.effect_x = RouletteScrollEffect(anchor=4, interval=4)
        super().build_self()

    def opacity_refresh_hard(self, dt):
        super().opacity_refresh_hard(dt)