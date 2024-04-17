import time
from kivymd.uix.screen import MDScreen


class DailyActivityScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.activity_data = None

    def start_up_screen(self, activity_name, activity_time, activity_data):
        self.activity_data = activity_data
        print(f"Activity data: {activity_data.keys()}")
        self.ids["activity_name"].text = activity_name
        self.ids["activity_time"].text = activity_time
        self.ids["time_quantity"].quantity = time.strftime('%H:%M:%S',
                                                           time.gmtime(round(activity_data["time_elapsed"])))
        self.ids["distance_quantity"].quantity = str(int(activity_data["total_distance"])) + " m"
        self.ids["velocity_quantity"].quantity = str(round(activity_data["average_velocity"], 1)) + " km/h"
        # self.change_labels(activity_type)


    def back_arrow(self):
        self.manager.transition.direction = "right"
        self.manager.goto_screen("mss")
        # not good, should be fired on complete of transition
        mss = self.manager.get_screen("mss")
        # mss.bind(on_enter=mss.reenter_hero)

    def open_map_view(self, activity_data):
        # self.manager.active_user.send_request(path=f"/api/collections/locations/records?filter=(exercise%3D'{activity_data.id}')", success_func=self.fetch_location_success)

        self.manager.transition.direction = "right"
        rms = self.manager.get_screen("rms")
        rms.open_webview()

    def fetch_location_success(self, req, res):
        print(f"Open map response: {dir(res)}")
        print(f"Open map response: {res.keys()}")
