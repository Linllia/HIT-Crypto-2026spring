# 得到私钥
from Crypto.PublicKey import RSA
from Crypto.Util.number import inverse, GCD
import base64
from Crypto.Cipher import PKCS1_OAEP

with open("public_key1.pem", "rb") as f:
    public_key1 = f.read()
with open("public_key2.pem", "rb") as f:
    public_key2 = f.read()

key1 = RSA.importKey(public_key1)
key2 = RSA.importKey(public_key2)

n1, e1 = key1.n, key1.e
n2, e2 = key2.n, key2.e

p = GCD(n1, n2)

if p > 1:
    print("成功找到公共因子p")
    q1 = n1 // p
    phi1 = (p - 1) * (q1 - 1)
    d1 = inverse(e1, phi1)
    private_key = RSA.construct((n1, e1, d1, p, q1))
    print(private_key)

    with open("private_key.pem", "wb") as f:
        f.write(private_key.export_key())
    print("成功生成私钥")
else:
    print("未能找到公共因子p")

# 根据私钥解密对称密钥
with open("encrypted_aes_key.txt", "r") as f:
    encoded_key = f.read()

encrypted_aes_key = base64.b64decode(encoded_key)

with open("private_key.pem", "rb") as f:
    private_key = f.read()

recipient_key = RSA.importKey(private_key)
cipher_rsa = PKCS1_OAEP.new(recipient_key)

try:
    aes_key = base64.b64decode(cipher_rsa.decrypt(encrypted_aes_key))
    print("对称密钥解密成功")
    print(f"AES_key = {aes_key.hex()}")
except ValueError:
    print("对称密钥解密失败")

# 解密图片
from Crypto.Cipher import AES
from PIL import Image
import io
import struct

img = Image.open("enc1.png").convert("RGBA")
pixels = list(img.getdata())

last_pixel = pixels[-1]
k = (last_pixel[0] << 24) | (last_pixel[1] << 16) | (last_pixel[2] << 8) | last_pixel[3]
pixels = pixels[:-k]
cipher_bytes = b"".join(bytes(p) for p in pixels)

iv = cipher_bytes[:16]
ciphertext = cipher_bytes[16:]

print(f"[+] IV = {iv.hex()}")

cipher = AES.new(aes_key, AES.MODE_CBC, iv)
plaintext = cipher.decrypt(ciphertext)

pad_len = plaintext[-1]
plaintext = plaintext[:-pad_len]

print(f"[+] PKCS7 padding removed: {pad_len} bytes")

width = img.width
height = len(plaintext) // (4 * width)

print(f"[+] output size = {width} x {height}")

img_out = Image.frombytes("RGBA", (width, height), plaintext)
img_out.save("out.png")
