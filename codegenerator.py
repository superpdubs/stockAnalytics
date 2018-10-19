import random
from Cryptodome.Cipher import AES
from binascii import b2a_hex, a2b_hex

class Verfication:

    def generate_code(self):
        num = random.randint(100,999)
        cap1 = chr(random.randint(65,90))
        cap2 = chr(random.randint(65,90))
        low = chr(random.randint(97,122))
        vercode = cap1 + str(num) + cap2 + low
        return vercode





class Encryption():

    def __init__(self):
        self.key = 'keyskeyskeyskeys'

    def encrypt_Code(self, text):
        cryptor = AES.new(self.key.encode("utf8"), AES.MODE_CBC, b'0000000000000000')
        length = 16
        count = len(text)
        if count < length:
            add = (length - count)
            # \0 backspace
            text = text + ('\0' * add)
        elif count > length:
            add = (length - (count % length))
            text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text.encode("utf8"))
        return b2a_hex(self.ciphertext)


    def decrpty_Code(self, text):
        cryptor = AES.new(self.key.encode("utf8"), AES.MODE_CBC, b'0000000000000000')
        plain_text = cryptor.decrypt(a2b_hex(text)).decode()
        return plain_text.rstrip('\0')


