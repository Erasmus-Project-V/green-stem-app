from kivy.animation import Animation
from kivy.metrics import dp
from kivymd.effects.roulettescroll import RouletteScrollEffect
from kivymd.uix.label import MDLabel

from NavApp.custom_widgets.authentication.selector_behavior_widget.selector_behavior_widget import \
    SelectorBehaviorWidget
from NavApp.scripts.utilities import find_manager


class SwipeableImageWidget(SelectorBehaviorWidget):

    def __init__(self, **kwargs):
        self.do_scroll_y = False
        self.do_scroll_x = True
        self.build_auto = False
        self.button_num = 5
        self.component_width = dp(60)
        self.component_height = dp(58.5)
        self.scroll_x = 0.5
        self.current = 3

        super().__init__(**kwargs)

        self.texts = ["HIKING", "WALKING", "RUNNING", "CYCLING", "SKATING"]
        self.widget_type = (MDLabel, {"text": self.texts, "halign": "center",
                                      "font": None,
                                      "pos_hint": {"center_x": 0.5, "center_y": 0.5},
                                      "size_hint": (1, 1), "font_size": dp(120),
                                      "text_color": "white",
                                      "theme_text_color": "Custom"})

        self.enumerate = True
        self.enumeration_min = 0

    def build_self(self, effect=None):
        super().build_self()
        self.layout.bind(minimum_width=self.layout.setter('width'))
        self.visualise_components()
        self.do_scroll_x = False

    def visualise_components(self):
        for x in range(len(self.components)):
            self.components[x].text = self.texts[x]
            self.components[x].font = self.font
        self.components[self.current - 1].font_size = dp(24)
        self.components[self.current].opacity = 0.5
        self.components[self.current - 2].opacity = 0.5

    def change_current(self, direction):
        self.current += direction

        swipe_animation_bottom = Animation(scroll_x=self.scroll_x + 0.5 * direction,
                                           t="out_cubic", duration=1.)
        swipe_animation_bottom.start(self)

        animation_centered = Animation(font_size=dp(24), opacity=1, duration=1., t="out_cubic")
        animation_peripheral = Animation(font_size=dp(18), opacity=.5, duration=1., t="out_cubic")
        if self.current < len(self.components):
            animation_peripheral.start(self.components[self.current])
        if self.current - 1 > 0:
            animation_peripheral.start(self.components[self.current - 2])
        animation_centered.start(self.components[self.current - 1])

    def get_current(self):
        return self.current
