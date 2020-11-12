import almath
from naoqi import ALProxy


def sendrobot(anglelist, t, robotIP="127.0.0.1", PORT=9559):
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

        # print("init")
        if (t == 0):  # if it is the first time the robot is called upon
            # motionProxy.setStiffnesses("Body", 0.0) # unstiffens the joints
            motionProxy.wbEnable(True)
            postureProxy.goToPosture("StandInit", 0.5)  # gets the robot into his initial standing position
            print("init")
            t = t + 1
        names = []
        angleLists = []
        timeLists = []
        # print(anglelist)
        for name in anglelist:
            print(name)
            print float(anglelist[name])
            names.append(str(name))
            angleLists.append([float(anglelist[name]) * almath.TO_RAD])
            timeLists.append([2])
        # print("asdfa")
        # print(names)
        # print(angleLists)
        # names = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RElbowYaw",  "LShoulderPitch", "LShoulderRoll", "LElbowRoll", "LElbowYaw"]
        # list of joints that will get changed

        #        angleLists = [[(anglelist[len(anglelist) - 8]) * almath.TO_RAD], # all the coordinates are saved in one big list
        #                   [(anglelist[len(anglelist) - 7]) * almath.TO_RAD], # and in a specific order (see list of joints)
        #                       [(anglelist[len(anglelist) - 6]) * almath.TO_RAD], # this gets them out of that list and sent to the right joint
        #                       [(anglelist[len(anglelist) - 5]) * almath.TO_RAD],
        #                       [(anglelist[len(anglelist) - 4]) * almath.TO_RAD],
        #                       [(anglelist[len(anglelist) - 3]) * almath.TO_RAD],
        #                       [(anglelist[len(anglelist) - 2]) * almath.TO_RAD],
        #                       [(anglelist[len(anglelist) - 1]) * almath.TO_RAD]]
        #
        #        timeLists = [[0.4], [0.4], [0.4], [0.4], [0.4], [0.4], [0.4], [0.4]] # sets the time the robot has to get to the joint location (when you give more than one coordinate for a joint, you have to give more than one timestamp for that same joint!)
        isAbsolute = True  # kindoff is deprecated, but makes the joint positions absolute and not relative
        print names
        print angleLists
        print timeLists
        motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)  # the function talks with the robot
        t += 1  # global t gets added by 1 so the joints dont get unstiffened again and the robot does not get put in its initial position
    except Exception as e:  # checks for any and all errors
        print("error")
        print(e)
        pass  # ignores every single one of them, except keyboardInterupt and SystemExit
    except (KeyboardInterrupt, SystemExit):  # when the program gets terminated
        print("error program terminated")
        postureProxy.goToPosture("StandInit", 0.5)  # set the robot in its initial position
        motionProxy.setStiffnesses("Body", 1.0)  # stiffen the joints
        raise  # actually quit
