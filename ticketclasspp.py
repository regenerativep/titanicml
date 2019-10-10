import math
# take in val of (nan, 1, 2, 3). outputs array of [is first ? 1 : 0, is second ? 1 : 0, is third ? 1 : 0]
def format_ticket_class(val):
    arr = [0, 0, 0]
    if not isinstance(val, int):
        return arr
    for i in range(1, 4, 1):
        if val == i:
            arr[i - 1] = 1
    return arr
