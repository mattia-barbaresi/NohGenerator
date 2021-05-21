import os
import time

from genetic_algorithm import constants
from utils import json_editor
from nao_libs.common import robot_proxy


def reproduce(sequence):
    # robot_proxy.turn_head()
    for pose in sequence:
        print pose + " : " + constants.LIST_OF_MOVES[pose]
        if pose == "z":
            robot_proxy.move_forward()
        elif pose == "y":
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
chors = ["abcdabefabcgbfea",
         "hibebajkldaebmda",
         "ldaebmdabldanoba",
         "alcibebaebcdaebk",
         "bmiafbaebcdaebka",
         "amialdbohpicenla",
         "aidbieclkdaikdba",
         "bkldaidlbebaibea",
         "milkdgjihdbnfbcd",
         "akfkekaildkhkeba",
         "edkimbehihopmfba",
         "bfahbiefkibdhbek",
         "kedneihbefbhdfke",
         "hihbcdfabebkldhn",
         "dpadmqdopqmdejfk",
         "azrtxwwgxyntzmay",
         "anbzhiuayvbzubay",
         "avnevbhzxbwwwzcr",
         "aljgzrtmydiaklra",
         "azpxowwqxmnldylm",
         "abcewhvxfnubzrha"]
katas = {
    "open-retreat":"sbyrs",
    "forward-point":"szbyrs",
    "backing-point":"syebs",
    "scooping-point":"swbexbs",
    "double-sweep":"wfzhxzrybzwzw",
    "zig-zag":"xmhzwbz",
    "pivot-to-point":"wezxbx",
    "weeping-r":"q",
    "weeping-l":"o",
    "weeping-both":"p",
}
shimai_dance = "zwzyxwezxbxsbyrsxzytqwszbyrssbyrsza"
print "Reproducing... " + chors[2]
robot_proxy.initialize()
reproduce("q")
robot_proxy.stop()
print "Execution finished"
