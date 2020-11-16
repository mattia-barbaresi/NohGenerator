from NaoLibs.Common import arms
import legsSimple as legs
from Common import constants

def anglesList(msg):
    listAngles = {}
    joints = {}
    support_leg = ""
    for i in msg:
        if i['jointname'] == "ShoulderLeft":
            shoulderLeft = i['coordinates']
        if i['jointname'] == "ElbowLeft":
            elbowLeft = i['coordinates']
        if i['jointname'] == "WristLeft":
            wristLeft = i['coordinates']
        if i['jointname'] == "ShoulderRight":
            shoulderRight = i['coordinates']
        if i['jointname'] == "ElbowRight":
            elbowRight = i['coordinates']
        if i['jointname'] == "WristRight":
            wristRight = i['coordinates']
        joints[i['jointname']] = i['coordinates']
    difference_between_feet = joints["AnkleLeft"][1] - joints["AnkleRight"][1]
    if difference_between_feet < constants.STABILITY_THRESHOLD:
        support_leg = "Legs"
    elif difference_between_feet > 0:
        support_leg = "RLeg"
    else:
        support_leg = "LLeg"
    listAngles["RShoulderPitch"] = arms.angleRShoulderPitch(shoulderRight[0], shoulderRight[2], shoulderRight[1], elbowRight[0], elbowRight[2],
                                                            elbowRight[1])
    listAngles["RShoulderRoll"] = arms.angleRShoulderRoll(shoulderRight[0], shoulderRight[2], shoulderRight[1], elbowRight[0], elbowRight[2],
                                                          elbowRight[1])
    listAngles["RElbowRoll"] = arms.angleRElbowRoll(shoulderRight[0], shoulderRight[2], shoulderRight[1], elbowRight[0], elbowRight[2],
                                                    elbowRight[1], wristRight[0], wristRight[2], wristRight[1])
    listAngles["RElbowYaw"] = arms.angleRElbowYaw(elbowRight[0], elbowRight[2], elbowRight[1], wristRight[0], wristRight[2],
                                                  wristRight[1], listAngles["RShoulderPitch"])
    listAngles["LShoulderPitch"] = arms.angleLShoulderPitch(shoulderLeft[0], shoulderLeft[2], shoulderLeft[1], elbowLeft[0], elbowLeft[2],
                                                            elbowLeft[1])
    listAngles["LShoulderRoll"] = arms.angleLShouderRoll(shoulderLeft[0], shoulderLeft[2], shoulderLeft[1], elbowLeft[0], elbowLeft[2],
                                                         elbowLeft[1])
    listAngles["LElbowRoll"] = arms.angleLElbowRoll(shoulderLeft[0], shoulderLeft[2], shoulderLeft[1], elbowLeft[0], elbowLeft[2],
                                                    elbowLeft[1], wristLeft[0], wristLeft[2], wristLeft[1])
    listAngles["LElbowYaw"] = arms.angleLElbowYaw(elbowLeft[0], elbowLeft[2], elbowLeft[1], wristLeft[0], wristLeft[2],
                                                  wristLeft[1], listAngles["LShoulderPitch"])

    listAngles["LKneePitch"] = legs.calculateKneePitch(joints["HipLeft"][0],
                                                       joints["HipLeft"][2],
                                                       joints["HipLeft"][1],
                                                       joints["KneeLeft"][0],
                                                       joints["KneeLeft"][2],
                                                       joints["KneeLeft"][1],
                                                       joints["AnkleLeft"][0],
                                                       joints["AnkleLeft"][2],
                                                       joints["AnkleLeft"][1])

    listAngles["RKneePitch"] = legs.calculateKneePitch(joints["HipRight"][0],
                                                       joints["HipRight"][2],
                                                       joints["HipRight"][1],
                                                       joints["KneeRight"][0],
                                                       joints["KneeRight"][2],
                                                       joints["KneeRight"][1],
                                                       joints["AnkleRight"][0],
                                                       joints["AnkleRight"][2],
                                                       joints["AnkleRight"][1])
    #
    # angleRHipPitchYaw = legs.calculateHipPitchYaw(joints["HipRight"][0],
    #                                               joints["HipRight"][2],
    #                                               joints["HipRight"][1],
    #                                               joints["KneeRight"][0],
    #                                               joints["KneeRight"][2],
    #                                               joints["KneeRight"][1],
    #                                               joints["AnkleRight"][0],
    #                                               joints["AnkleRight"][2],
    #                                               joints["AnkleRight"][1])
    #
    # angleLHipPitchYaw = legs.calculateHipPitchYaw(joints["HipLeft"][0],
    #                                               joints["HipLeft"][2],
    #                                               joints["HipLeft"][1],
    #                                               joints["KneeLeft"][0],
    #                                               joints["KneeLeft"][2],
    #                                               joints["KneeLeft"][1],
    #                                               joints["AnkleLeft"][0],
    #                                               joints["AnkleLeft"][2],
    #                                               joints["AnkleLeft"][1])
    #
    # listAngles["LHipYawPitch"] = legs.hipYawPitch(angleLHipPitchYaw, angleRHipPitchYaw)

    # listAngles["HeadPitch"] = head.angleHeadPitch(joints["Head"][0],
    #                                               joints["Head"][2],
    #                                               joints["Head"][1],
    #                                               joints["ShoulderCenter"][0],
    #                                               joints["ShoulderCenter"][2],
    #                                               joints["ShoulderCenter"][1],
    #                                               joints["Spine"][0],
    #                                               joints["Spine"][2],
    #                                               joints["Spine"][1])

    listAngles["LHipPitch"] = legs.calculateHipPitch(joints["HipLeft"][0],
                                                  joints["HipLeft"][2],
                                                  joints["HipLeft"][1],
                                                  joints["KneeLeft"][0],
                                                  joints["KneeLeft"][2],
                                                  joints["KneeLeft"][1])
    listAngles["RHipPitch"] = legs.calculateHipPitch(joints["HipRight"][0],
                                                  joints["HipRight"][2],
                                                  joints["HipRight"][1],
                                                  joints["KneeRight"][0],
                                                  joints["KneeRight"][2],
                                                  joints["KneeRight"][1])

    listAngles["RHipRoll"] = legs.calculateHipRoll(joints["HipRight"][0],
                                                  joints["HipRight"][2],
                                                  joints["HipRight"][1],
                                                  joints["KneeRight"][0],
                                                  joints["KneeRight"][2],
                                                  joints["KneeRight"][1], False)
    listAngles["LHipRoll"] = legs.calculateHipRoll(joints["HipLeft"][0],
                                                  joints["HipLeft"][2],
                                                  joints["HipLeft"][1],
                                                  joints["KneeLeft"][0],
                                                  joints["KneeLeft"][2],
                                                  joints["KneeLeft"][1], True)
    listAngles["RAnklePitch"] = legs.calculateAnklePitch(joints["KneeRight"][0],
                                                       joints["KneeRight"][2],
                                                       joints["KneeRight"][1],
                                                       joints["AnkleRight"][0],
                                                       joints["AnkleRight"][2],
                                                       joints["AnkleRight"][1],
                                                       joints["FootRight"][0],
                                                       joints["FootRight"][2],
                                                       joints["FootRight"][1])
    listAngles["LAnklePitch"] = legs.calculateAnklePitch(joints["KneeLeft"][0],
                                                       joints["KneeLeft"][2],
                                                       joints["KneeLeft"][1],
                                                       joints["AnkleLeft"][0],
                                                       joints["AnkleLeft"][2],
                                                       joints["AnkleLeft"][1],
                                                       joints["FootLeft"][0],
                                                       joints["FootLeft"][2],
                                                       joints["FootLeft"][1])
    return {"angles": listAngles, "supportLeg": support_leg}
