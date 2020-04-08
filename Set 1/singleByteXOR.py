
# not the best scoring method but its works in this case :p
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

def main():
	encrypted = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
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

	print(possibleStr)
	print(hex(key))

if __name__ == "__main__":
	main()