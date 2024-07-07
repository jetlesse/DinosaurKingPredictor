from GameData.StringConversion import string_compare


# given a string read from the screen, find the closest matching known dino name
def get_actual_dino_name(dinos, name):
    diffs = []
    for n in dinos:
        if name == n:
            return n
        diffs.append((string_compare.compare(name, n), n))

    return min(diffs, key=lambda diff: diff[0])[1]
