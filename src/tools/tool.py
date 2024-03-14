import hashlib

from constants import message
from exceptions import exception

def verifyUserPassword(password, hash):
    try:
        newHash = getHash(password)
        return newHash == hash
    except Exception:
        raise exception.ServerError(message.UNKNOWN_ERROR)
    
def getHash(str):
    try:
        m = hashlib.md5()
        m.update(str.encode("utf-8"))
        h = m.hexdigest()
        return h
    except Exception:
        raise exception.ServerError(message.UNKNOWN_ERROR)