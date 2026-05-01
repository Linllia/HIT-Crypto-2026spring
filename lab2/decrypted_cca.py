from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

header_size = 54
nonce_size = 12

with open("encrypted_cca_output.bmp", "rb") as f:
    data = f.read()

header = data[:header_size]
nonce = data[header_size : header_size + nonce_size]
body = data[header_size + nonce_size :]

with open("key_cca.txt", "rb") as f:
    key = f.read()

# 尝试篡改密文
body_list = list(body)
changed_index = 70
body_list[changed_index] = body_list[changed_index] ^ 0xFF
body = bytes(body_list)

aesgcm = AESGCM(key)

try:
    decrypted_data = aesgcm.decrypt(nonce, body, None)

    with open("decrypted_cca_output.bmp", "wb") as f:
        f.write(header + decrypted_data)
    print("解密成功")

except Exception as e:
    print(f"解密失败({e})")
