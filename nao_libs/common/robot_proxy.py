import math
import time

import motion
from naoqi import ALProxy
import almath
from nao_libs.common import constants


# Singleton for proxies
class Proxies(object):
    _motion_proxy = None
    _posture_proxy = None

    def __new__(cls):
        if cls._motion_proxy is None:
            try:
                cls._motion_proxy = ALProxy("ALMotion", constants.robotIP, constants.PORT)
            except Exception, e:
                print "Could not create proxy to AlMotion"
                print "Error was: ", e

        if cls._posture_proxy is None:
            try:
                cls._posture_proxy = ALProxy("ALRobotPosture", constants.robotIP, constants.PORT)
            except Exception, e:
                print "Could not create proxy to ALRobotPosture"
                print "Error was: ", e
        return [cls._motion_proxy, cls._posture_proxy]


def initialize():
    motion_proxy, posture_proxy = Proxies()
    stiffness_on(motion_proxy)
    posture_proxy.goToPosture("StandInit", 0.8)
    motion_proxy.waitUntilMoveIsFinished()
    motion_proxy.setMoveArmsEnabled(False, False)
    # gets the robot into his initial standing position
    # position = [0.0, 0.0, 0.3, 0.0, 0.0, 0.0]  # Absolute Position
    # motion_proxy.setPositions("Torso", motion.FRAME_ROBOT, position, 0.5, 63)
    # # Hula hoop
    # effector = "Torso"
    # space = motion.FRAME_WORLD
    # axisMask = almath.AXIS_MASK_ALL  # full control
    # isAbsolute = False
    # # Define the changes relative to the current position
    # dx = 0.045  # translation axis X (meter)
    # dy = 0.050  # translation axis Y (meter)
    # path = [
    #     [+dx, 0.0, 0.0, 0.0, 0.0, 0.0],  # point 1
    #     [0.0, -dy, 0.0, 0.0, 0.0, 0.0],  # point 2
    #     [-dx, 0.0, 0.0, 0.0, 0.0, 0.0],  # point 3
    #     [0.0, +dy, 0.0, 0.0, 0.0, 0.0],  # point 4
    #     [+dx, 0.0, 0.0, 0.0, 0.0, 0.0],  # point 5
    #     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]  # point 6
    # times = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]  # seconds
    #
    # motion_proxy.positionInterpolation(effector, space, path,
    #                                   axisMask, times, isAbsolute)


def stop():
    motion_proxy, posture_proxy = Proxies()
    # End Walk
    motion_proxy.move(0, 0, 0)
    motion_proxy.stopMove()
    motion_proxy.waitUntilMoveIsFinished()


def stiffness_on(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)


def move_forward():
    motion_proxy, posture_proxy = Proxies()
    motion_proxy.move(0, 0, 0)
    motion_proxy.waitUntilMoveIsFinished()
    motion_proxy.moveToward(0.5, 0.0, 0.0, constants.GAIT_STYLE)
    time.sleep(4)
    # motion_proxy.stopMove()


def move_backward():
    motion_proxy, posture_proxy = Proxies()
    motion_proxy.move(0,0,0)
    motion_proxy.waitUntilMoveIsFinished()
    motion_proxy.moveToward(-0.5, 0.0, 0.0, constants.GAIT_STYLE)
    time.sleep(4)
    # motion_proxy.stopMove()


def rotate_left():
    motion_proxy, posture_proxy = Proxies()
    motion_proxy.move(0, 0, 0)
    motion_proxy.waitUntilMoveIsFinished()
    motion_proxy.moveTo(0.0, 0.0, math.pi / 2, constants.GAIT_STYLE)
    time.sleep(4)
    # motion_proxy.stopMove()


def rotate_right():
    motion_proxy, posture_proxy = Proxies()
    motion_proxy.move(0, 0, 0)
    motion_proxy.waitUntilMoveIsFinished()
    motion_proxy.moveTo(0.0, 0.0, -math.pi / 2, constants.GAIT_STYLE)
    time.sleep(4)
    # motion_proxy.stopMove()


def send_robot(angle_list):
    motion_proxy, posture_proxy = Proxies()
    names = []
    al = []
    for name in angle_list["angles"]:
        names.append(str(name))
        al.append(float(angle_list["angles"][name]) * almath.TO_RAD)
    motion_proxy.stopMove()
    motion_proxy.angleInterpolationWithSpeed(names, al, 0.1)  # the function talks with the robot


