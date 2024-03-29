from kivy.clock import Clock
from kivymd.uix.screen import MDScreen


class WeeklyActivityScreen(MDScreen):
    activity = None
    measurement_type = "inital"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Clock.schedule_once(self.build_self, 0.4)

    def back_arrow(self):
        self.manager.transition.direction = "right"
        self.manager.goto_screen("mss")
        # not good, should be fired on complete of transition
        mss = self.manager.get_screen("mss")
        mss.bind(on_enter=mss.reenter_hero)

    def start_up_screen(self,hero_tag, activity_type):
        self.ids["hero_to"].tag = hero_tag
        self.activity = activity_type
        print(self.activity)
        self.ids["top_bar"].title = activity_type
        self.change_labels(activity_type)

    def change_labels(self, activity):
        if activity in "Hiking, Running, Walking":
            self.measurement_type = "STEPS"
        else:
            self.measurement_type = "KM"

        label = self.ids["label"]
        label.text = self.measurement_type

        quantity_display = self.ids["changeable_unit_quantity"]
        quantity_display.title = self.measurement_type
