
def str_score(decrypted):
	score = 0
	letter_scores = {
    'e': 10,
    't': 9,
    'a': 8,
    'o': 7,
    'i': 6,
    'n': 5,
    's': 4,
    'r': 3,
    'h': 2,
    'd': 1,
	}

	for i in decrypted:
		if i in letter_scores:
			score += letter_scores[i]

	return score

# returns tuple {max score for a string, possible string}
def findStrMaxScore(encrypted):
	ciphertext = bytes.fromhex(encrypted)
	maxScore = 0
	possibleStr = ""
	key = 0

	# we knwo that the decrypted string is printable
	# since the key is 1 byte bruteforcing makes sense here
	for i in range(256):
		curScore = 0
		decrypted = b""

		for j in ciphertext:
			decrypted += bytes([i ^ j])
		# try to encode the decrypted bytes using utf-8
		try:
			curScore = str_score(decrypted.decode("utf-8"))
			if curScore > maxScore:
				maxScore = curScore
				possibleStr = decrypted.decode("utf-8")
				key = i
		except UnicodeError:
			pass

	return maxScore, possibleStr

# same task as challenge 3 but applied to more than 1 encrypted str
def main():
	encryptedStrings = open('XORed_strings.txt').read().splitlines()
	mostLikelyStr = ""
	curMax = 0
	m = 0

	for encrypted in encryptedStrings:
		# only the most likely strings are the ones being returned
		curMax, curStr = findStrMaxScore(encrypted)
		if(curMax > m):
			m = curMax
			mostLikelyStr = curStr
	print(mostLikelyStr)

if __name__ == "__main__":
	main()