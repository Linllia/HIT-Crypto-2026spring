from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

header_size = 54
with open("original.bmp", "rb") as f:
    data = f.read()

header = data[:header_size]
body = data[header_size:]


def encrypt_cpa(plain_text, key):
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(plain_text) + encryptor.finalize()
    return iv + cipher_text


key = os.urandom(32)

with open("key.txt", "wb") as f:
    f.write(key)

encrypted_body = encrypt_cpa(body, key)

with open("encrypted_output.png", "wb") as f:
    f.write(header + encrypted_body)
