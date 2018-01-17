import sys

def parseData(filename):
    try:
        f = open(filename, "r")
        num = set()
        for number in num:
            num.add(number.strip())
        f.close()
    except FileNotFoundError:
        print("File not found: ", filename)
    return num

if len(sys.argv) != 3:
    print("Invalid entries")
else:
    file1 = parseData(sys.argv[1])
    file2 = parseData(sys.argv[2])
    print("Overlap: ", file1.intersection(file2))
