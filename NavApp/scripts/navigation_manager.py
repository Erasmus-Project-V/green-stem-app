from kivy.clock import Clock
from plyer import gps, accelerometer, compass, gyroscope, gravity, barometer
from scripts.utilities import *


class NavigationManager:

    def __init__(self):
        self.gps_configured = False
        self.gps_running = False
        self.calibrated = False
        self.accelerometer_event = None

        self.last_location = None
        self.last_location_lat_lon = None

        self.previous_velocity = Vector(0, 0, 0)
        self.all_velocities = []

        self.delta_path = 0
        self.cached_path = 0
        self.average_velocity = 0

    def configure_gps(self,auth_method,is_android):
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

    # TODO: Add compensation for wobble and filter out unfiltered bad gps
    # Z axis - out of device , Y - along the length, X - along the width
    def update_acceleration(self, dt):
        acceleration_vector = Vector(accelerometer.acceleration)
        compass_vector = Vector(compass.field)

        gyroscope_velocity = Vector(gyroscope.rotation)
        gyroscope_movement = gyroscope_velocity * dt

        gravity_vector = Vector(gravity.gravity)
        raw_acceleration = acceleration_vector - gravity_vector

        orientation, inclination, rotation_matrix = processMagAcc(compass_vector, gravity_vector)
        rotated_acceleration = rotateVector(rotation_matrix, raw_acceleration)

        delta_velocity = rotated_acceleration * dt

        v0 = self.previous_velocity
        v1 = self.previous_velocity + delta_velocity
        self.previous_velocity += delta_velocity
        print(f"AM03 AverageVelocity {self.previous_velocity.get_magnitude()}")

        self.all_velocities.append(self.previous_velocity.get_magnitude())
        self.delta_path += (v0.get_magnitude() + v1.get_magnitude()) * dt / 2

        return orientation, rotated_acceleration

    def update_location(self, **kwargs):
        print(f"KW00 {kwargs}")
        latitude = kwargs["lat"]
        longitude = kwargs["lon"]
        velocity_magnitude = kwargs['speed']
        bearing_gps = kwargs['bearing']
        altitude = kwargs['altitude']

        # might make it stricter
        accuracy_factor = 5 / (kwargs['accuracy'])
        if accuracy_factor > 1:
            accuracy_factor = 1

        location_vector = polarToCartesian(6378137 + altitude, latitude, longitude)
        self.last_location_lat_lon = (latitude, longitude, altitude)

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
        if self.delta_path > 0.5 and 0.3 < average_velocity < 10:
            print(f"AM04 delta path: {self.delta_path}, gps_distance {gps_distance} average velocity {average_velocity},")
            self.cached_path += round(self.delta_path, 2)
            self.average_velocity = average_velocity

        self.previous_velocity = Vector(math.cos(bearing_gps), math.sin(bearing_gps), 0) * velocity_magnitude
        self.delta_path = 0

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
    def calibrate_sensors(self,dt):
        pass
