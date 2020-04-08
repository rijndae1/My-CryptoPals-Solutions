
def main():
	hex1 = input("Enter hex str1: ")
	hex2 = input("Enter hex str2: ")
	xored = ""

	# using default zip behavior works fine here since both hex strs have the same length
	for i,j in zip(hex1, hex2):
		xored += hex(int(i, 16) ^ int(j, 16)).lstrip("0x")	# lstrip is a quick way to get rid of 0x

	print(xored)	

if __name__ == "__main__":
	main()