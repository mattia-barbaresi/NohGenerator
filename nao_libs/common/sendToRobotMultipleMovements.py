from naoqi import ALProxy
import almath
import time

def send_robot_multiple_movements(angleListArray):
    t = 0
    for x in angleListArray:
        sendrobot(x, t)
        t = t + 1


def sendrobot(anglelist,t):
    robotIP = "127.0.0.1"  # raw_input("robot IP: ")
    PORT = 9559  # int(raw_input("robot Port (standard 9559): "))
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
        if (t == 0): # if it is the first time the robot is called upon
            #motionProxy.setStiffnesses("Body", 0.0) # unstiffens the joints
            motionProxy.wbEnable(True)
            postureProxy.goToPosture("StandInit", 0.5) # gets the robot into his initial standing position
            t = t+1
        names = []
        angleLists = []
        timeLists = []
        for name in anglelist:
            names.append(str(name))
            angleLists.append([float(anglelist[name])*almath.TO_RAD])
            timeLists.append([1])
        isAbsolute = True # kindoff is deprecated, but makes the joint positions absolute and not relative
        motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute) #the function talks with the robot
        # motionProxy.waitUntilMoveIsFinished()
        t += 1 # global t gets added by 1 so the joints dont get unstiffened again and the robot does not get put in its initial position
    except Exception as e: # checks for any and all errors
        print("error")
        print(e)
        pass # ignores every single one of them, except keyboardInterupt and SystemExit
    except (KeyboardInterrupt, SystemExit): # when the program gets terminated
        print("error program terminated")
        postureProxy.goToPosture("StandInit", 0.5) # set the robot in its initial position
        motionProxy.setStiffnesses("Body", 1.0) # stiffen the joints
        raise #actually quit
