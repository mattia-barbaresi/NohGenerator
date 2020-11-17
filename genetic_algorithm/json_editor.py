import json
import sys


def dump_dict(filename, dictionary):
    with open(filename + '.json', 'w') as fp:
        json.dump(dictionary, fp)
    fp.close()


def read_dict(filename):
    try:
        with open(filename + '.json', 'r') as fp:
            file_opened = json.load(fp)
            fp.close()
            return file_opened
    except Exception as e:
        print "Unexpected error: " + filename, sys.exc_info()[0]
        print e
