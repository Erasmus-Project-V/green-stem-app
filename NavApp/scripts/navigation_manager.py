import math
import time

import numpy as np
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

        self.delta_path = 0
        self.cached_path = 0
        self.average_velocity = 0

    def configure_gps(self, auth_method, is_android):
        if not self.gps_configured:
            gps.configure(on_location=self.update_location,
                          on_status=auth_method)
            self.gps_configured = True
        self.enable_sensors()
        Clock.schedule_once(self.calibrate_sensors, 1)

    def enable_sensors(self):
        accelerometer.enable()
        compass.enable()
        gravity.enable()
        gyroscope.enable()

    def disable_sensors(self):
        accelerometer.disable()
        compass.disable()
        gravity.disable()
        gyroscope.disable()

    def start_gps(self, min_time, min_dist):
        self.last_location = None
        self.last_location_lat_lon = None
        gps.start(minTime=1000, minDistance=min_dist)
        self.accelerometer_event = Clock.schedule_interval(self.update_acceleration, 0.1)
        self.gps_running = True

    # TODO: Add compensation for wobble and filter out bad gps
    # Z axis - out of device , Y - along the length, X - along the width
    def update_acceleration(self, dt):
        acceleration_vector = Vector(accelerometer.acceleration)
        compass_vector = Vector(compass.field)

        gyroscope_velocity = Vector(gyroscope.rotation)
        if gyroscope_velocity:
            gyroscope_movement = gyroscope_velocity * dt
        else:
            gyroscope_movement = Vector(0, 0, 0)
        gyroscope_movement_rad = gyroscope_movement * math.pi / 180

        gravity_vector = Vector(gravity.gravity)
        raw_acceleration = acceleration_vector - gravity_vector

        orientation, inclination, rotation_matrix = processMagAcc(compass_vector, gravity_vector)
        if self.rotated_orientation[0]:
            predicted_orientation = self.rotated_orientation + gyroscope_movement_rad
        else:
            predicted_orientation = orientation

        rotation_averaged = [0, 0, 0]
        for i in range(3):
            try:
                rotation_averaged[i] = round(average_orientation(predicted_orientation[i], orientation[i], w1=0.9), 2)
            except:
                rotation_averaged[i] = orientation[i]
        rotation_averaged = Vector(rotation_averaged)

        # not functioning
        rotation_matrix_smoothened = getRotationMatrixFromOrientation(rotation_averaged[0], rotation_averaged[1],
                                                                      rotation_averaged[2])

        rotated_acceleration = rotateVector(rotation_matrix_smoothened, raw_acceleration)
        rotated_acceleration = round(rotated_acceleration, 2)

        self.all_accelerations.append(rotated_acceleration)
        print(rotated_acceleration)

        delta_velocity = rotated_acceleration * dt
        VELOCITY_TRESH = 0.2
        if delta_velocity.get_magnitude() > VELOCITY_TRESH:
            print(f"AM00 ERROR VELOCITY: {delta_velocity}")
            delta_velocity = Vector(0, 0, 0)
        v0 = self.previous_velocity
        v1 = self.previous_velocity + delta_velocity
        self.previous_velocity += delta_velocity
        self.all_velocities.append(self.previous_velocity.get_magnitude())
        self.delta_path += (v0.get_magnitude() + v1.get_magnitude()) * dt / 2
        self.rotated_orientation = rotation_averaged

        return rotation_averaged, rotated_acceleration

    def update_location(self, **kwargs):
        self.last_location_ping = time.perf_counter() - self.last_location_ping
        print(f"KW00 {kwargs}")
        latitude = kwargs["lat"]
        longitude = kwargs["lon"]
        velocity_magnitude = kwargs['speed']
        bearing_gps = kwargs['bearing']
        altitude = kwargs['altitude']

        # might make it stricter
        accuracy_factor = 25 / (kwargs['accuracy']**2)
        if accuracy_factor > 1:
            accuracy_factor = 1

        location_vector = polarToCartesian(6378137 + altitude, latitude, longitude)
        self.last_location_lat_lon = (latitude, longitude, altitude)
        self.all_accelerations = []


        # jednostavna korekcija ovisno o preciznosti lokacije - treba prepraviti
        if self.last_location:
            location_vector = location_vector * accuracy_factor + self.last_location * (1 - accuracy_factor)
        elif accuracy_factor < 0.25:
            return

        gps_distance = 0
        if self.last_location:
            gps_distance = (location_vector - self.last_location).get_magnitude()
        self.last_location = location_vector
        if self.all_velocities:
            average_velocity = sum(self.all_velocities) / len(self.all_velocities)
            self.all_velocities.clear()
        else:
            average_velocity = 0
        print(
            f"AM04 delta path: {self.delta_path}, gps_distance {gps_distance} average velocity {average_velocity}, "
            f"predicted velocity: {average_velocity*self.last_location_ping}, {self.last_location_ping}")
        if 0.3 < self.delta_path and 0.3 < average_velocity < 10:
            self.delta_path = min(self.delta_path,average_velocity * self.last_location_ping)
            if abs(gps_distance-self.delta_path) < 1:
                self.cached_path += round(self.delta_path*0.5 + gps_distance*0.5,2)
            else:
                self.cached_path += round(self.delta_path, 2)
            self.average_velocity = average_velocity

        if bearing_gps > 180:
            bearing_gps = -360 + bearing_gps
        bearing_gps = math.radians(bearing_gps)
        self.bearing_ref = bearing_gps
        self.previous_velocity = Vector(math.sin(bearing_gps), math.cos(bearing_gps), 0) * velocity_magnitude
        self.delta_path = 0
        self.last_location_ping = time.perf_counter()


    def clear_cache(self):
        self.cached_path = 0

    def get_avg_velocity(self):
        return self.average_velocity

    def get_location_polar(self):
        return self.last_location_lat_lon

    def get_cached_path(self):
        return self.cached_path

    def stop_gps(self):
        if self.gps_running:
            return False
        gps.stop()
        self.accelerometer_event.cancel()
        self.gps_running = False

    # TODO
    def calibrate_sensors(self, dt):
        pass
