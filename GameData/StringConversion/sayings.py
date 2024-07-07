from os import path
from GameData.StringConversion import string_compare


# given a string read from the screen, find the closest matching known dino name
def get_actual_saying(sayings, st):
    if not st:
        return ""
    diffs = []
    for s in sayings:
        if st == s:
            print("exact match {}".format(s))
            return s
        diffs.append((string_compare.compare(st, s), s))

    ret = min(diffs, key=lambda diff: diff[0])[1]
    print("match {}\nwith  {}".format(st, ret))
    return ret
