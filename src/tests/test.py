import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.validation import signupValidation
from tools.tool import verifyUserPassword, getHash
from exceptions import exception

class TestUserMethods(unittest.TestCase):
    def test_signupValidation_username_length(self):
        # validate username
        self.assertEqual(signupValidation("test", "tesT1234"), (True, ''))
        # type error
        self.assertRaises(exception.ServerError, signupValidation, 123, "tesT1234")
        # too short
        self.assertEqual(signupValidation("tt", "tesT1234"), (False, 'Username must be between 3 and 32 characters in length. '))
        # too long
        self.assertEqual(signupValidation("ttttttttttttttttttttttttttttttttttt", "tesT1234"), (False, 'Username must be between 3 and 32 characters in length. '))

    def test_signupValidation_password_length(self):
        # validate password
        self.assertEqual(signupValidation("test", "tesT1234"), (True, ''))
        # type error
        self.assertRaises(exception.ServerError, signupValidation, "test", 123)
        # too short
        self.assertEqual(signupValidation("test", "tT345"), (False, 'Passwords must be between 8 and 32 characters in length. '))
        # too long
        self.assertEqual(signupValidation("test", "1Tttttttttttttttttttttttttttttttttt"), (False, 'Passwords must be between 8 and 32 characters in length. '))

    def test_signupValidation_password_format(self):
        # no number
        self.assertEqual(signupValidation("test", "tesTtest"), (False, 'Passwords must be to include: one number, '))
        # no lowercase
        self.assertEqual(signupValidation("test", "test1234"), (False, 'Passwords must be to include: one uppercase character, '))
        # no uppercase
        self.assertEqual(signupValidation("test", "TEST1234"), (False, 'Passwords must be to include: one lowercase character, '))
        # no number no lowercase
        self.assertEqual(signupValidation("test", "TESTTEST"), (False, 'Passwords must be to include: one lowercase character, one number, '))
        # no number no uppercase
        self.assertEqual(signupValidation("test", "testtest"), (False, 'Passwords must be to include: one uppercase character, one number, '))
        # no lowercase no uppercase
        self.assertEqual(signupValidation("test", "12341234"), (False, 'Passwords must be to include: one uppercase character, one lowercase character, '))

    def test_getHash(self):
        # get "a" hash 
        self.assertEqual(getHash("a"), '0cc175b9c0f1b6a831c399e269772661')
        # get 32 length string hash
        self.assertEqual(getHash("fdsgdshdghghsghfghdhgdghodhgdhgd"), 'bb3a5fcceff36a99e3e85f212362b2cc')
        # type error
        self.assertRaises(exception.ServerError, getHash, 1)

    def test_verifyUserPassword(self):
        # verify password
        self.assertTrue(verifyUserPassword("a", "0cc175b9c0f1b6a831c399e269772661"))
        # incorrect password 
        self.assertFalse(verifyUserPassword("a", "a"))
        # 32 length string
        self.assertTrue(verifyUserPassword("fdsgdshdghghsghfghdhgdghodhgdhgd", "bb3a5fcceff36a99e3e85f212362b2cc"))
        # type error
        self.assertRaises(exception.ServerError, verifyUserPassword, 1, 1)
        # two 32 length string
        self.assertFalse(verifyUserPassword("0cc175b9c0f1b6a831c399e269772661", "0cc175b9c0f1b6a831c399e269772661"))

if __name__ == '__main__':
    unittest.main()