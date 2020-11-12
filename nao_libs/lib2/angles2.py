import legs
from nao_libs.common import arms


def anglesList(msg):
    listAngles = {}
    joints = {}
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

    listAngles["RShoulderPitch"] = arms.angleRShoulderPitch(shoulderRight[0], shoulderRight[1], shoulderRight[2],
                                                            elbowRight[0], elbowRight[1],
                                                            elbowRight[2])
    listAngles["RShoulderRoll"] = arms.angleRShoulderRoll(shoulderRight[0], shoulderRight[1], shoulderRight[2],
                                                          elbowRight[0], elbowRight[1],
                                                          elbowRight[2])
    listAngles["RElbowRoll"] = arms.angleRElbowRoll(shoulderRight[0], shoulderRight[1], shoulderRight[2], elbowRight[0],
                                                    elbowRight[1],
                                                    elbowRight[2], wristRight[0], wristRight[1], wristRight[2])
    listAngles["RElbowYaw"] = arms.angleRElbowYaw(elbowRight[0], elbowRight[1], elbowRight[2], wristRight[0],
                                                  wristRight[1],
                                                  wristRight[2], listAngles["RShoulderPitch"])
    listAngles["LShoulderPitch"] = arms.angleLShoulderPitch(shoulderLeft[0], shoulderLeft[1], shoulderLeft[2],
                                                            elbowLeft[0], elbowLeft[1],
                                                            elbowLeft[2])
    listAngles["LShoulderRoll"] = arms.angleLShouderRoll(shoulderLeft[0], shoulderLeft[1], shoulderLeft[2],
                                                         elbowLeft[0], elbowLeft[1],
                                                         elbowLeft[2])
    listAngles["LElbowRoll"] = arms.angleLElbowRoll(shoulderLeft[0], shoulderLeft[1], shoulderLeft[2], elbowLeft[0],
                                                    elbowLeft[1],
                                                    elbowLeft[2], wristLeft[0], wristLeft[1], wristLeft[2])
    listAngles["LElbowYaw"] = arms.angleLElbowYaw(elbowLeft[0], elbowLeft[1], elbowLeft[2], wristLeft[0], wristLeft[1],
                                                  wristLeft[2], listAngles["LShoulderPitch"])

    listAngles["LKneePitch"] = legs.calculateKneePitch(joints["HipLeft"][0],
                                                       joints["HipLeft"][1],
                                                       joints["HipLeft"][2],
                                                       joints["KneeLeft"][0],
                                                       joints["KneeLeft"][1],
                                                       joints["KneeLeft"][2],
                                                       joints["AnkleLeft"][0],
                                                       joints["AnkleLeft"][1],
                                                       joints["AnkleLeft"][2])

    listAngles["RKneePitch"] = legs.calculateKneePitch(joints["HipRight"][0],
                                                       joints["HipRight"][1],
                                                       joints["HipRight"][2],
                                                       joints["KneeRight"][0],
                                                       joints["KneeRight"][1],
                                                       joints["KneeRight"][2],
                                                       joints["AnkleRight"][0],
                                                       joints["AnkleRight"][1],
                                                       joints["AnkleRight"][2])

    angleRHipPitchYaw = legs.calculateHipPitchYaw(joints["HipRight"][0],
                                                  joints["HipRight"][1],
                                                  joints["HipRight"][2],
                                                  joints["KneeRight"][0],
                                                  joints["KneeRight"][1],
                                                  joints["KneeRight"][2],
                                                  joints["AnkleRight"][0],
                                                  joints["AnkleRight"][1],
                                                  joints["AnkleRight"][2])

    angleLHipPitchYaw = legs.calculateHipPitchYaw(joints["HipLeft"][0],
                                                  joints["HipLeft"][1],
                                                  joints["HipLeft"][2],
                                                  joints["KneeLeft"][0],
                                                  joints["KneeLeft"][1],
                                                  joints["KneeLeft"][2],
                                                  joints["AnkleLeft"][0],
                                                  joints["AnkleLeft"][1],
                                                  joints["AnkleLeft"][2])

    print "calculateHipPitchYaw"
    print legs.calculateHipPitchYaw(joints["ShoulderCenter"][0],
                                    joints["ShoulderCenter"][1],
                                    joints["ShoulderCenter"][2],
                                    joints["Spine"][0],
                                    joints["Spine"][1],
                                    joints["Spine"][2],
                                    joints["HipCenter"][0],
                                    joints["HipCenter"][1],
                                    joints["HipCenter"][2])
    listAngles["LHipYawPitch"] = legs.hipYawPitch(angleLHipPitchYaw, angleRHipPitchYaw)
    listAngles["LHipPitch"] = legs.calculateHipPitch(listAngles["LHipYawPitch"],
                                                     joints["HipLeft"][0],
                                                     joints["HipLeft"][1],
                                                     joints["HipLeft"][2],
                                                     joints["KneeLeft"][0],
                                                     joints["KneeLeft"][1],
                                                     joints["KneeLeft"][2])
    listAngles["RHipPitch"] = legs.calculateHipPitch(listAngles["LHipYawPitch"],
                                                     joints["HipRight"][0],
                                                     joints["HipRight"][1],
                                                     joints["HipRight"][2],
                                                     joints["KneeRight"][0],
                                                     joints["KneeRight"][1],
                                                     joints["KneeRight"][2])

    print legs.calculateAnklePitch(joints["HipRight"][0],
                                   joints["HipRight"][1],
                                   joints["HipRight"][2],
                                   joints["KneeRight"][0],
                                   joints["KneeRight"][1],
                                   joints["KneeRight"][2],
                                   joints["FootRight"][0],
                                   joints["FootRight"][1],
                                   joints["FootRight"][2])

    return listAngles
