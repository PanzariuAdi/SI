from typing import SupportsComplex
import config
import socket
from Crypto import Cipher
import base64
from Crypto.Cipher import AES
from Crypto import Random
import config
import socket
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from os import urandom


sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (config.SERVER_NAME, config.SERVER_PORT)
sockt.connect(server_address)
current_node = sockt.recv(2)
print (current_node)


encrypt_mode = b'ECB'
message = encrypt_mode


if current_node == b'a':
    sockt.send(encrypt_mode)
    print (f"\nAm trimis din A : {encrypt_mode}")
    # encrypted_key = sockt.recv(128)
else:
    # if encrypt_mode == b'ECB':
        # sockt.send()
    print (f"\nAm primit in B : {encrypt_mode}")
    

encrypted_key = sockt.recv(128)
# print(encrypted_key)
decrypted_key = config.AESCipher(config.KEY_CENTRAL).decrypt(encrypted_key).decode('utf-8')

if current_node == b'b':
    start = "start"
    start = str.encode(start)
    sockt.send(start)

    length_of_blocks = int.from_bytes(sockt.recv(1), "big")
    print(f"AIA E : {length_of_blocks}")
    
else: # Node a
    start = sockt.recv(16).decode('utf-8')
    if start == "start":
        f = open("story.txt", "r")
        decrypted_text = f.read()
        encrypted_text = config.AESCipher(decrypted_key).encrypt(decrypted_text).decode('UTF-8')

        blocks_from_file = [encrypted_text[i: i + 8] for i in range (0, len(encrypted_text), 8)]
        length_of_blocks = len(blocks_from_file)
        print(f"BAAA : {length_of_blocks}")
        sockt.send(bytes([length_of_blocks]))

        for i in range (0, length_of_blocks):
            # encrypted_block = config.AESCipher(decrypted_key).encrypt(blocks_from_file[i]).decode('UTF-8')
            sockt.send(blocks_from_file[i].encode())