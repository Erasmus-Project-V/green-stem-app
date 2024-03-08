from kivy.metrics import dp
from kivymd.effects.roulettescroll import RouletteScrollEffect
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout
from NavApp.custom_widgets.authentication.selector_behavior_widget.selector_behavior_widget import SelectorBehaviorWidget


class AgeSelectorWidget(SelectorBehaviorWidget):

    def __init__(self, **kwargs):

        self.do_scroll_x = False
        self.do_scroll_y = True
        self.component_height = dp(58.5)
        self.component_width = dp(20)
        super().__init__(**kwargs)
        self.button_num = 40
        self.widget_type = (MDLabel, {"text": "Null", "halign": "center",
                                      "pos_hint": {"center_x": 0.5, "center_y": 0.5},
                                      "size_hint": (1, 1), "font_size": dp(80)})
        self.enumerate = True
        self.enumeration_min = 11

    def build_self(self, null):
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.effect_y = RouletteScrollEffect(anchor=50,interval=50)
        super().build_self(None)

    def opacity_refresh_hard(self, dt):
        super().opacity_refresh_hard(dt)