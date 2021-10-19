import config
import socket
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from os import urandom


KEY_1 = "cheiePtECB"
KEY_2 = "cheiePtXXX"

# ------------------- Nodul MC ------------------- #
sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (config.SERVER_NAME, config.SERVER_PORT)
sockt.bind(server_address)


print(f"\nServer: IP {server_address[0]} | Port {server_address[1]}\n")


sockt.listen()
node_a, address_a = sockt.accept()
node_a.send(b'a')
print(f"Nodul A s-a conectat cu adresa {address_a}")


sockt.listen()
node_b, address_b = sockt.accept()
node_b.send(b'b')
print(f"Nodul B s-a conectat cu adresa {address_b}")


encrypt_mode = node_a.recv(3)
print (f"Nodul MC a primit : {encrypt_mode}")


txt = config.AESCipher(config.KEY_CENTRAL).encrypt(KEY_1).decode('utf-8')
dec_txt = config.AESCipher(config.KEY_CENTRAL).decrypt(txt).decode('utf-8')


if encrypt_mode == b'ECB':
    encrypted_key = config.AESCipher(config.KEY_CENTRAL).encrypt(KEY_1).decode('utf-8')
else:
    encrypted_key = config.AESCipher(config.KEY_CENTRAL).encrypt(KEY_2).decode('utf-8')


encrypted_key = str.encode(encrypted_key)
node_a.send(encrypted_key)
node_b.send(encrypted_key)


start = node_b.recv(128)
node_a.send(start)


length_of_blocks = node_a.recv(8)
node_b.send(length_of_blocks)
full_message_encrypted = ""

for i in range (0, int.from_bytes(length_of_blocks, "big")):
    encrypted_block = node_a.recv(8)
    full_message_encrypted += encrypted_block.decode('UTF-8')


print(full_message_encrypted)
print(config.AESCipher(KEY_1).decrypt(full_message_encrypted).decode('UTF-8'))