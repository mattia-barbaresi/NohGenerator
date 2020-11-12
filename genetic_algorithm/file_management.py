import genetic_algorithm.constants
import json_editor


# todo refactor here
def getArchive():
    try:
        dict = json_editor.read_dict(genetic_algorithm.constants.ARCHIVE_PATH)
        return dict
    except Exception, e:
        print "error", Exception, e


def saveArchive(archive):
    json_editor.dump_dict(genetic_algorithm.constants.ARCHIVE_PATH, archive)


def getres(path):
    try:
        dict = json_editor.read_dict(path)
        return dict
    except Exception, e:
        print "error", Exception, e


def saveres(res, path):
    json_editor.dump_dict(path, res)


def addres(x, path, index):
    # print "adding to archive"
    res = getres(path)
    res[index] = x
    saveres(res, path)


def addToArchive(choreography):
    # print "adding to archive"
    archive = getArchive()
    archive["archive"].append(choreography)
    saveArchive(archive)


def initres(path):
    saveres({}, path + "res_arch")


def clearArchive():
    saveArchive({"archive": []})


def loadListOfMoves():
    return json_editor.read_dict(genetic_algorithm.constants.list_of_moves_path)


def saveListOfMoves(list_of_moves):
    return json_editor.dump_dict(genetic_algorithm.constants.list_of_moves_path, list_of_moves)


def getRepertoire():
    try:
        dict = json_editor.read_dict(genetic_algorithm.constants.REPERTOIRE_PATH[0])
        return dict
    except Exception, e:
        print "error", e


def getRepertoireWithPath(path):
    try:
        dict = json_editor.read_dict(path)
        return dict
    except Exception, e:
        print "error", Exception, e


def saveRepertoire(archive):
    json_editor.dump_dict(genetic_algorithm.constants.REPERTOIRE_PATH[0], archive)


def addToRepertoire(choreography):
    archive = getRepertoire()
    archive["repertoire"].append(choreography)
    saveArchive(archive)


def getResults():
    try:
        dict = json_editor.read_dict(genetic_algorithm.constants.results_path)
        return dict
    except Exception, e:
        print "error", Exception, e


def saveResults(archive):
    saveResultsToPath(genetic_algorithm.constants.results_path, archive)


def saveResultsToPath(archive, path):
    json_editor.dump_dict(path, archive)

# def addToResults(choreography):
#     archive = getResults()
#     archive["results"].append(choreography)
#     saveResults(archive)
