import math
import time
from time import sleep
from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient
from android.config import SERVICE_CLASS_NAME
from jnius import autoclass
from plyer import gps, accelerometer, compass, gyroscope, gravity, barometer
from scripts.utilities import *

PythonService = autoclass(SERVICE_CLASS_NAME)

# find parent manager using while loop with rules
import math


class BackgroundNavigator:

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
        self.altitude = 0

    def configure_gps(self, is_android):
        if not self.gps_configured:
            gps.configure(on_location=self.update_location)
            self.gps_configured = True
        self.enable_sensors()

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
        self.gps_running = True

    def reset_containers(self):
        self.last_acceleration = Vector(0, 0, 0)
        self.previous_velocity = Vector(0, 0, 0)
        self.filtered_acceleration = Vector(0, 0, 0)
        self.all_velocities = []
        self.previous_locations = []
        self.average_velocity = 0
        self.delta_path = 0
        self.cached_path = 0
        self.last_cached_path = 0
        self.altitude = 0

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
        if not self.last_acceleration:
            self.last_acceleration, self.filtered_acceleration = filterAccelerometerData(rotated_acceleration, dt=dt)
        else:
            self.last_acceleration, self.filtered_acceleration = filterAccelerometerData(rotated_acceleration,
                                                                                         self.filtered_acceleration,
                                                                                         self.last_acceleration,
                                                                                         dt=dt)

        rotated_acceleration[2] = 0.0
        self.all_accelerations.append(rotated_acceleration)

        delta_velocity = rotated_acceleration * dt
        v0 = self.previous_velocity
        v1 = self.previous_velocity + delta_velocity
        self.previous_velocity += delta_velocity
        self.all_velocities.append(self.previous_velocity.get_magnitude())
        ds = (v0 + v1) * dt / 2
        self.delta_path += ds.get_magnitude()
        self.rotated_orientation = rotation_averaged

        return rotation_averaged, rotated_acceleration

    def update_location(self, **kwargs):
        print("updating location...")
        latitude = kwargs["lat"]
        longitude = kwargs["lon"]
        velocity_magnitude = kwargs['speed']
        bearing_gps = kwargs['bearing']
        altitude = kwargs['altitude']
        self.altitude = altitude
        print(kwargs["accuracy"])
        # might make it stricter
        accuracy_factor = 4 / (kwargs['accuracy'] ** 1.25)
        print(accuracy_factor)
        if accuracy_factor > 1:
            accuracy_factor = 1
        elif accuracy_factor < 0.22:
            return

        # take care of runaway velocity
        self.pivot_velocity(velocity_magnitude, bearing_gps)

        # factor of altitude removed from calculations for now
        current_location = Vector(latitude, longitude, altitude)
        self.all_accelerations = []
        self.previous_locations.append((current_location[0], current_location[1], current_location[2], accuracy_factor))
        if len(self.previous_locations) >= 3:
            triangulated_location = Vector(sum([i[0] for i in self.previous_locations]) / 3,
                                           sum([i[1] for i in self.previous_locations]) / 3,
                                           6371000)
            averaged_accuracy = sum([i[-1] for i in self.previous_locations]) / 3
            self.previous_locations = [
                (triangulated_location[0], triangulated_location[1], triangulated_location[2], accuracy_factor)]
        else:
            return

        if self.last_location:
            self.lld = round(self.last_location, 1)

        gps_distance = 0
        if self.last_location:
            gps_distance = coordinate_distance_calculator(lat1=self.last_location[0], lon1=self.last_location[1],
                                                          lat2=triangulated_location[0], lon2=triangulated_location[1])
        self.last_location = triangulated_location
        print(
            f"AM04 delta path: {self.cached_path-self.last_cached_path}, gps_distance {gps_distance} average velocity {self.average_velocity}, "
            f"weighed {(1-averaged_accuracy)*(self.cached_path-self.last_cached_path) + averaged_accuracy*gps_distance}, {averaged_accuracy}")
        if self.cached_path - self.last_cached_path > 1:
            self.cached_path = self.last_cached_path + (1 - averaged_accuracy) * (
                    self.cached_path - self.last_cached_path) + averaged_accuracy * gps_distance
        self.last_cached_path = self.cached_path

    def pivot_velocity(self, velocity_magnitude, bearing_gps):
        if self.last_location_ping > 10:
            self.last_location_ping = time.perf_counter() - self.last_location_ping
        else:
            self.last_location_ping = 1

        if bearing_gps > 180:
            bearing_gps = -360 + bearing_gps
        bearing_gps = math.radians(bearing_gps)
        self.bearing_ref = bearing_gps
        self.previous_velocity = Vector(math.sin(bearing_gps), math.cos(bearing_gps), 0) * velocity_magnitude

        if self.all_velocities:
            average_velocity = sum(self.all_velocities) / len(self.all_velocities)
            self.all_velocities.clear()
        else:
            average_velocity = 0

        if 0.3 < self.delta_path and 0.3 < average_velocity < 10:
            self.cached_path += round(self.delta_path, 2)
        self.delta_path = 0
        self.average_velocity = average_velocity

        self.last_location_ping = time.perf_counter()

    def clear_cache(self):
        self.cached_path = 0

    def get_avg_velocity(self):
        return self.average_velocity

    def get_cached_path(self):
        return self.cached_path

    def stop_gps(self):
        if not self.gps_running:
            return False
        gps.stop()
        self.gps_running = False

    def run(self):
        self.server = OSCThreadServer()
        self.server.listen('localhost', port=3000, default=True)
        self.client = OSCClient('localhost', 3002)
        self.mService = PythonService.mService

        self.loop_running = True
        self.paused = True

        self.server.bind(b'/terminate', self.terminate)
        self.server.bind(b'/resume', self.resume)
        self.server.bind(b'/pause', self.pause)
        self.server.bind(b'/reset', self.reset)

        self.configure_gps(True)
        self.enable_sensors()
        sleep(1)
        self.client.send_message(b'/receive_data', [100])
        start_time = time.perf_counter() - 0.1
        counter = 0
        dt = 0
        while self.loop_running:
            counter += 1
            dt0 = time.perf_counter() - start_time
            if not self.paused:
                self.update_acceleration(dt0)
            dt += dt0
            start_time = time.perf_counter()
            sleep(0.1)
            if counter == 10:
                if not self.paused:
                    print("sending update!")
                    argument = f'{dt}A{self.last_location}A{self.cached_path}A{self.average_velocity}A{self.altitude}'
                    print(argument)
                    self.client.send_message(b'/receive_navdata',argument.encode('ascii'))
                dt = 0
                counter = 0

        self.mService.stopSelf()

    def pause(self):
        self.paused = True
        self.stop_gps()

    def resume(self):
        self.paused = False
        self.start_gps(1000, 1)

    def reset(self):
        self.reset_containers()

    def terminate(self):
        self.loop_running = False
        self.stop_gps()
        self.disable_sensors()
        self.server.close()


BackgroundNavigator().run()
