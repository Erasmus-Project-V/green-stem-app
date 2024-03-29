from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.button import Button
from kivymd.uix.label import MDLabel
from custom_widgets.statistics.calendar_widget.calendar_widget import CalendarWidget
from custom_widgets.statistics.activity_history_card_widget.activity_history_card_widget import \
    ActivityHistoryCardWidget
from custom_widgets.statistics.activity_history_list_widget.activity_history_list_widget import \
    ActivityHistoryListWidget
from kivy.metrics import dp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.transition import MDSlideTransition, MDFadeSlideTransition

from NavApp.custom_widgets.activity_grid_widget.activity_grid_widget import ActivityGridWidget


class MainStatisticScreen(MDScreen):
    image_root = "assets/images/home/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initialized = False
        self.hero_activity_presets = [{"text": "Running", "img_path": f"{self.image_root}home_trcanje_1.png",
                                       "hero_tag": "running_card", "release_func": self.transit_hero},
                                      {"text": "Cycling", "img_path": f"{self.image_root}home_bicikliranje_1.png",
                                       "hero_tag": "cycling_card", "release_func": self.transit_hero},
                                      {"text": "Hiking", "img_path": f"{self.image_root}home_planinarenje_1.png",
                                       "hero_tag": "hiking_card", "release_func": self.transit_hero},
                                      {"text": "Walking", "img_path": f"{self.image_root}home_hodanje_1.png",
                                       "hero_tag": "walking_card", "release_func": self.transit_hero},
                                      {"text": "Skating", "img_path": f"{self.image_root}home_rolanje_1.png",
                                       "hero_tag": "skating_card", "release_func": self.transit_hero}]

        self.ref_nav = {"Chosen day": "day", "This week": "week_month", "This month": "week_month"}
        self.layouts = {
            "day": CalendarWidget(current_month="January", current_year="2024"),
            "week_month": ActivityGridWidget(activity_grid_elements=self.hero_activity_presets),
        }


        self.build_references = {
            "day": self.build_chosen_day,
            "week_month": self.build_hero_panels
        }

        self.active_layout = None
        self.changeable_widget = None

        Clock.schedule_once(self.futher_build, 0.1)

    def futher_build(self, dt):
        self.changeable_widget = self.ids["changeable"]

    def start_up_screen(self):
        if self.initialized:
            return
        self.destroy_old_layout()
        self.manager.tamper_hero_data(self.layouts["week_month"])
        self.build_hero_panels()
        self.initialized = True

    def destroy_old_layout(self):
        if self.active_layout:
            self.changeable_widget.remove_widget(self.active_layout)
            self.active_layout = None

    def change_state(self, btn):
        layout = self.ref_nav[btn.name]
        self.destroy_old_layout()
        self.build_references[layout]()

    def placeholder(self, *args):
        pass

    def _transit_hero(self, *args):
        hero_tag = self.current_hero_tag
        self.manager.transition = MDSlideTransition()
        self.manager.current_heroes = [hero_tag]
        was = self.manager.get_screen("was")
        was.start_up_screen(self.current_hero_tag, self.current_activity_type)
        # goto screen doesnt work
        self.manager.current = "was"

    def transit_hero(self, btn):
        self.current_hero_tag = btn.hero_tag
        self.current_activity_type = btn.activity_type
        x = self.active_layout.nav_ref[btn.hero_tag].ids.front_box
        anim = Animation(opacity=0, duration=0.2)
        anim.bind(on_complete=self._transit_hero)
        anim.start(x)

    def reenter_hero(self, *args):
        anim = Animation(opacity=1, duration=0.2)
        anim.start(self.active_layout.nav_ref[self.current_hero_tag].ids.front_box)
        self.unbind(on_enter=self.reenter_hero)

    def build_hero_panels(self):
        self.active_layout = self.layouts["week_month"]
        self.changeable_widget.add_widget(self.active_layout)
        self.changeable_widget.manager = self.manager

    def build_chosen_day(self):
        changeable = self.ids["changeable"]
        self.rectangle_radius = [20, 20, 0, 0]
        self.rectangle_height = dp(200)
        calendar_widget = self.layouts["day"]
        calendar_widget.pos_hint = {"center_x": 0.5, "center_y": 0.85}
        changeable.add_widget(calendar_widget)
        self.active_layout = calendar_widget

        # history_widget = ActivityHistoryCardWidget()
        # history_widget.pos_hint = {"center_x":0.5,"center_y":0.5}
        # changeable.add_widget(history_widget)
        history_list = ActivityHistoryListWidget()
        history_list.activity_history_elements = [
            {"img_path": "assets/images/home/home_trcanje_1.png", "activity_time": "11:22", "activity_name": "Trcanje"},
            {"img_path": "assets/images/home/home_trcanje_1.png", "activity_time": "11:22", "activity_name": "Trcanje"},
            {"img_path": "assets/images/home/home_trcanje_1.png", "activity_time": "11:22", "activity_name": "Trcanje"},
            {"img_path": "assets/images/home/home_trcanje_1.png", "activity_time": "11:22", "activity_name": "Trcanje"},
            {"img_path": "assets/images/home/home_trcanje_1.png", "activity_time": "11:22", "activity_name": "Trcanje"},
            {"img_path": "assets/images/home/home_trcanje_1.png", "activity_time": "11:22", "activity_name": "Trcanje"},
        ]
        history_list.pos_hint = {"center_x": 0.5, "center_y": 0.48}
        changeable.add_widget(history_list)

    def clean_children(self):
        changeable = self.ids["changeable"]
        children = changeable.children
        for child in children:
            changeable.remove_widget(child)

    def arrow_press(self, btn):
        print("Left arrow pressed")
