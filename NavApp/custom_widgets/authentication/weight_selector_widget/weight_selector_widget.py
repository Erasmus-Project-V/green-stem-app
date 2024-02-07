from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivymd.effects.roulettescroll import RouletteScrollEffect
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout
from NavApp.scripts.utilities import find_manager


class WeightSelectorWidget(ScrollView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_value = 0
        self.layout = MDGridLayout(rows=1, padding=0, size_hint=(None, 1))
        self.components = list()
        self.button_num = 200
        self.event = None
        self.component_width = 20
        self.widget_type = (MDLabel, {"text": "|", "halign": "center",
                                      "pos_hint": {"center_x": 0.5, "center_y": 0.5},
                                      "size_hint": (1, 1), "font_size": 80,
                                      "text_color":self.blue_color_container
                                    ,"theme_text_color": "Custom"})
        self.enumerate = False
        self.enumeration_min = 30
        self.do_scroll_y = False
        self.do_scroll_x = True
        self.bindable = None
        #builda se tek kad se inicijalizira da se ne builda nepotrebno svaki puta na učitavanju aplikacije!
        Clock.schedule_once(self.build_self, 0.01)

    def re_argument(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def build_self(self, null):
        self.layout.bind(minimum_width=self.layout.setter('width'))
        for i in range(1, self.button_num + 1):
            encase = MDRelativeLayout(width=self.component_width, size_hint=(None, 1))
            kw = self.widget_type[1]
            kw["text"] = str(i + self.enumeration_min) if self.enumerate else kw["text"]
            kw["font_name"] = self.font
            component = self.widget_type[0](**kw)
            encase.add_widget(component)
            self.components.append(component)
            self.layout.add_widget(encase)
        self.add_widget(self.layout)
        self.effect_x = RouletteScrollEffect(anchor=4, interval=4)
        self.always_overscroll = False
        self.bar_width = 0

    def start_repeatable_intervals(self):
        event = Clock.schedule_interval(self.opacity_refresh_hard, 0.1)
        manager = find_manager(self)
        manager.add_process(event)

    def bind_to_scroll(self,bindable):
        self.bindable = bindable

    def stop_repeatable_intervals(self):
        if self.event:
            self.event.cancel()

    def opacity_refresh_hard(self, dt):
        sx = self.scroll_x
        bottom_normalizer = (1 - sx) * self.width // 2
        top_normalizer = sx * self.width // 2
        center = sx * self.layout.width + bottom_normalizer - top_normalizer
        centered_component = center / self.layout.width * self.button_num
        min_dist = 999
        nearest = 0
        correction_speed_factor = 3
        for i, button in enumerate(self.components):
            dist = abs(centered_component - i)
            if dist>15:
                continue
            button.opacity = 1 / dist ** 0.5
            button.font_size = 40 / dist ** 0.5 if dist >= 0.25 else 80
            if dist < min_dist:
                min_dist = centered_component - i
                nearest = i
        if nearest > 0:
            middle = (center - min_dist * correction_speed_factor - bottom_normalizer + top_normalizer)
            correction = middle / self.layout.width
            self.scroll_x = correction
        self.selected_value = nearest
        if self.bindable:
            self.bindable(self.selected_value)

    def get_selected_value(self):
        return self.selected_value
