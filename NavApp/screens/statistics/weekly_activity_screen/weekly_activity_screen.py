from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from scripts.utilities import calculate_steps

class WeeklyActivityScreen(MDScreen):
    activity = None
    measurement_type = "inital"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroller = None

    def back_arrow(self):
        self.manager.transition.direction = "right"
        self.manager.goto_screen("mss")
        self.anim = Animation(opacity=0, duration=0.3)
        self.anim.bind(on_complete=self.return_to_mss)
        self.anim.start(self.scroller)
        # not good, should be fired on complete of transition

    def return_to_mss(self, *args):
        mss = self.manager.get_screen("mss")
        mss.bind(on_enter=mss.reenter_hero)

    def start_up_screen(self, hero_tag, activity_type):
        self.ids["hero_to"].tag = hero_tag
        self.scroller = self.ids["stat_scroller"]
        self.anim = Animation(opacity=1, duration=0.3)
        self.anim.start(self.scroller)
        self.activity = activity_type
        print(self.activity)
        self.ids["top_bar"].title = activity_type
        self.change_labels(activity_type)

    def change_labels(self, activity):
        if activity in "Hiking, Running, Walking":
            self.measurement_type = "DISTANCE"
        else:
            self.measurement_type = "DISTANCE"

        label = self.ids["label"]
        label.text = self.measurement_type

        quantity_display = self.ids["changeable_unit_quantity"]
        quantity_display.title = self.measurement_type

    def receive_activity_data(self,items,n_items):
        print(f"received {n_items}")
        total_distance = 0
        for i in range(n_items):
            total_distance += items[i]["total_distance"]

        height = self.manager.active_user.get_user_attribute("height")
        gender = self.manager.active_user.get_user_attribute("gender")
        total_steps = str(int(calculate_steps(total_distance, gender,height)))
        self.calorie_count = total_steps
        if total_distance > 1000:
            total_distance = str(int(total_distance / 1000)) + " km"
        else:
            total_distance = str(int(total_distance)) + " m"
        self.unit_quantity = total_distance