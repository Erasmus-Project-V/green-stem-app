from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.relativelayout import MDRelativeLayout

from scripts.utilities import find_manager


class SelectorBehaviorWidget(ScrollView):
    # MUST DEFINE
    enumerate: bool
    enumeration_min: int
    button_num: int = 10
    component_width: float | int
    component_height: float | int
    widget_type: tuple = None
    build_auto: bool = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repeatable_event = None
        self.bindable_event = None

        if self.do_scroll_x:
            self.layout = MDGridLayout(rows=1, padding=0, size_hint=(None, 1))
            self.encase_kwargs = {"width": self.component_width, "size_hint": (None, 1)}
        else:
            self.layout = MDGridLayout(cols=1, padding=0, size_hint=(1, None))
            self.encase_kwargs = {"height": self.component_height, "size_hint": (1, None)}
        self.components = list()
        self.selected_value = 0
        if self.build_auto:
            Clock.schedule_once(self.build_self, 0.01)

    def re_argument(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def build_self(self, effect=None):

        for i in range(1, self.button_num + 1):
            encase = MDRelativeLayout(**self.encase_kwargs)
            component_kwargs = self.widget_type[1]
            component_kwargs["text"] = str(i + self.enumeration_min) if self.enumerate else component_kwargs["text"]
            component_kwargs["font_name"] = self.font
            component = self.widget_type[0](**component_kwargs)
            encase.add_widget(component)
            self.components.append(component)
            self.layout.add_widget(encase)

        self.add_widget(self.layout)
        self.bar_width = 0
        self.always_overscroll = False

    def start_repeatable_intervals(self):
        self.repeatable_event = Clock.schedule_interval(self.opacity_refresh_hard, 0.1)
        manager = find_manager(self)
        manager.add_process(self.repeatable_event)

    def bind_to_scroll(self, bindable):
        self.bindable_event = bindable

    def stop_repeatable_intervals(self):
        if self.repeatable_event:
            self.repeatable_event.cancel()

    def opacity_refresh_hard(self, dt):
        min_dist = 999
        correction_speed_factor = 3
        render_limit = 10
        default_size = 80

        if self.do_scroll_x:
            scroll_perc = self.scroll_x
            self_dim = self.width
            layout_dim = self.layout.width
        else:
            scroll_perc = 1 - self.scroll_y
            self_dim = self.height
            layout_dim = self.layout.height

        bottom_normalizer = (1 - scroll_perc) * self_dim // 2
        top_normalizer = scroll_perc * self_dim // 2
        center = scroll_perc * layout_dim + bottom_normalizer - top_normalizer
        centered_component = center / layout_dim * self.button_num

        nearest = 0
        for i, button in enumerate(self.components):
            dist = abs(centered_component - i)
            if dist > render_limit:
                continue
            button.opacity = 1 / dist ** 0.5
            button.font_size = 0.5 * default_size / dist ** 0.5 if dist >= 0.25 else default_size
            if dist < min_dist:
                min_dist = centered_component - i
                nearest = i
        if nearest > 0:
            middle = (center - min_dist * correction_speed_factor - bottom_normalizer + top_normalizer)
            if self.do_scroll_x:
                correction = middle / layout_dim
                self.scroll_x = correction
            else:
                correction = (1 - middle / layout_dim)
                self.scroll_y = correction
        self.selected_value = nearest
        if self.bindable_event:
            self.bindable_event(self.enumeration_min + self.selected_value)

    def get_selected_value(self):
        return self.enumeration_min + self.selected_value
