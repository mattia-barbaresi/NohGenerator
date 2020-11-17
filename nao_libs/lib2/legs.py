import math
from utils import trigo


def calculateKneePitch(x1, y1, z1, #1 is the hip position
                       x2, y2, z2, #2 is the knee position
                       x3, y3, z3): #3 is the ankle position
    angle = 180 - trigo.angleBetween3Points3D(x1, y1, z1,
                                              x2, y2, z2,
                                              x3, y3, z3)
    if angle > 121:
        angle = 121
    elif angle < -5:
        angle = -5
    return angle

def calculateAnklePitch(x1, y1, z1, #1 is the hip position
                         x2, y2, z2, #2 is the knee position
                         x3, y3, z3):
    angle = trigo.angleBetween3Points3D(x1, y1, z1,
                                        x2, y2, z2,
                                        x3, y3, z3)
    print "ankle angle3d"
    print angle
    if angle > 52:
        angle = 52
    elif angle < -68:
        angle = -68
    return angle

def calculateHipPitchYaw(x1, y1, z1, #1 is the hip position
                         x2, y2, z2, #2 is the knee position
                         x3, y3, z3): #3 is the ankle position
    l = trigo.distanceBetween2Points3D(x1, y1, z1, x2, y2, z2) #calculate distance between hip and knee
    alpha = trigo.angleBetween3Points3D(x2, y2, z2, x1, y1, z1, x3, y3, z3) # calculate the angle between the ankle, the hip and the knee
    h = l * math.cos(math.radians(alpha))
    distanceKneeFromLine = trigo.distanceOfPointFromLine(x1, y1, x3, y3, x2, y2)
    angle = math.acos(distanceKneeFromLine/h)
    return angle

def calculateHipPitch(angleHipPitchYaw,
                      x1, y1, z1, #1 is the hip position
                      x2, y2, z2): #2 is the knee position):

    radiusLength = trigo.distanceBetween2Points3D(x1, y1, z1, x2, y2, z2)
    xNAO = math.cos(math.radians(angleHipPitchYaw))*(math.sqrt(2)/2)  * radiusLength  # the x of the nao without pitch and roll, equals to k axis
    yNAO = ((math.sqrt(2)/ 2)  + math.sin(math.radians(angleHipPitchYaw)) * (math.sqrt(2)/2)) *radiusLength
    zNAO = ((math.sqrt(2)/ 2) - math.sin(math.radians(angleHipPitchYaw)) * (math.sqrt(2)/2)) *radiusLength

    naoLength = trigo.distanceBetween2Points3D(x1, y1, z1, xNAO, yNAO, zNAO)
    print "length"
    print str(radiusLength) + " " + str(naoLength)

    # x1 + xNAO, y1 - yNAO, z1 - zNAO
    # trigo.angleBetween3Points2D(, x1, y1, z1)

def hipYawPitch(angleLHipPitchYaw, angleRHipPitchYaw):
    angleHipPitchYaw = (angleLHipPitchYaw + angleRHipPitchYaw)/2
    angle =  - angleHipPitchYaw/2
    if angle < -65:
        angle = -65
    elif angle > 42:
        angle = 42
    return angle


