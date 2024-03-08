import time


class ActivityManager:
    def __init__(self, user_id):
        self.user_id = user_id

        self.activities = {
            "planinarenje": [],
            "hodanje": [],
            "trcanje": [],
            "bicikliranje": [],
            "rolanje": []
        }

    def add_new_activity(self, activity_type):
        activity = Activity(activity_type)
        self.activities[activity_type].append(activity)
        return activity


class Activity:

    def __init__(self, activity_type):
        self.activity_type = activity_type

        self.start_date = None
        self.start_time = 0
        self.elapsed_time_active = 0
        self.elapsed_time_total = 0

        self.location_series = []
        self.speed_series = []
        self.total_distance = 0

    def start_activity(self, start_date, start_time):
        self.start_date = [start_date.tm_year, start_date.tm_mon, start_date.tm_mday,
                           start_date.tm_hour, start_date.tm_min, start_date.tm_sec]
        self.start_time = start_time

    def update_activity(self, dt, location_ping, ):
        self.elapsed_time_active += dt
        self.location_series.append(location_ping)

    def stop_activity(self, end_time):
        self.elapsed_time_total = end_time - self.start_time

    def calculate_average_speed(self):
        pass

    def save_activity(self):
        pass
