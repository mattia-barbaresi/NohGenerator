import os
import time

from genetic_algorithm import constants
from utils import json_editor
from nao_libs.common import robot_proxy


def reproduce(sequence):
    for pose in sequence:
        print pose + " : " + constants.LIST_OF_MOVES[pose]
        if pose == "z":
            robot_proxy.move_forward()
        elif pose == "y":  # z and y are the walk and the rotation
            robot_proxy.move_backward()
        elif pose == "x":
            robot_proxy.rotate_left()
        elif pose == "w":
            robot_proxy.rotate_right()
        else:
            list_angles = json_editor.read_dict(
                os.path.dirname(os.path.abspath(__file__)).rsplit("/")[0] + "/" + constants.LIST_OF_MOVES[pose])
            # send command to robot
            robot_proxy.send_robot(list_angles)
            time.sleep(2)


os.chdir("/")
# chor = "abcdefghijklmnopqrstuvwxyz"
chor = "zrqtghyrt"
print "Reproducing... " + chor
robot_proxy.initialize()
reproduce(chor)
robot_proxy.stop()
print "Execution finished"
