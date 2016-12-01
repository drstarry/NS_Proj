#!/usr/bin/python2.7

import itertools

# a pool of all characters allowed in a password
pool = '1234567890!@#$%^&*()_-+=~qwertyuiop{[]}asdfghjkl:;"zxcvbnm,.`\/|<>?''QWERTYUIOPLKJHGFDSAZXCVBNM'

# number = '1234567890'
# special_chr = '!@#$%^&*()_-+`=~{[]}:;",./<>?\|''
# lower_case = 'qwertyuiopasdfghjklzxcvbnm'
# upper_case = 'QWERTYUIOPLKJHGFDSAZXCVBNM'
# Upper, lower, number, special characters
char_set = [26, 26, 10, 33]


def get_count(l, comb):
    result = 0
    for n in range(1, comb+1):
        for sub_char_set in itertools.combinations(char_set, n):
            print sub_char_set
            char_n = sum(sub_char_set)
            for m in range(n, 0, -1):
                sign = (-1) ** (n - m)
                for sets in itertools.combinations(sub_char_set, m):
                    result += sign * sum(sets) ** l
    return result


def enumeration(comb, min_dig, max_dig):
    """The number of enumeration of a password
    comb = int: number of combination of character type
    min_dig = int: min length of the password
    max_dig = int: max length of the password
    """
    return sum(get_count(l, comb) for l in range(min_dig, max_dig + 1))


def bruteforce(pwd, cur_len, min_dig, max_dig):
    """Password permutation for variable lengths
    min_dig = int: minimum number of digits, default 5
    max_dig = int: maximum number of digits, default 12
    """
    if cur_len > max_dig:
        return
    if cur_len >= min_dig:
        yield pwd
    for x in pool:
        for y in bruteforce(pwd+x, cur_len+1, min_dig, max_dig):
            yield y


def bruteforce_offline(filename):
    """3579140 common passwords, easy to attack
    """
    with open(filename) as f:
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

if __name__ == '__main__':
    # lowercase, uppercase, numbers, special characters
    comb, min_dig, max_dig = 2, 6, 6
    n = enumeration(comb, min_dig, max_dig)
    print n, comb, min_dig, max_dig
