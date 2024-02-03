from datetime import datetime, timedelta
from base64 import b64decode, b64encode
import os

from utils.aes import AESModeOfOperationCBC


BLOCK_SIZE = 16

def encrypt(plain_text: str, key):
    plain_text = plain_text.ljust(len(plain_text) + (BLOCK_SIZE - len(plain_text) % BLOCK_SIZE) % BLOCK_SIZE, '\0')
    iv = os.urandom(BLOCK_SIZE)
    aes = AESModeOfOperationCBC(key, iv)
    buffer = plain_text.encode('utf-8')
    blocks_count = len(buffer) // BLOCK_SIZE
    cipher_text = b''
    for i in range(blocks_count):
        block = buffer[i * BLOCK_SIZE:i * BLOCK_SIZE + BLOCK_SIZE]
        cipher_text += aes.encrypt(block)

    cipher_text = iv + cipher_text

    return b64encode(cipher_text).decode('utf-8')

def create_access_token(mac_address: str, duration: int, key: str) -> str:
    expiration_datetime = datetime.now() + timedelta(hours=duration)

    return encrypt(f'{mac_address}->{expiration_datetime.isoformat()}Z', b64decode(key))