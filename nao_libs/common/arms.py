import math

import bcolors


def angleRShoulderPitch(x2, y2, z2, x1, y1,
                        z1):  # calulates the Shoulderpitch value for the Right shoulder by using geometry
    print bcolors.BLUE + "angleRShoulderPitch" + bcolors.ENDC
    angle = math.atan2((y2 - y1), (z2 - z1))  # obtain the angle between shoulder and elbow
    angle = math.degrees(angle)
    print "angleRShoulderPitch", angle
    # if (z2 - z1) < 0:
    #     if angle > 0:
    #         angle = angle - 180
    #     elif angle < 0:
    #         angle = angle + 180
    # # angle = -90  - angle
    angle = - angle
    if angle > 118:
        angle = 118
    elif angle < -118:
        angle = -118
    print bcolors.OKMSG + "angle rshoulder pitch " + str(angle) + bcolors.ENDC
    return - angle


def angleRShoulderRoll(x2, y2, z2, x1, y1,
                       z1):  # calulates the ShoulderRoll value for the Right shoulder by using geometry
    print bcolors.BLUE + "angleRShoulderRoll" + bcolors.ENDC
    angle = math.atan2((x2 - x1), (z2 - z1))
    angle = math.degrees(angle)
    print angle

    # angle = angle +90
    if angle < -76:
        angle = -76
    elif angle > 18:
        angle = 18
    print bcolors.OKMSG, "angle rshoulder roll ", angle, bcolors.ENDC

    return angle
    # if  left:
    #     angle = - angle`
    #
    # if(z2<z1):
    #     test = z2
    #     anderetest = z1
    #     z2=anderetest
    #     z1=test
    # if (z2 - z1 < 0.1):
    #     z2 = 1.0
    #     z1 = 0.8
    # angle = math.atan((x2 - x1) / (z2 - z1))
    # angle = math.degrees(angle)
    # return angle


def angleLShoulderPitch(x2, y2, z2, x1, y1,
                        z1):  # calulates the Shoulderpitch value for the Left shoulder by using geometry
    print bcolors.BLUE + "angleLShoulderPitch" + bcolors.ENDC
    print "y, z", (y2 - y1), (z2 - z1)

    angle = 0
    if (z2 - z1) < 0:
        angle = math.atan((y2 - y1) / (z2 - z1))
    elif (y2 - y1) < 0:
        angle = -math.atan((z2 - z1) / (y2 - y1)) + (math.pi / 2)
    else:
        angle = -math.atan((z2 - z1) / (y2 - y1)) - (math.pi / 2)

    # angle = math.atan2((y2 - y1), (z2 - z1))
    angle = math.degrees(angle)
    print "angle", angle
    angle = angle + 180
    # angle = -angle
    if angle > 118:
        angle = 118
    elif angle < -118:
        angle = -118
    print(bcolors.OKMSG + "angle final Lshoulderpitch " + str(angle) + bcolors.ENDC)
    return - angle


def angleLShouderRoll(x2, y2, z2, x1, y1,
                      z1):  # calulates the ShoulderRoll value for the Left shoulder by using geometry
    print bcolors.BLUE + "angleLShouderRoll" + bcolors.ENDC
    print "x, z", (x2 - x1), (z2 - z1)
    angle = math.atan2((x2 - x1), (z2 - z1))
    angle = math.degrees(angle)
    print "angle", angle
    print angle
    # angle = angle +90

    if angle < -18:
        angle = -18
    elif angle > 76:
        angle = 76
    print(bcolors.OKMSG + "angle final lshouder roll " + str(angle) + bcolors.ENDC)
    return angle


def angleRElbowYaw(x2, y2, z2, x1, y1, z1,
                   shoulderpitch):  # calulates the ElbowYaw value for the Right elbow by using geometry
    print "shoulder pitch", shoulderpitch
    if abs(y2 - y1) < 0.2 and abs(z2 - z1) < 0.2 and (x1 < x2):
        return 0
    elif (abs(x2 - x1) < 0.1 and abs(z2 - z1) < 0.1 and (y1 > y2)):
        return 90
    elif (abs(x2 - x1) < 0.1 and abs(z2 - z1) < 0.1 and (shoulderpitch > 50)):
        return 90
    elif (abs(y2 - y1) < 0.1 and abs(z2 - z1) < 0.1 and (shoulderpitch < 50)):
        return 0
    elif (abs(x2 - x1) < 0.1 and abs(y2 - y1) < 0.1 and (shoulderpitch > 50)):
        return 90
    else:
        angle = math.atan((z2 - z1) / (y2 - y1))
        angle = math.degrees(angle)
        angle = - angle + (shoulderpitch)
        angle = - angle
        return angle


def angleRElbowRoll(x3, y3, z3, x2, y2, z2, x1, y1,
                    z1):  # calulates the ElbowRoll value for the Right elbow by using geometry
    a1 = (x3 - x2) ** 2 + (y3 - y2) ** 2 + (z3 - z2) ** 2
    lineA = a1 ** 0.5  # calculates length of line between 2 3D coordinates
    b1 = (x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2
    lineB = b1 ** 0.5  # calculates length of line between 2 3D coordinates
    c1 = (x1 - x3) ** 2 + (y1 - y3) ** 2 + (z1 - z3) ** 2
    lineC = c1 ** 0.5  # calculates length of line between 2 3D coordinates

    cosB = (pow(lineA, 2) + pow(lineB, 2) - pow(lineC, 2)) / (2 * lineA * lineB)
    acosB = math.acos(cosB)
    angle = math.degrees(acosB)
    angle = 180 - angle
    return angle


def angleLElbowYaw(x2, y2, z2, x1, y1, z1,
                   shoulderpitch):  # calulates the ElbowYaw value for the Left elbow by using geometry
    if (abs(y2 - y1) < 0.2 and abs(z2 - z1) < 0.2 and (x1 > x2)):
        return 0
    elif (abs(x2 - x1) < 0.1 and abs(z2 - z1) < 0.1 and (y1 > y2)):
        return -90
    elif (abs(x2 - x1) < 0.1 and abs(z2 - z1) < 0.1 and (shoulderpitch > 50)):
        return -90
    elif (abs(y2 - y1) < 0.1 and abs(z2 - z1) < 0.1 and (shoulderpitch > 50)):
        return 0
    elif (abs(x2 - x1) < 0.1 and abs(y2 - y1) < 0.1 and (shoulderpitch > 50)):
        return -90
    else:
        angle = math.atan((z2 - z1) / (y2 - y1))
        angle = math.degrees(angle)
        angle = - angle + (shoulderpitch)
        angle = - angle
        return angle


def angleLElbowRoll(x3, y3, z3, x2, y2, z2, x1, y1,
                    z1):  # calulates the ElbowRoll value for the Left elbow by using geometry

    a1 = (x3 - x2) ** 2 + (y3 - y2) ** 2 + (z3 - z2) ** 2
    lineA = a1 ** 0.5  # calculates length of line between 2 3D coordinates
    b1 = (x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2
    lineB = b1 ** 0.5  # calculates length of line between 2 3D coordinates
    c1 = (x1 - x3) ** 2 + (y1 - y3) ** 2 + (z1 - z3) ** 2
    lineC = c1 ** 0.5  # calculates length of line between 2 3D coordinates

    cosB = (pow(lineA, 2) + pow(lineB, 2) - pow(lineC, 2)) / (2 * lineA * lineB)
    acosB = math.acos(cosB)
    angle = math.degrees(acosB)
    angle = -180 + angle
    return angle
