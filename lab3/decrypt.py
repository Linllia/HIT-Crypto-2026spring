from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

with open("private.pem", "rb") as f:
    private_key = f.read()

recipient_key = RSA.importKey(private_key)
cipher_rsa = PKCS1_OAEP.new(recipient_key)

with open("encrypted_aes_key.txt", "r") as f:
    encoded_key = f.read()

encrypted_aes_key = base64.b64decode(encoded_key)

try:
    aes_key = base64.b64decode(cipher_rsa.decrypt(encrypted_aes_key))
    print("对称密钥解密成功")
    print(f"AES_key = {aes_key.hex()}")
except ValueError:
    print("对称密钥解密失败")

# 解密图片
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

header_size = 54
nonce_size = 12

with open("encrypted_cca_output.bmp", "rb") as f:
    data = f.read()

header = data[:header_size]
nonce = data[header_size : header_size + nonce_size]
body = data[header_size + nonce_size :]

aesgcm = AESGCM(aes_key)

try:
    decrypted_data = aesgcm.decrypt(nonce, body, None)

    with open("decrypted_cca_output.bmp", "wb") as f:
        f.write(header + decrypted_data)
    print("图片解密成功")

except Exception as e:
    print(f"图片解密失败({e})")
