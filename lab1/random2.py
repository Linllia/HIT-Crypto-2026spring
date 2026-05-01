import os
import binascii

raw_bytes = os.urandom(16)
hex_string = binascii.hexlify(raw_bytes).decode()

print(hex_string)
