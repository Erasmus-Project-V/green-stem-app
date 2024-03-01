from kivy.clock import Clock
from kivy.uix.screenmanager import Screen


class ActivityScreen(Screen):
    current_background = "assets/images/home/home_*_1.png"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.activities = ["planinarenje", "hodanje", "trcanje", "bicikliranje", "rolanje"]
        self.activity_presets = [1, 2, 2, 3, 3]
        self.presets = {
            1: {"type": 1, "data": ["STEPS", "TIME", "KM", "NET ALTITUDE", "CALORIES"]},
            2: {"type": 1, "data": ["STEPS", "TIME", "KM", "TEMPO", "CALORIES"]},
            3: {"type": 0, "data": ["KM", "TIME", "TEMPO", "CALORIES","0"]},
        }
        self.current_activity = 1
        Clock.schedule_once(self.further_build,0.1)

    def further_build(self,dt):
        self.image_container = self.ids["image_container"]
        self.activity_containers = [
            self.ids["ac1"],
            self.ids["ac2"],
            self.ids["ac3"],
            self.ids["ac4"],
            self.ids["ac5"]
        ]

    def start_up_screen(self):
        home_screen = self.manager.get_screen("hme")
        self.current_activity = home_screen.get_current_activity() - 1
        self.image_container.source = self.current_background.replace("*", self.activities[self.current_activity])
        self.set_up_preset()

    def set_up_preset(self):
        pid = self.activity_presets[self.current_activity]
        preset = self.presets[pid]
        print(preset["type"])
        self.activity_containers[-1].opacity = preset["type"]
        print(self.activity_containers[-2].pos_hint)
        self.activity_containers[-2].pos_hint = {"center_x":0.5-preset["type"]*0.25,"center_y":0.32}
        for c in range(len(self.activity_containers)):
            self.activity_containers[c].quantity = "0"
            self.activity_containers[c].title = preset["data"][c]
