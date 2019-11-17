import base64

from Crypto.Cipher import AES
from pbkdf2 import PBKDF2

from paisa_core.config import SALT

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]


class AESCipher:

    def __init__(self, key):
        self.salt = str(bytes(SALT).decode()).encode()
        self.key = key

    def encrypt(self, raw):
        # Derive key
        raw = pad(raw)
        generator = PBKDF2(self.key, self.salt)
        aes_iv = generator.read(16)
        aes_key = generator.read(32)
        # Crypto
        mode = AES.MODE_CBC
        cipher = AES.new(aes_key, mode, IV=aes_iv)
        return base64.b64encode(cipher.encrypt(raw)).decode()

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        generator = PBKDF2(self.key, self.salt)
        aes_iv = generator.read(16)
        aes_key = generator.read(32)
        mode = AES.MODE_CBC
        cipher = AES.new(aes_key, mode, IV=aes_iv)
        return unpad(cipher.decrypt(enc))



# crypt = AESCipher("58xZ4dP3K762WtpDVt5EjqnNdfTZD844s8CAW5gGy9w7WMhuVtUPJ7xU2EMCrFQk")
# print("{0}".format(crypt.encrypt("mkjhytfd48j")))
# OUTPUT: XB+RbZ6RIymFbWFmjoTf5w==



