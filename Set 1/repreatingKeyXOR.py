from itertools import cycle

def main():
	raw = "Burning 'em, if you ain't quick and nimble\n\
	I go crazy when I hear a cymbal"
	key = "ICE"

	raw_bytes = raw.encode("utf-8")
	encrypted_bytes = b""

	# using cycle to keep looping over the bytes in key till every byte in raw_bytes is encrypted by the appropriate byte in key
	for i, j in zip(cycle(key), raw_bytes):
		encrypted_bytes += bytes([ord(i) ^ j])

	print(encrypted_bytes.hex())

if __name__ == "__main__":
	main()