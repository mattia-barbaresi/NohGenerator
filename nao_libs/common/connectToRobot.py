from naoqi import ALProxy
import almath


def connect(PORT):
    robotIP = "127.0.0.1"  # raw_input("robot IP: ")
    #PORT = 52461  # int(raw_input("robot Port (standard 9559): "))
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


    except Exception as e: # checks for any and all errors
        print("error")
        print(e)
        pass # ignores every single one of them, except keyboardInterupt and SystemExit
    except (KeyboardInterrupt, SystemExit): # when the program gets terminated
        print("error program terminated")
        postureProxy.goToPosture("StandInit", 0.5) # set the robot in its initial position
        motionProxy.setStiffnesses("Body", 1.0) # stiffen the joints
        raise #actually quit

