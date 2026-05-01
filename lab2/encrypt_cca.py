from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

header_size = 54
with open("original.bmp", "rb") as f:
    data = f.read()

header = data[:header_size]
body = data[header_size:]


def encrypt_cca(plain_text, key):
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    cipher_text = aesgcm.encrypt(nonce, plain_text, None)
    return nonce + cipher_text


key = AESGCM.generate_key(bit_length=256)
with open("key_cca.txt", "wb") as f:
    f.write(key)

encrypted_data = encrypt_cca(body, key)

with open("encrypted_cca_output.bmp", "wb") as f:
    f.write(header + encrypted_data)
