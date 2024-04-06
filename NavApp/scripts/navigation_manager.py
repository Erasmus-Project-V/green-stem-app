import math
import time

from kivy.clock import Clock
from plyer import gps, accelerometer, compass, gyroscope, gravity, barometer
from scripts.utilities import *


class NavigationManager:

    def __init__(self):
        self.bearing_ref = None
        self.gps_configured = False
        self.gps_running = False
        self.calibrated = False
        self.accelerometer_event = None

        self.last_location = None
        self.last_location_lat_lon = None

        self.previous_velocity = Vector(0, 0, 0)
        self.rotated_orientation = Vector(0, 0, 0)
        self.all_velocities = []
        self.all_accelerations = []
        self.last_location_ping = time.perf_counter()
        self.lld = None
        self.previous_locations = []

        self.last_acceleration = None
        self.filtered_acceleration = None

        self.delta_path = 0
        self.cached_path = 0
        self.last_cached_path = 0
        self.average_velocity = 0




    def calculate_steps(self, delta_path, gender, height):
        # za sada bez brzine, nije dovoljno tocna
        c1 = 0.415 if gender == "male" else 0.413
        stride_length = c1 * height / 100
        steps = delta_path / stride_length
        return steps

    def calculate_calories(self, delta_time, delta_path, weight, type="hodanje"):
        # constants calculated by manual linear regression
        c = {
            "hodanje": (1.344, -3.452, 2.6),
            "trcanje": (1.344, -3.452, 2.6),
            "bicikliranje": (0.375, 0.2, 5),
            "rolanje": (0.691, -2.445, 3),
            "planinarenje": (1.344, -1.452, 1.6)

        }
        if delta_time == 0:
            delta_time = 1
        c0 = c[type]
        speed = delta_path / delta_time * 3.6
        if speed < c0[2]:
            return 0
        MET = c0[0] * speed + c0[1]
        calories_burned = MET * 3.5 * weight / (200*60) * delta_time
        return calories_burned

