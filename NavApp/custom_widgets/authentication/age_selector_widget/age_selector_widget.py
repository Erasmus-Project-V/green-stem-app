from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivymd.effects.roulettescroll import RouletteScrollEffect
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout
from NavApp.scripts.utilities import find_manager


class AgeSelectorWidget(ScrollView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_value = 0
        self.event = None
        self.bindable = None
        self.layout = MDGridLayout(cols=1, padding=0, size_hint=(1, None))
        self.components = list()
        self.button_num = 40
        self.component_height = 58.5
        self.widget_type = (MDLabel, {"text": "Null", "halign": "center",
                                      "pos_hint": {"center_x": 0.5, "center_y": 0.5},
                                      "size_hint": (1, 1), "font_size": 80})
        self.enumerate = True
        self.enumeration_min = 11
        self.do_scroll_x = False
        Clock.schedule_once(self.build_self, 0.01)

    def re_argument(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def build_self(self, null):
        self.layout.bind(minimum_height=self.layout.setter('height'))
        for i in range(1, self.button_num + 1):
            encase = MDRelativeLayout(height=self.component_height, size_hint=(1, None))
            kw = self.widget_type[1]
            kw["text"] = str(i + self.enumeration_min) if self.enumerate else kw["text"]
            kw["font_name"] = self.font
            component = self.widget_type[0](**kw)
            encase.add_widget(component)
            self.components.append(component)
            self.layout.add_widget(encase)
        self.add_widget(self.layout)
        self.effect_y = RouletteScrollEffect(anchor=4, interval=4)
        self.always_overscroll = False
        self.bar_width = 0


    def start_repeatable_intervals(self):
        self.event = Clock.schedule_interval(self.opacity_refresh_hard, 0.1)
        manager = find_manager(self)
        manager.add_process(self.event)

    def bind_to_scroll(self,bindable):
        self.bindable = bindable

    def stop_repeatable_intervals(self):
        if self.event:
            self.event.cancel()

    def opacity_refresh_hard(self, dt):
        sy = 1 - self.scroll_y
        bottom_normalizer = (1 - sy) * self.height // 2
        top_normalizer = sy * self.height // 2
        center = sy * self.layout.height + bottom_normalizer - top_normalizer
        centered_component = center / self.layout.height * self.button_num
        min_dist = 999
        nearest = 0
        correction_speed_factor = 3
        for i, button in enumerate(self.components):
            dist = abs(centered_component - i)
            if dist>self.button_num/10:
                continue
            button.opacity = 1 / dist ** 0.5
            button.font_size = 40 / dist ** 0.5 if dist >= 0.25 else 80
            if dist < min_dist:
                min_dist = centered_component - i
                nearest = i
        if nearest > 0:
            middle = (center - min_dist * correction_speed_factor - bottom_normalizer + top_normalizer)
            correction = (1 - middle / self.layout.height)
            self.scroll_y = correction
        self.selected_value = nearest
        if self.bindable:
            self.bindable(self.selected_value)

    def get_selected_value(self):
        return self.selected_value
