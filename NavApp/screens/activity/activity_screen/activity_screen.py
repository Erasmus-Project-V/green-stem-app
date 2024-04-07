import math
import time
from kivy.properties import StringProperty
from kivy.uix.screenmanager import FadeTransition
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer
from plyer import gps, accelerometer, compass, gyroscope, gravity, barometer
from kivy.utils import platform
from kivy.animation import Animation
from kivy.clock import Clock
from scripts.activity_manager import ActivityManager, Activity

from scripts.navigation_manager import NavigationManager

if platform == "android":
    from jnius import autoclass
    from android import mActivity

MIN_MEASURE_DISTANCE = 10


class ActivityScreen(MDScreen):
    current_background = "assets/images/home/home_*_1.png"
    activity_manager: ActivityManager
    active_activity: Activity
    last_location_debug = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.activities = ["planinarenje", "hodanje", "trcanje", "bicikliranje", "rolanje"]
        self.activity_presets = [1, 2, 2, 3, 3]
        self.presets = {
            1: {"type": 1, "data": ["STEPS", "TIME", "DISTANCE", "ALTITUDE", "CALORIES"]},
            2: {"type": 1, "data": ["STEPS", "TIME", "DISTANCE", "SPEED", "CALORIES"]},
            3: {"type": 0, "data": ["DISTANCE", "TIME", "SPEED", "CALORIES", "0"]},
        }
        self.update_methods = {
            1: self.update_mountaineering,
            2: self.update_walk,
            3: self.update_wheel
        }
        self.current_activity = 1
        Clock.schedule_once(self.further_build, 0.01)

        self.last_location_debug = "None"
        self.navigator = None

        server = OSCThreadServer()
        server.listen(address=b'localhost', port=3002, default=True)
        server.bind(b'/receive_data', self.receive_data)
        server.bind(b'/receive_navdata',self.receive_navdata)
        self.client = OSCClient(b'localhost', 3000)


        self.last_location = None
        self.cached_path = 0
        self.average_velocity = 0
        self.altitude = 0

    def further_build(self, dt):

        self.active_activity: Activity = None
        self.location_on = False
        self.sensor_manager = None
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

        self.navigator = NavigationManager()

    def on_auth_status(self, general_status, status_message):
        if general_status == "provider_enabled":
            pass
        else:
            self.open_gps_access_popup()

    def open_gps_access_popup(self):
        dialog = MDDialog(title="GPS Error", text="Please enable GPS to continue!")
        dialog.size_hint = [.8, .8]
        dialog.pos_hint = {"center_x": .5, "center_y": .5}
        dialog.bind(on_dismiss=lambda *args: self.quit_activity)
        dialog.open()

    def get_service_name(self):
        context = mActivity.getApplicationContext()
        return str(context.getPackageName()) + '.Service' + 'Navigator'

    def start_service(self):
        if platform == "android":
            service = autoclass(self.get_service_name())
            argument = autoclass("android.content.pm.ServiceInfo")
            service.start(mActivity, 'img' ,'NavApp' ,'Navigation is active' , str(argument.FOREGROUND_SERVICE_TYPE_LOCATION))
            self.service = service
            print("service started!")

    def stop_service(self):
        if platform == "android":
            self.client.send_message(b'/terminate', [])

    def receive_data(self, message="null"):
        print(f"OSCPY Recieved message: {message}")
        if message == 100:
            self.play_button.button_disabled = False

    def receive_navdata(self, *args):
        res = ''.join(map(chr, args))
        print(f"received data {res}")
        subres = res.split("A")
        dt = float(subres[0])
        ll = subres[1]
        if ll != "None":
            ll = tuple(map(float,ll[1:-1].replace(" ","").split(",")))
        else:
            ll = None
        print(ll)
        cp = float(subres[2])
        avg_vel = float(subres[3])
        alt = float(subres[4])
        self.last_location = ll
        self.cached_path = cp
        self.average_velocity = avg_vel
        self.altitude = alt
        if self.active_activity:
            self.update_activity(dt)

    def start_up_screen(self):
        home_screen = self.manager.get_screen("hme")
        self.activity_manager = self.manager.active_user.activity_manager
        self.current_activity = home_screen.get_current_activity() - 1
        self.image_container.source = self.current_background.replace("*", self.activities[self.current_activity])
        self.set_up_preset()
        if platform == "android":
            self.play_button.button_disabled = True
            # imam pojma otkud se android importa, ne ici instalirati!!!
            from android.permissions import Permission, request_permissions
            print("imported!")

            def callback(permission, results):
                if not False in results:
                    print("Got all permissions!")
                    self.start_service()
                else:
                    self.open_gps_access_popup()

            request_permissions([Permission.ACCESS_COARSE_LOCATION,
                                 Permission.ACCESS_FINE_LOCATION], callback)



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
            print(self.activity_manager)
            self.active_activity = self.activity_manager.add_new_activity(self.activities[self.current_activity])
            self.active_activity.start_activity(time.localtime(), time.perf_counter())
        if platform == "android":
            self.client.send_message(b'/resume',[])

    def __pause_activity(self, dt=0):
        self.update_activity()
        if platform == "android":
            self.active_activity.reset_active_location()
            self.client.send_message(b'/pause',[])




    def update_activity(self, dt=0.0):
        self.active_activity.update_activity(dt, self.last_location, self.cached_path, self.average_velocity)
        self.update_widgets(self.active_activity.elapsed_time_active,
                            self.cached_path)

    def update_walk(self, elapsed_distance, gender, height):
        self.activity_containers[0].quantity = str(
            int(self.navigator.calculate_steps(elapsed_distance, gender, height)))
        self.activity_containers[2].quantity = str(int(elapsed_distance)) + "m"
        self.activity_containers[3].quantity = str(int(self.average_velocity * 36) / 10) + "km/h"

    def update_mountaineering(self, elapsed_distance, gender, height):
        self.activity_containers[0].quantity = str(
            int(self.navigator.calculate_steps(elapsed_distance, gender, height)))
        self.activity_containers[2].quantity = str(int(elapsed_distance)) + "m"
        self.activity_containers[3].quantity = str(int(self.altitude)) + "m"

    def update_wheel(self, elapsed_distance, gender, height):
        self.activity_containers[0].quantity = str(int(elapsed_distance)) + "m"
        self.activity_containers[2].quantity = str(int(self.average_velocity * 36) / 10) + "km/h"

    def update_widgets(self, elapsed_time, elapsed_distance):
        self.activity_containers[1].quantity = time.strftime('%H:%M:%S', time.gmtime(round(elapsed_time)))
        gender = self.manager.active_user.get_user_attribute("gender")
        height = self.manager.active_user.get_user_attribute("height")
        weight = self.manager.active_user.get_user_attribute("weight")
        calories = int(self.navigator.calculate_calories(elapsed_time, elapsed_distance, weight,
                                                             self.activities[self.current_activity]))
        self.activity_containers[-1].quantity = str(calories)
        self.update_methods[self.activity_presets[self.current_activity]](elapsed_distance, gender, height)

    def finish_activity(self, button):
        if self.active_activity:
            self.client.send_message(b'/reset',[])
            print("finalizing activity...")
            self.reset_containers(self.presets[self.activity_presets[self.current_activity]])
            self.active_activity.stop_activity(time.perf_counter())
            self.active_activity = None

    def quit_activity(self, button=None, *args):
        if platform == "android":
            self.stop_service()
        self.manager.transition = FadeTransition()
        self.manager.goto_screen("hme")
