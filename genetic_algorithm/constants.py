# the thresholds considered when need to add a choreography to the archive
# the threshold considered to calculate feasible individuals
# threshold_f_min = 0.3
# min_number_of_moves = 5
# max_number_of_moves = 16
NUMBER_OF_MOVES = 16
# parameter used to switch to fitness
T_MIN = 65
# parameter used to switch to hybrid
T_MAX = 80
# max number of archive entries considered
MAX_ARCH = 5
# genetic
MAX_NUMBER_OF_MUTATIONS = 4
POPULATION_SIZE = 100
# probability for mutating an individual
MUTPB = 0.35

# paths
ARCHIVE_PATH = "data/archive/archive"
REPERTOIRE_PATH = [
    "data/archive/repertoire1",
    "data/archive/repertoire2",
    "data/archive/repertoire3_priest",
    "data/archive/repertoire3_warrior",
    "data/archive/repertoire4",
    "data/archive/repertoire6",
    "data/archive/repertoire5",
    "data/archive/repertoire10"
]
RANDOM_PATH = "data/archive/random"

# LIST_OF_MOVES = jsonEditor.readDict("./data/archive/LIST_OF_MOVES")
LIST_OF_MOVES = {
    "a": "data/poses/armsdown",
    "b": "data/poses/swordright",
    "c": "data/poses/swordrightleftrequest",
    "d": "data/poses/openarms",
    "e": "data/poses/rightopen",
    "f": "data/poses/rightup45",
    "g": "data/poses/extremelysadchest",
    "h": "data/poses/swordleft",
    "i": "data/poses/arms45",
    "j": "data/poses/rightsadchest",
    "k": "data/poses/requestright",
    "l": "data/poses/request",
    "m": "data/poses/offering",
    "n": "data/poses/armsforward",
    "o": "data/poses/sadleft",
    "p": "data/poses/extremelysad",
    "q": "data/poses/sadright",
    "r": "data/poses/openarmsextended",
    "s": "data/poses/armsinit",
    "t": "data/poses/armsuppraying",
    "u": "data/poses/shieldleft",
    "v": "data/poses/shieldright",
    "w": "right",
    "x": "left",
    "y": "backward",
    "z": "forward"
}
