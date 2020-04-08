"""
	detecting the ciphertext encrypted by AES ECB is similar to detecting the ciphertext of a single-byte XOR encryption
	since each block (of 16 bytes in this case) is encrypted independently of previous blocks (as in a stream cipher) and with the same key, the same plaintext would result in the
	same ciphertext. so looking for repeated ciphertext blocks can help us find the ciphertext encrypted by AES ECB.
	this "flaw" in AES ECB mode opens the door to a bunch of attacks that can be caried out in order to decrypt the ciphertext
"""

BLOCK_SIZE = 16
def main():
	possibleLine = ""
	f = open("ARS_ECB_encrypted_2.txt", "r")

	cipherLines = f.readlines()

	for line in cipherLines:
		blocks = []			# list holding the blocks each of size BLOCK_SIZE forming each line
		duplicates = []
		maxDup = 0

		for i in range(0, len(line), BLOCK_SIZE):
			blocks.append(line[i:i+BLOCK_SIZE])

		for block in blocks:
			if blocks.count(block) > 1:
				duplicates.append(block)	# each time we find a repeated block we append it to the list, this will append the same block multipe times
											# but then we can use the length of the list to determine the line with the most duplicates
		if len(duplicates) > maxDup:
			maxDup = len(duplicates)
			possibleLine = line

	print("AES ECB ciphertext: \n" + possibleLine)

	f.close()

if __name__ == "__main__":
	main()
