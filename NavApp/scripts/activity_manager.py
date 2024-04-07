import json
import math
import time
from math import sin, cos, acos

#  1 is best
DATA_DETAIL = 3


class ActivityManager:
    def __init__(self, user_id, sql_manager):
        self.user_id = user_id
        self.sql_manager = sql_manager

        self.activities = {
            "planinarenje": [],
            "hodanje": [],
            "trcanje": [],
            "bicikliranje": [],
            "rolanje": []
        }

    def add_new_activity(self, activity_type):
        activity = Activity(activity_type, self)
        self.activities[activity_type].append(activity)
        return activity

    def save_activity(self, payload, payload_two):
        payload["user"] = self.user_id
        payload_two["user"] = self.user_id
        self.sql_manager.add_finished_activity(payload, payload_two)


class Activity:

    def __init__(self, activity_type, manager):
        self.activity_type = activity_type
        self.manager = manager

        self.start_date = None
        self.start_time = 0
        self.elapsed_time_active = 0
        self.elapsed_time_total = 0

        self.active_location_series = []
        self.passive_location_series = []
        self.speed_series = []
        self.total_distance = 0

    def start_activity(self, start_date, start_time):
        self.start_date = [start_date.tm_year, start_date.tm_mon, start_date.tm_mday,
                           start_date.tm_hour, start_date.tm_min, start_date.tm_sec]
        self.start_time = start_time

    def update_activity(self, dt, location_ping, distance, avg_velocity):
        self.elapsed_time_active += dt
        print("acitivty is being updated!")
        if location_ping:
            self.active_location_series.append((self.elapsed_time_active, location_ping, distance, avg_velocity))
            self.passive_location_series.append((self.elapsed_time_active, location_ping, distance, avg_velocity))
            self.total_distance = distance

    def reset_active_location(self):
        self.active_location_series = []
        ## trebalo bi naznaciti da je lokacija shifted!

    def stop_activity(self, end_time):
        self.elapsed_time_total = end_time - self.start_time
        self.average_velocity = round(3.6 * self.total_distance / self.elapsed_time_total, 2)
        payload, payload_two = self.wrap_self()
        self.manager.save_activity(payload, payload_two)


    def __format_time(self, tlist):
            for i in range(len(tlist)):
                s = str(tlist[i])
                if len(s) == 1:
                    s = '0' + s
                tlist[i] = s
            return f"{tlist[0]}-{tlist[1]}-{tlist[2]} {tlist[3]}:{tlist[4]}:{tlist[5]}"

    def wrap_self(self):
        payload = {
            "type": self.activity_type,
            "user": None,
            "time_started": self.__format_time(self.start_date),
            "time_elapsed": self.elapsed_time_active,
            "total_distance": self.total_distance,
            "average_velocity": self.average_velocity
        }

        times = []
        lats = []
        lons = []
        velocities = []
        distances = []
        for i in range(0, len(self.passive_location_series), DATA_DETAIL):
            times.append(round(self.passive_location_series[i][0]))
            lats.append(self.passive_location_series[i][1][0])
            lons.append(self.passive_location_series[i][1][1])
            velocities.append(round(self.passive_location_series[i][3] * 3.6))
            distances.append(round(self.passive_location_series[i][2]))

        lat_json = {"time": times, "latitude": lats}
        lon_json = {"time": times, "longitude": lons}
        vel_json = {"time": times, "velocity": velocities}
        dist_json = {"time": times, "distance": distances}

        payload_two = {
            "user": None,
            "exercise": None,
            "latitude": json.dumps(lat_json),
            "longitude": json.dumps(lon_json),
            "velocity": json.dumps(vel_json),
            "distance": json.dumps(dist_json)

        }
        return payload, payload_two
