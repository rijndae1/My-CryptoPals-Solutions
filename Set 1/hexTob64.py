from binascii import unhexlify
from base64 import b64encode

def main():
	hexStr = input("Enter hex: ")
	print(b64encode(unhexlify(hexStr)).decode("ascii"))

if __name__ == "__main__":
	main()