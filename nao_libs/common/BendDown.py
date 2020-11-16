import motion
from naoqi import ALProxy
from nao_libs.common import constants


def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)


def bend_down(t):
    robotIP = constants.robotIP
    PORT = constants.PORT
    try:
        try:
            motionProxy = ALProxy("ALMotion", robotIP, PORT) #creates proxy to call specific functions
        except Exception, e:
            print "Could not create proxy to AlMotion"
            print "Error was: ", e
        try:
            postureProxy = ALProxy("ALRobotPosture", robotIP, PORT) #creates proxy to call specific functions
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e
        StiffnessOn(motionProxy)
        # if (t == 0): # if it is the first time the robot is called upon
        #     motionProxy.setStiffnesses("Body", 0.0) # unstiffens the joints
        #     motionProxy.wbEnable(True)
        #     postureProxy.goToPosture("Stand", 10) # gets the robot into his initial standing position
        #     print("init")

        motionProxy.wbEnable(True)
        # motionProxy.setCollisionProtectionEnabled("Arms", True)
        # Example showing how to set Torso Position, using a fraction of max speed
        # chainName = "Torso"
        space = motion.FRAME_ROBOT
        # position = [0.05, -1, -1, 0.0, math.pi/8, 0.0]  # Absolute Position
        # fractionMaxSpeed = 0.7
        axisMask = [63]
        print "bending"
        # Lower the Torso and move to the side
        effectorList = ["Torso"]
        pathList = [[0.0, -0.2, -0.2, 0.0, 0.0, 0.0]]
        timeList = [[2.0]]  # seconds
        isAbsolute = False

        motionProxy.positionInterpolations(effectorList, space, pathList,
                                          axisMask, timeList, isAbsolute)
        # motionProxy.setPositions(chainName, frame, position, fractionMaxSpeed, axisMask)
    except Exception as e: # checks for any and all errors
        print "error here " , e
         # ignores every single one of them, except keyboardInterupt and SystemExit
    except (KeyboardInterrupt, SystemExit): # when the program gets terminated
        print("error program terminated")
        postureProxy.goToPosture("StandInit", 0.5) # set the robot in its initial position
        motionProxy.setStiffnesses("Body", 1.0) # stiffen the joints
        raise #actually quit
