from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Hash import HMAC, SHA256
import sys
import base64

flag = "kurenaifCTF{POOOOOOOOOOOOOOOOOOOOODLE}"

def add_digest(b, secret):
    h = HMAC.new(secret, digestmod=SHA256)
    h.update(b)
    return b + h.digest()

def check_digest(b, mac, secret):
    h = HMAC.new(secret, digestmod=SHA256)
    h.update(b)
    return h.digest() == mac
    try:
        h.verify(mac)
        return True
    except ValueError:
        return False

def comm():
    ### input prefix###
    prefix = input(">> ")

    ### input suffix ###
    suffix = input(">> ")

    ### make cipher ###
    message = prefix + flag + suffix

    message = message.encode("utf-8")

    key = get_random_bytes(16)
    message = add_digest(message, key)
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    c = base64.b64encode(cipher.encrypt(pad(message, AES.block_size))).decode('utf-8')
    print("cipher:", c, flush=True)

    ### validate ###
    c = input(">> ")
    cipher = AES.new(key, AES.MODE_CBC, iv)
    message = cipher.decrypt(base64.b64decode(c))
    message = message[:-message[-1]]
    message, mac = message[:-32], message[-32:]
    if check_digest(message, mac, key):
        print("result: ok", flush=True)
    else:
        print("result: ng", flush=True)

while True:
    comm()
