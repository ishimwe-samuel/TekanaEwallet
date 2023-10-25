import math
import random


class CodeGenerator:
    @classmethod
    def generate_otp(cls, size: int = 6,digit=False):
        OTP = ""            
        if digit:
            for _ in range(6):
                digit = str(random.randint(0, 9))
                OTP += digit
            return OTP
        else:
            string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            length = len(string)
            for i in range(size):
                OTP += string[math.floor(random.random() * length)]
            return OTP
    otp = ""



    @classmethod
    def generate_account_number(cls):
        account_number = ''.join(str(random.randint(0, 9)) for _ in range(10))
        return account_number
