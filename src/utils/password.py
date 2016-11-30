#!/usr/bin/python2.7


# a pool of all characters allowed in a password
POOL = '1234567890!@#$%^&*()_-+=~qwertyuiop{[]}asdfghjkl:;"zxcvbnm,./<>?''QWERTYUIOPLKJHGFDSAZXCVBNM'

SUCCESS_AUTH = "success"
FAILURE_AUTH = "failure"


def bruteforce(pwd, cur_len, min_dig, max_dig):
    """Password permutation for variable lengths
    min_dig = int: minimum number of digits, default 5
    max_dig = int: maximum number of digits, default 12
    """
    if cur_len > max_dig:
        return
    if cur_len >= min_dig:
        yield pwd
    for x in POOL:
        for y in bruteforce(pwd+x, cur_len+1, min_dig, max_dig):
            yield y


def bruteforce_offline():
    """3579140 common passwords, easy to attack
    """
    file = '../../data/password_dictionary.txt'
    with open(file) as f:
        for line in f:
            yield line.strip()


def bruteforce_with_meta(name, year, month, day):
    """Given name and birthday
    name = string: username
    year = string: birth year
    month = string: birth month
    day = string: birth day
    """
    pass
    # some combination of metadata
