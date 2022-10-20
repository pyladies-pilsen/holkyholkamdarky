"""Provide simple password decryption

Expect admin password hash made by

"""

import os
import hashlib
import configparser

CREDENTIALS_FILE =  ".credentials.ini"

def text_to_number(text):
    """Convert text to numbers Not testest for long texts"""
    numbers = map(lambda x: ord(x)+1000, text)
    numbers_as_string = map(lambda x: str(x), numbers)
    string_as_numbers = ''.join(numbers_as_string)
    return string_as_numbers

def numbers_to_text(number):
    """Convert number to text"""
    number_as_string = str(number)
    string_from_numbers = ''
    for i in range(0,len(number_as_string),4):
        char_from_number = chr(int(number_as_string[i:i+4])-1000)
        string_from_numbers += char_from_number
    return string_from_numbers

def get_localhost_admin_passwd_hash():
    return hashlib.sha512("x".encode()).hexdigest()

def hash_of_password(text):
    passwd_hash = hashlib.sha512(text).hexdigest()
    # print(passwd_hash)
    return passwd_hash

def hash_check(stored_hash, passwd):
    passwd_hash = hashlib.sha512(passwd.encode()).hexdigest()
    if stored_hash == passwd_hash:
        return True
    else:
        return False

def read_from_ini(file):
    config = configparser.ConfigParser()
    if os.path.isfile(file):
        config.read(file)
    else:
        print(file, "file is not found, credential_example.ini file is used. Admin password is 'x', Email cannot by send.")
        config.read("credential_example.ini")

    ADMIN_PASSWD_HASH = config['ADMIN']['hash']
    EMAIL_SMTP_URL = config['EMAIL']['smtpserver']
    EMAIL_SMTP_PORT = config['EMAIL']['port']
    EMAIL_USERNAME = config['EMAIL']['username']
    EMAIL_PASSWD = numbers_to_text(config['EMAIL']['password_in_no'])

    return ADMIN_PASSWD_HASH, EMAIL_SMTP_URL, EMAIL_SMTP_PORT, EMAIL_USERNAME,EMAIL_PASSWD
