"""
	here we are decrypting AES-128 with a 16-byte key in ECB mode
	each block is divided into BLOCKSIZE which must be 16, 24 or 32 bytes long, depending if AES-128, AES-192 or AES-256 is used, and so does the key, if the last block is shorter than BLOCKSIZE it gets padded.
	note that ECB can be attacked easily mostly because its deterministic: which means that a block encrypted under a specific key will always result in the same block of ciphertext, also the key does not change form one block
	to the other (static key).
	The attacks dont target AES itself since AES is "secure" but rather they target the encryption schemes around the AES system
"""

from Crypto.Cipher import AES
from base64 import b64decode

# returns decrypted bytes
def AES_ECB_decrypt(ciphertext, key):
	cipher = AES.new(key, AES.MODE_ECB)
	return cipher.decrypt(ciphertext)


def main():
	key = b"YELLOW SUBMARINE"
	f = open("AES_ECB_encrypted.txt", "r")

	ciphertext = b64decode(f.read())
	plaintext = AES_ECB_decrypt(ciphertext, key)

	print(plaintext.decode("utf-8"))

	f.close()

if __name__ == "__main__":
	main()