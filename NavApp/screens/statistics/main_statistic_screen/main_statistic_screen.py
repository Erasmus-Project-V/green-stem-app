from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.button import Button
from kivymd.uix.label import MDLabel
from custom_widgets.statistics.calendar_widget.calendar_widget import CalendarWidget
from custom_widgets.statistics.activity_history_card_widget.activity_history_card_widget import \
    ActivityHistoryCardWidget

from kivy.metrics import dp
from kivymd.uix.transition import MDSlideTransition, MDFadeSlideTransition

from NavApp.custom_widgets.activity_grid_widget.activity_grid_widget import ActivityGridWidget



class MainStatisticScreen(MDScreen):
    image_root = "assets/images/home/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

        self.active_layout = None
        self.changeable_widget = None

        Clock.schedule_once(self.futher_build, 0.1)

    def futher_build(self,dt):
        self.changeable_widget = self.ids["changeable"]

    def start_up_screen(self):
        if self.active_layout:
            self.changeable_widget.remove_widget(self.active_layout)
            self.active_layout = None
        self.build_hero_panels()

    def placeholder(self,*args):
            pass


    def transit_hero(self, btn):
        self.manager.transition = MDSlideTransition()
        self.manager.current_heroes = ["running_card"]
        self.manager.get_screen("was").ids["hero_to"].tag = "running_card"
        self.manager.current = "was"

    def build_hero_panels(self):
        self.active_layout = ActivityGridWidget(activity_grid_elements=self.hero_activity_presets)
        self.changeable_widget.add_widget(self.active_layout)

    def build_chosen_day(self, btn):
        changeable = self.ids["changeable"]
        self.clean_children()
        self.rectangle_radius = [20, 20, 0, 0]
        self.rectangle_height = dp(200)
        calendar_widget = CalendarWidget(current_month="January", current_year="2024")
        calendar_widget.pos_hint = {"center_x": 0.5, "center_y": 0.81}
        changeable.add_widget(calendar_widget)

        # history_widget = ActivityHistoryCardWidget()
        # history_widget.pos_hint = {"center_x":0.5,"center_y":0.7}
        # changeable.add_widget(history_widget)

    def clean_children(self):
        changeable = self.ids["changeable"]
        children = changeable.children
        for child in children:
            changeable.remove_widget(child)

    def arrow_press(self, btn):
        print("Left arrow pressed")
