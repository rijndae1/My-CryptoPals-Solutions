from base64 import b64decode

def hamming(b1, b2):
	# finding the number of differing bits (hamming distance) between 2 strings of length KEYLEN
	# can be done using XOR, since the bits that are equal will be zeroed out when XORed
	# in order to count the bits that are still set after XOR we use binary shifting

	dist = 0

	if len(b1) != len(b2):
		print("Cant calculate hamming distancce for 2 chunks of different length")
		return

	for i, j in zip(b1, b2):
		xored = i ^ j

		bitsset = 0

		while xored > 0:
			# check if the LSB is set
			bitsset += xored & 0x00000001
			# prepare to check the bit after it
			xored >>= 1

		# add the number of bits set for each byte to distance
		dist += bitsset

	return dist

def keylen(ciphertext):
	lowest = 0
	possibleKeyLen = 0

	# 2 <= KEYLEN && KEYLEN <= 40
	for keyLen in range(2, 41):
		# list that holds distances for each KEYLEN to be averaged
		dists = []

		start = 0
		end = start + keyLen

		# loop over the ciphertext 2 adjacent chunks at a time each of length KEYLEN
		while(1):
			chunk1 = ciphertext[start:end]
			chunk2 = ciphertext[end:end+keyLen]

			if len(chunk2) < keyLen:
				break

			# calculate their hamming distance and add it to the normalized dist list
			dist = hamming(chunk1, chunk2)
			normalizedDist = dist / keyLen

			dists.append(normalizedDist)

			# move to the next 2 adjacent chunks
			start = end + keyLen
			end += 2*keyLen

		# calculate the average of distances for each KEYLEN
		avgDist = sum(dists) / len(dists)
		dists = []

		# store the lowest average of normalized hamming distances and the KEYLEN for which this distance was calculated (the possible KEYLEN)
		if lowest == 0 or avgDist < lowest:
			lowest = avgDist
			possibleKeyLen = keyLen

	return possibleKeyLen

def transpose(ciphertext, keyLen):
	# dict with keys: 0,...,Keylen-1
	groups = dict.fromkeys(range(keyLen))

	# keeps track of which group to append to based on keyLen
	i = 0
	for byte in ciphertext:
		if i == keyLen:
			i = 0

		# initialize dict values to empty lists
		if groups[i] == None:
			groups[i] = []

		groups[i].append(byte)
		i += 1

	return groups

def calcKey(groups):
	# a similar scoring technique to the one I used in detectSingleByteXOR
	freqChars = "ETAOIN SHRDLU"
	key = ""

	for i in groups:
		highScore = 0
		keyByte = ''
		xored = []

		for j in range(256):
			# XOR each group by all possible bytes
			xored = [j ^ byte for byte in groups[i]]

			xoredBytes = bytes(xored)
			try:
				xoredStr = xoredBytes.decode("utf-8")
			except UnicodeError:
				pass

			# Increase the score for each match
			score = 0
			for k in xoredStr.upper():
				if k in freqChars:
					 score += 1

			# add the byte with the highest score to key
			# this byte was most probably the one used in XORing
			if score > highScore:
				highScore = score
				keyByte = chr(j)

		key += keyByte
	return key

def decrypt(ciphertext, key):
	plaintext = b''
	keyBytes = key.encode("utf-8")
	i = 0

	# iterate over kEYLEN ciphertext blocks XORing each byte by the corresponding byte in key
	for byte in ciphertext:
		if i == len(key):
			i = 0

		plaintext += bytes([byte ^ keyBytes[i]])
		i += 1

	return plaintext.decode("utf-8")

def main():

	f = open("b64_encoded.txt", "r")

	# decode base64 and prepare for next steps
	b64Encoded = f.read()
	decoded = b64decode(b64Encoded)

	# now we have to find the KEYLEN which is the len that produces the shortest averaged hamming distance between all adjacent KEYLEN chunks of ciphertext
	# we divide our ciphertext into KEYLEN blocks of len KEYLEN and group together the bytes that will be XORed by the same byte in the key
	# so if KEYLEN is x then the 1st group would contain bytes: ciphertext[0], ciphertext[x],... the 2nd: ciphertext[1], ciphertext[x+1],... 
	# then we try to decrypt each block on its own by a byte and add the byte with the highest score to the key
	# once we have the possible key we can decrypt the ciphertext
	groups = transpose(decoded, keylen(decoded))
	key = calcKey(groups)
	print("Possible key: " + key + "\n")
	print(decrypt(decoded, key))

	f.close()
if __name__ == "__main__":
	main()
