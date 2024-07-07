def compare(s1, s2):
    """
    get the relative distance between two strings by calculating how many characters are different between them
    :param s1: string to compare
    :param s2: string to compare
    :return: relative distance between s1 and s2. 0 being equal, 1 being completely different
    """
    if not s1 or not s2:
        return 1
    if s1 == s2:
        return 0

    arr = [[0 for j in range(len(s2))] for i in range(len(s1))]
    for i in range(1, len(s1)):
        arr[i][0] = i
    for i in range(1, len(s2)):
        arr[0][i] = i

    return float(distance(arr, s1, s2)) / max(len(s1), len(s2))


# 2-D dynamic program to calculate the total distance between two strings
def distance(arr, s1, s2):
    """
    2-D dynamic program to count the minimum number of character differences
    :param arr: 2-D array of size len(s1), len(s2) where arr[i][0] = i and arr[0][i] = i
    :param s1: string to compare
    :param s2: string to compare
    :return:
    """
    for i in range(1, len(s1)):
        for j in range(1, len(s2)):
            if s1[i] == s2[j]:
                arr[i][j] = arr[i - 1][j - 1]
            else:
                arr[i][j] = 1 + min(arr[i - 1][j - 1], min(arr[i - 1][j], arr[i][j - 1]))

    return arr[len(s1) - 1][len(s2) - 1]
