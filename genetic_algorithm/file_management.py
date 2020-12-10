import genetic_algorithm.constants
from utils import json_editor


# todo refactor here
def init_res_arch(path):
    json_editor.dump_dict(path + "res_arch", {})


def getres(path):
    try:
        return json_editor.read_dict(path)
    except Exception, e:
        print "error", Exception, e


def addres(x, path, index):
    res = getres(path)
    res[index] = x
    json_editor.dump_dict(path, res)


def getRepertoireWithPath(path):
    try:
        return json_editor.read_dict(path)
    except Exception, e:
        print "error", Exception, e


def getResults():
    try:
        return json_editor.read_dict(genetic_algorithm.constants.results_path)
    except Exception, e:
        print "error", Exception, e


def saveResults(res):
    saveResultsToPath(genetic_algorithm.constants.results_path, res)


def saveResultsToPath(res, path):
    json_editor.dump_dict(path, res)
