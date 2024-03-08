import time

from plyer import gps
from kivy.utils import platform
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from NavApp.scripts.activity_manager import ActivityManager, Activity


class ActivityScreen(Screen):
    current_background = "assets/images/home/home_*_1.png"
    activity_manager: ActivityManager
    active_activity: Activity

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.activities = ["planinarenje", "hodanje", "trcanje", "bicikliranje", "rolanje"]
        self.activity_presets = [1, 2, 2, 3, 3]
        self.presets = {
            1: {"type": 1, "data": ["STEPS", "TIME", "KM", "NET ALTITUDE", "CALORIES"]},
            2: {"type": 1, "data": ["STEPS", "TIME", "KM", "TEMPO", "CALORIES"]},
            3: {"type": 0, "data": ["KM", "TIME", "TEMPO", "CALORIES", "0"]},
        }
        self.current_activity = 1
        Clock.schedule_once(self.further_build, 0.01)

    def further_build(self, dt):
        self.activity_manager = self.manager.active_user.activity_manager
        self.active_activity = None
        self.image_container = self.ids["image_container"]
        self.activity_containers = [
            self.ids["ac1"],
            self.ids["ac2"],
            self.ids["ac3"],
            self.ids["ac4"],
            self.ids["ac5"]
        ]

        self.play_button = self.ids["play_button"]
        self.stop_button = self.ids["stop_button"]

    def start_up_screen(self):
        home_screen = self.manager.get_screen("hme")
        self.current_activity = home_screen.get_current_activity() - 1
        self.image_container.source = self.current_background.replace("*", self.activities[self.current_activity])
        self.set_up_preset()
        if platform == "android":
            gps.configure(on_location=self.update_location)
            gps.start()

    def placeholder(self, *args):
        pass

    def button_released(self, button):
        match button.parent.button_type:
            case "play":
                self.start_activity()
            case "pause":
                self.pause_activity()

    def set_up_preset(self):
        pid = self.activity_presets[self.current_activity]
        preset = self.presets[pid]
        self.activity_containers[-1].opacity = preset["type"]
        self.activity_containers[-2].pos_hint = {"center_x": 0.5 - preset["type"] * 0.25, "center_y": 0.32}
        self.reset_containers(preset)

    def reset_containers(self, preset):
        for c in range(len(self.activity_containers)):
            self.activity_containers[c].quantity = "0"
            self.activity_containers[c].title = preset["data"][c]

    def pause_activity(self):
        self.play_button.button_disabled = True
        self.stop_button.set_button_type("check")
        move_to_back = Animation(pos_hint={"center_x": 0.4}, t="out_cubic", duration=0.5)
        move_to_back.bind(on_complete=self.revisualise_stop_button)
        move_to_back.start(self.play_button)
        self.__pause_activity()

    def revisualise_stop_button(self, pause=True, *args):
        self.stop_button.pos_hint["center_x"] = 0.6
        self.stop_button.opacity = 1
        self.reenable_play_button()

    def reenable_play_button(self, *args):
        self.play_button.button_disabled = False

    def start_activity(self):
        self.play_button.button_disabled = True
        self.stop_button.opacity = 0
        self.stop_button.pos_hint["center_x"] = 1
        move_to_middle = Animation(pos_hint={"center_x": 0.5}, t="in_cubic", duration=0.5)
        move_to_middle.bind(on_complete=self.reenable_play_button)
        move_to_middle.start(self.play_button)
        self.__start_activity()

    def __start_activity(self, dt=0):

        if not self.active_activity:
            self.active_activity = self.activity_manager.add_new_activity(self.activities[self.current_activity])
            self.active_activity.start_activity(time.localtime(), time.perf_counter())
        self.last_ping = time.perf_counter()
        self.activity_event = Clock.schedule_interval(self.update_activity, 1)

    def update_location(self, **kwargs):
        lat = kwargs["lat"]
        lon = kwargs["lon"]
        self.update_location_widget(lat, lon)

    def update_activity(self, dt=0):
        self.dt = round(time.perf_counter() - self.last_ping, 5)
        self.last_ping = time.perf_counter()
        self.active_activity.update_activity(self.dt, ["lokacija"])
        print(self.dt, self.active_activity.elapsed_time_active)
        self.update_time_widget(self.active_activity.elapsed_time_active)

    def update_location_widget(self, latitude, longitude):
        self.activity_containers[2].quantity = f"lat: {latitude} lon: {longitude}"
        print(latitude,longitude)

    def update_time_widget(self, elapsed_time):
        self.activity_containers[1].quantity = time.strftime('%H:%M:%S', time.gmtime(round(elapsed_time)))

    def __pause_activity(self, dt=0):
        self.activity_event.cancel()
        self.update_activity()

    def finish_activity(self, button):
        if self.active_activity:
            print("finalizing activity...")
            self.active_activity = None

    def quit_activity(self, button):
        self.manager.goto_screen("hme")
