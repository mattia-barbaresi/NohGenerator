import os

from genetic_algorithm import constants, json_editor
from nao_libs.common import sendToRobot, MoveForward, MoveBackward, Rotate


def read_and_move(filename, t):
    print "filename: " + filename
    list_angles = json_editor.read_dict(
        os.path.dirname(os.path.abspath(__file__)).rsplit("/")[0] + "/" + filename)
    sendToRobot.sendrobot(list_angles, t)


def reproduce(sequence):
    t = 1
    sendToRobot.initialize()
    for pose in sequence:
        # print Constants.LIST_OF_MOVES[x]
        if pose == "z":
            MoveForward.move_forward(t)
        elif pose == "y":  # z and y are the walk and the rotation
            MoveBackward.move_backward(t)
        elif pose == "x":
            Rotate.rotate_left(t)
        elif pose == "w":
            Rotate.rotate_right(t)
        else:
            read_and_move(constants.LIST_OF_MOVES[pose], t)


os.chdir("/")
reproduce("awhzsnxpyabtxdjj")
# reproduce("abcdefghijklmnopqrstuvwxyz")
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
# winsound.Beep(frequency, duration)
print "Execution finished"
