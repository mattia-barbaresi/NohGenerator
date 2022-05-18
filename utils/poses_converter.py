import glob
import json

import almath

for pose_name in glob.glob("data/poses/*"):
    with open(pose_name, "r") as fp:
        pose = json.load(fp)
    pose_c = pose_name.replace("poses", "poses_conv")
    pose_c = pose_c.replace(".json", ".py")
    with open(pose_c, "w") as fp:
        fp.write("names = list()")
        fp.write("\n")
        fp.write("times = list()")
        fp.write("\n")
        fp.write("keys = list()")
        fp.write("\n")
        fp.write("\n")

        for k, v in pose["angles"].items():
            fp.write("names.append('{}')".format(k))
            fp.write("\n")
            fp.write("times.append([1.25])")
            fp.write("\n")
            fp.write("keys.append([{}])".format(v * almath.TO_RAD))
            fp.write("\n")
            fp.write("\n")
