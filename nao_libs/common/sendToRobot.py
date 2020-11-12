import almath
import motion
from naoqi import ALProxy

from common import constants


def initialize():
    robotIP = constants.robotIP
    # robotIP = "127.0.0.1"
    PORT = constants.PORT
    try:
        motionProxy = ALProxy("ALMotion", robotIP, PORT)  # creates proxy to call specific functions
    except Exception, e:
        print "Could not create proxy to AlMotion"
        print "Error was: ", e
    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)  # creates proxy to call specific functions
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    StiffnessOn(motionProxy)
    motionProxy.setStiffnesses("Body", 0.0)  # unstiffens the joints
    motionProxy.wbEnable(True)
    postureProxy.goToPosture("Stand", 10)  # gets the robot into his initial standing position


def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)


def sendrobot(anglelist, t):
    robotIP = constants.robotIP
    PORT = constants.PORT
    try:
        try:
            motionProxy = ALProxy("ALMotion", robotIP, PORT)  # creates proxy to call specific functions
        except Exception, e:
            print "Could not create proxy to AlMotion"
            print "Error was: ", e
        try:
            postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)  # creates proxy to call specific functions
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e
        names = []
        angleLists = []
        timeLists = []
        StiffnessOn(motionProxy)
        for name in anglelist["angles"]:
            names.append(str(name))
            angleLists.append(float(anglelist["angles"][name]) * almath.TO_RAD)
            timeLists.append(4.0)

        if (t == 0):  # if it is the first time the robot is called upon
            motionProxy.setStiffnesses("Body", 0.0)  # unstiffens the joints
            motionProxy.wbEnable(True)

            postureProxy.goToPosture("Stand", 10)  # gets the robot into his initial standing position
            print("init")
            chainName = "Torso"
            frame = motion.FRAME_ROBOT
            position = [0.0, 0.05, 0.3, 0.1, 0.0, 0.0]  # Absolute Position
            fractionMaxSpeed = 0.05
            axisMask = 63
            motionProxy.setPositions(chainName, frame, position, fractionMaxSpeed, axisMask)
        motionProxy.wbEnable(True)
        leftArmEnable = False
        rightArmEnable = False
        motionProxy.setMoveArmsEnabled(leftArmEnable, rightArmEnable)
        motionProxy.angleInterpolation(names, angleLists, timeLists, True)  # the function talks with the robot
    except Exception as e:  # checks for any and all errors
        print "error in here ", e
        # ignores every single one of them, except keyboardInterupt and SystemExit
    except (KeyboardInterrupt, SystemExit):  # when the program gets terminated
        print("error program terminated")
        postureProxy.goToPosture("StandInit", 0.5)  # set the robot in its initial position
        motionProxy.setStiffnesses("Body", 1.0)  # stiffen the joints
        raise  # actually quit
