from Crypto.Cipher import AES
import base64
from django.conf import settings
from Crypto.Util.Padding import pad, unpad

BLOCK_SIZE = 16

def encrypt(raw_id):
    aes = AES.new(settings.SECRET_KEY, AES.MODE_ECB)
    raw_id = str(raw_id)
    encoded = base64.b64encode(aes.encrypt(pad(raw_id.encode(), BLOCK_SIZE)))
    return base64.b64encode(encoded)
    # return raw_id


def decrypt(encrypted_id):
    try:
        encrypted_id = base64.b64decode(encrypted_id.encode('utf-8'))
        aes = AES.new(settings.SECRET_KEY, AES.MODE_ECB)
        encoded = unpad(aes.decrypt(base64.b64decode(encrypted_id)), BLOCK_SIZE)
        return encoded.decode('UTF-8')
    except Exception as e:
        print(e)