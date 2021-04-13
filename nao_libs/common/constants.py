hipPitchMax = 27
hipPitchMin = -88

hipRollMax = 21
hipRollMin = -45

HIP_OFFSET = 85
THIGH_LENGTH = 100
TIBIA_LENGTH = 102, 9

robotIP = "127.0.0.1"
PORT = 9559

STABILITY_THRESHOLD = 0.07

GAIT_STYLE = [["MaxStepX", 0.04],  # maximum forward translation along X (meters)	0.040	0.001	0.080
              ["MaxStepY", 0.11],  # absolute maximum lateral translation along Y (meters)	0.140	0.101	0.160
              ["MaxStepTheta", 0.35],  # absolute maximum rotation around Z (radians)	0.349	0.001	0.524
              ["MaxStepFrequency", 0],  # maximum step frequency (normalized, unit-less)  1   0   1
              ["StepHeight", 0.005],  # peak foot elevation along Z (meters)	0.020	0.005	0.040
              ["TorsoWx", 0.0],  # peak torso rotation around X (radians)	0.000	-0.122	0.122
              ["TorsoWy", 0.00]  # peak torso rotation around Y (radians)	0.000	-0.122	0.122
              ]

