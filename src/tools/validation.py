import re

from constants import message
from exceptions import exception

def atLeastUppercase(str):
    return re.search("[A-Z]", str)

def atLeastLowercase(str):
    return re.search("[a-z]", str)

def atLeastOneNumber(str):
    return re.search("[0-9]", str)

def minimum(str, length):
    return len(str) >= length

def maximum(str, length):
    return len(str) <= length

def signupValidation(username, password):
    try:
        totoalMsg = ""
        # length
        if(not minimum(username, 3) or not maximum(username, 32)):
            totoalMsg += message.USERNAME_LENGTH_INCORRECT + " " 

        if(not minimum(password, 8) or not maximum(password, 32)):
            totoalMsg += message.PASSWORD_LENGTH_INCORRECT + " "
        
        passwordMsg = ""
        # uppercase
        if(not atLeastUppercase(password)):
            passwordMsg += message.PASSWORD_INCLUDE_UPPERCASE + ", " 
        
        # lowercase
        if(not atLeastLowercase(password)):
            passwordMsg += message.PASSWORD_INCLUDE_LOWERCASE + ", " 
        
        # number
        if(not atLeastOneNumber(password)):
            passwordMsg += message.PASSWORD_INCLUDE_NUMBER + ", "

        if(passwordMsg):
            totoalMsg += message.PASSWORD_INCLUDE + passwordMsg

        return (True, "") if not totoalMsg else (False, totoalMsg)
    except Exception:
        raise exception.ServerError(message.UNKNOWN_ERROR)