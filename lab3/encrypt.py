from Crypto.PublicKey import RSA

# 生成密钥对
key = RSA.generate(4096)

private_key = key.export_key()
with open("private.pem", "wb") as f:
    f.write(private_key)

public_key = key.publickey().export_key()
with open("public.pem", "wb") as f:
    f.write(public_key)

# 对称密钥加密图片
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


aes_key = AESGCM.generate_key(bit_length=128)
encrypted_data = encrypt_cca(body, aes_key)

with open("encrypted_cca_output.bmp", "wb") as f:
    f.write(header + encrypted_data)

# 加密对称密钥
from Crypto.Cipher import PKCS1_OAEP
import base64

recipient_key = RSA.importKey(public_key)
cipher_rsa = PKCS1_OAEP.new(recipient_key)
encoded_key = base64.b64encode(aes_key)
encrypted_key = cipher_rsa.encrypt(encoded_key)
final_base64_result = base64.b64encode(encrypted_key).decode("utf-8")

with open("encrypted_aes_key.txt", "w") as f:
    f.write(final_base64_result)
