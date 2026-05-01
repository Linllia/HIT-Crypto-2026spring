from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

header_size = 54


def decrypt_cpa(encrypted_data_with_iv, key):

    iv = encrypted_data_with_iv[:16]
    cipher_text = encrypted_data_with_iv[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted_body = decryptor.update(cipher_text) + decryptor.finalize()
    return decrypted_body


with open("encrypted_output.bmp", "rb") as f:
    data = f.read()

header = data[:header_size]
encrypted_data_with_iv = data[header_size:]

with open("key.txt", "rb") as f:
    key = f.read()

data_list = list(encrypted_data_with_iv)
attack_index = 54 + 16 + 100
data_list[attack_index] = data_list[attack_index] ^ 0xFF
tampered_data = bytes(data_list)

decrypted_data = decrypt_cpa(tampered_data, key)

with open("decrypted_output.bmp", "wb") as f:
    f.write(header + decrypted_data)
