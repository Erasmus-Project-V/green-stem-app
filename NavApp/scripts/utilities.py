# find parent manager using while loop with rules
import math

import numpy as np


def find_manager(parent, name="manager"):
    try:
        while hasattr(parent, "parent"):
            parent = parent.parent
            if hasattr(parent, "manager"):
                break
    except AttributeError:
        print("error occured while trying to locate screen manager from top_menu_widget")
        return None
    return parent.manager if parent.manager.name == name else None


def thumbnail_generator():
    print("treba generisati sliku za onaj profile, tj croppat ju")


def euclidean(*args):
    if args[0].__class__ in (tuple, list):
        args = args[0]
    if len(args) < 3:
        args.append(0)
    print(args)
    return (args[0] ** 2 + args[1] ** 2 + args[2] ** 2) ** 0.5


class Vector:

    def __init__(self, *args):
        self.dimension = len(args[0] if args[0].__class__ in (tuple, list) else args)
        self.components = args[0] if args[0].__class__ in (tuple, list) else args

    def expand(self, *args):
        self.dimension += len(args[0] if args[0].__class__ in (tuple, list) else args)
        components_add = args[0] if args[0].__class__ in (tuple, list) else args
        for c in components_add:
            self.components.append(c)

    def get_components(self):
        return list(self.components)

    def get_copy(self):
        return Vector(self.get_components())

    def get_magnitude(self):
        return euclidean(self.components)

    def __mul__(self, other):
        if other.__class__ in (int, float):
            return Vector([self.components[i] * other for i in range(self.dimension)])
        elif other.__class__ == Vector:
            if not other.dimension == self.dimension: raise ArithmeticError(
                f"Tried to multiply vectors of dimensions: {self.dimension} and {other.dimension},"
                f"\n Sentenced to math jail.")
            return sum([self.components[i] * other.components[i] for i in range(self.dimension)])
        else:
            print("no good")

    def __truediv__(self, other):
        if other.__class__ in (int, float):
            return Vector([self.components[i] / other for i in range(self.dimension)])
        elif other.__class__ == Vector:
            raise ArithmeticError("Why are you doing this?")
        else:
            print("no good")

    def __add__(self, other):
        if other.__class__ in (int, float):
            return Vector([self.components[i] + other for i in range(self.dimension)])
        elif other.__class__ == Vector:
            if not other.dimension == self.dimension: raise ArithmeticError(
                f"Tried to add vectors of dimensions: {self.dimension} and {other.dimension},"
                f"\n Sentenced to math jail.")
            return Vector([self.components[i] + other.components[i] for i in range(self.dimension)])
        else:
            raise ArithmeticError("Addition/Subtraction with class Screen not supported")

    def __getitem__(self, item):
        return self.components[item]

    def __setitem__(self, key, value):
        self.components[key] = value

    def cross(self, other):
        if not (self.dimension == 3 and other.dimension == 3):
            raise ArithmeticError("NO!")
        x = self.components[1] * other.components[2] - self.components[2] * other.components[1]
        y = self.components[2] * other.components[0] - self.components[0] * other.components[2]
        z = self.components[0] * other.components[1] - self.components[1] * other.components[0]
        return Vector((x, y, z))

    def __sub__(self, other):
        return self.__add__(other * -1)

    def __str__(self):
        return str(self.components)

    def __round__(self, n=0):
        s = list(self.components)
        for c in range(self.dimension):
            s[c] = round(self.components[c], n)
        return Vector(s)


def getRotationMatrix(gravity: Vector, geomagnetic: Vector):
    A = gravity
    E = geomagnetic

    normsqA = A * A
    g = 9.81
    freeFallGravitySquared = 0.01 * g ** 2
    # check if in freefall (not good)
    if (normsqA < freeFallGravitySquared):
        return False

    H = E.cross(A)

    normH = H.get_magnitude()

    # device in space
    if (normH < 0.1):
        return False

    H = H / H.get_magnitude()
    A = A / A.get_magnitude()

    M = A.cross(H)
    M = M / M.get_magnitude()

    R = [0] * 9
    I = [0] * 9

    for i in range(0, 3):
        R[i] = H[i]
        R[i + 3] = M[i]
        R[i + 6] = A[i]

    E = E / E.get_magnitude()

    c = E * M
    s = E * A

    I[0] = 1
    I[4] = c
    I[5] = s
    I[7] = -s
    I[8] = c

    return R, I


def getOrientation(R):
    values = [0] * 3
    values[0] = math.atan2(R[1], R[4])
    values[1] = math.asin(-R[7])
    values[2] = math.atan2(-R[6], R[8])
    return values


def mat_mul(m1, m2):
    row1_m1_vec = Vector(m1[0:3])
    row2_m1_vec = Vector(m1[3:6])
    row3_m1_vec = Vector(m1[6:9])
    col1_m2_vec = Vector(m2[0], m2[3], m2[6])
    col2_m2_vec = Vector(m2[1], m2[4], m2[7])
    col3_m2_vec = Vector(m2[2], m2[5], m2[8])
    return [
        row1_m1_vec * col1_m2_vec, row1_m1_vec * col2_m2_vec, row1_m1_vec * col3_m2_vec,
        row2_m1_vec * col1_m2_vec, row2_m1_vec * col2_m2_vec, row2_m1_vec * col3_m2_vec,
        row3_m1_vec * col1_m2_vec, row3_m1_vec * col2_m2_vec, row3_m1_vec * col3_m2_vec
    ]


# TODO BROĐANAC
def getRotationMatrixFromOrientation(yaw, pitch, roll):
    c_yaw = math.cos(yaw)
    s_yaw = math.sin(yaw)
    c_pitch = math.cos(pitch)
    s_pitch = math.sin(pitch)
    c_roll = math.cos(roll)
    s_roll = math.sin(roll)
    rotation_pitch = [1, 0, 0,
                      0, c_pitch, -s_pitch,
                      0, s_pitch, c_pitch]
    rotation_yaw = [c_yaw, -s_yaw, 0,
                    s_yaw, c_yaw, 0,
                    0, 0, 1]
    rotation_roll = [c_roll, 0, s_roll,
                     0, 1, 0,
                     -s_roll, 0, c_roll]
    identity_matrix = [
        1, 0, 0,
        0, 1, 0,
        0, 0, 1

    ]
    rotations_stacked = mat_mul(identity_matrix, rotation_yaw)
    rotations_stacked = mat_mul(rotations_stacked, rotation_pitch)
    rotations_stacked = mat_mul(rotations_stacked, rotation_roll)
    rotations_stacked[1] *= -1
    rotations_stacked[3] *= -1
    rotations_stacked[5] *= -1
    rotations_stacked[7] *= -1
    return rotations_stacked


def getInclintation(I):
    return math.atan2(I[5], I[4])


def rotateVector(rotationMatrix, V: Vector):
    m1 = Vector(rotationMatrix[0:3])
    m2 = Vector(rotationMatrix[3:6])
    m3 = Vector(rotationMatrix[6:9])
    vr = Vector(m1 * V, m2 * V, m3 * V)
    return vr


def processMagAcc(field, gravity):
    R, I = getRotationMatrix(gravity, field)
    orientation = getOrientation(R)
    inclintaion = getInclintation(I)
    return Vector(orientation), inclintaion, R


class SensorManager:
    def __init__(self, initial_orientation):
        self.orientation = initial_orientation
        self.position = None
        self.distrust_const = 9.81
        # stabilizing constant - currently low
        self.epsilon = 0.75

    def update_position(self, position):
        if not self.position:
            self.position = position
            return
        # fusion

    def get_measurements_orientation(self, true_orientation: Vector, movement: Vector):
        # TODO - fix when orientation snaps!! -180 > 180
        self.predicted_orientation = self.orientation + movement
        print(f"AM03 PT {self.predicted_orientation * 180 / math.pi}, {true_orientation * 180 / math.pi}")
        print(f"AM03 NORM {self.predicted_orientation * 180 / math.pi}, {true_orientation * 180 / math.pi}")
        self.combined_orientation = true_orientation * self.epsilon + self.predicted_orientation * (1 - self.epsilon)
        self.orientation = (self.combined_orientation + self.orientation) / 2

        return self.orientation


def polarToCartesian(ro, theta, phi):
    theta = math.radians(theta)
    phi = math.radians(phi)
    z = ro * math.cos(theta)
    x = ro * math.sin(theta) * math.cos(phi)
    y = ro * math.sin(theta) * math.sin(phi)
    return Vector(x, y, z)


# pojednostavljenje, trebalo bi štimati do 1500 metara NMV
def getAltitudeFromPressure(p):
    h = 145366.45 * (1 - (p / 1013.25) ** 0.190284)
    return h * 0.3048


class LocationManager:

    def __init__(self, sample_length, initial_location):
        self.averager = [initial_location] * sample_length

    def add(self, data):
        self.averager.pop(0)
        self.averager.append(data)

    def __average(self):
        return sum(self.averager) / len(self.averager)


def average_orientation(o1, o2, w1=0.5):
    o1_sign = o1 / abs(o1)
    o2_sign = o2 / abs(o2)
    if abs(o1) > math.pi:
        o1 = 2 * math.pi * -o1_sign + o1
        o1_sign *= -1
    if abs(o2) > math.pi:
        o2 = 2 * math.pi * -o2_sign + o2
        o2_sign *= -1
    if o1_sign == o2_sign or (abs(o1) < math.pi / 2 and abs(o2) < math.pi / 2):
        average = o1 * w1 + o2 * (1 - w1)
        if abs(average) > math.pi:
            return 2 * math.pi * -average / abs(average) + abs(average)
        return average
    if o1_sign > o2_sign:
        pos = o1
        neg = o2
    else:
        w1 = 1 - w1
        pos = o2
        neg = o1
    average = (2 * math.pi - abs(neg)) * (1 - w1) + pos * w1
    if average > math.pi:
        return (2 * math.pi - abs(average)) * -1
    return average


def convertBearing(bearing):
    if bearing > 180:
        bearing = - 360 + bearing
    return math.radians(bearing)


def low_pass_filter(adata: np.ndarray, bandlimit: int = 1, sampling_rate: int = 10) -> np.ndarray:
    # translate bandlimit from Hz to dataindex according to sampling rate and data size
    bandlimit_index = int(bandlimit * adata.size / sampling_rate)

    fsig = np.fft.fft(adata)

    for i in range(bandlimit_index + 1, len(fsig) - bandlimit_index ):
        fsig[i] = 0

    adata_filtered = np.fft.ifft(fsig)

    return np.real(adata_filtered)

