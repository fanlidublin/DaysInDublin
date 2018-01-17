import sys

def parseData(File):
	try:
		f = open(File, "r")		
		names = []
		for name in f.readlines():
			names.append(name.strip())
		f.close()
	except FileNotFoundError:
		print("Warning: File not found")
	return names


file1 = parseData(sys.argv[1])
argv_val = list(sys.argv)
pos = argv_val[2:]

for val in pos:
	print(file1[int(val)-1])