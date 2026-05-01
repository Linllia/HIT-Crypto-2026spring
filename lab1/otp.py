import secrets


def otp_encrypt(text):
    text_bytes = text.encode("ascii")
    key = secrets.token_bytes(len(text_bytes))
    ciphertext = bytes([p ^ k for p, k in zip(text_bytes, key)])
    return key, ciphertext


message = "Hello world!"
key, cipher = otp_encrypt(message)
print(f"明文: {message}")
print(f"明文长度：{len(message.encode('ascii'))}")
print(f"密钥 (Hex): {key.hex()}")
print(f"密钥长度: {len(key)}")
print(f"密文 (Hex): {cipher.hex()}")

decrypted = bytes([c ^ k for c, k in zip(cipher, key)]).decode("ascii")
print(f"解密后: {decrypted}")
