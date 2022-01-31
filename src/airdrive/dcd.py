from .ext import *
import binascii


PK = binascii.unhexlify(SD[::-1]).decode()
