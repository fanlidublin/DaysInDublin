import sys

def parseData(File):
	try:
		f = open(File, "r")
		num = set()
		for number in f.readlines():
			num.add(number.strip())
		f.close()
	except FileNotFoundError:
		print("Warning: File not found")
	return num


file1 = parseData(sys.argv[1])
file2 = parseData(sys.argv[2])

print("Overlap: ", file1.intersection(file2))