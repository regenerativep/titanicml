import preprocessing as pp

def test(actual, desired):
    global total, totalGood, showIndividualOutput
    isGood = False
    if actual == desired:
        totalGood += 1
        isGood = True
    total += 1
    if showIndividualOutput:
        if isGood:
            print("value " + str(actual) + " good")
        else:
            print("got value " + str(actual) + ", wanted " + str(desired))

def main():
    global total, totalGood, showIndividualOutput
    total = 0
    totalGood = 0
    showIndividualOutput = False
    test(pp.format_sex("hello"), [0, 0])
    test(pp.format_sex(""), [0, 0])
    test(pp.format_sex(float("nan")), [0, 0])
    test(pp.format_sex("male"), [1, 0])
    test(pp.format_sex("female"), [0, 1])

    test(pp.format_ticket_class(0), [0, 0, 0])
    test(pp.format_ticket_class(1), [1, 0, 0])
    test(pp.format_ticket_class(2), [0, 1, 0])
    test(pp.format_ticket_class(3), [0, 0, 1])
    test(pp.format_ticket_class(4), [0, 0, 0])
    test(pp.format_ticket_class(float("nan")), [0, 0, 0])

    print(str(totalGood) + " / " + str(total) + " tests good")

main()