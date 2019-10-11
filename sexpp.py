# input string (nan, "male", "female"). outputs array of [is male ? 1 : 0, is female ? 1 : 0]
def format_sex(val):
    arr = [0, 0]
    if not isinstance(val, str):
        return arr
    if val == "male":
        arr[0] = 1
    elif val == "female":
        arr[1] = 1
    return arr