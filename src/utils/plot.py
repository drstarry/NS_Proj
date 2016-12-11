#!/usr/bin/python2.7

import matplotlib.pyplot as plt
import numpy as np

from password import enumeration


def password_strength():
    # different length
    x = [6, 7, 8, 9]
    y = []
    for _x in x:
        _y = []
        for c in range(1, 5):
            _y.append(enumeration(c, _x, _x))
        y.append(tuple(_y))
    plt.xlabel('Number of digits')
    plt.ylabel('Number of guesses needed to crack')
    plt.title('Password strength based on password length')
    plt.plot(x, y)
    plt.savefig('variable_len.png')
    plt.close()

    # different combinations
    c = range(5)
    y = []
    for _c in c:
        _y = []
        for l in range(6, 10):
            _y.append(enumeration(_c, l, l))
        y.append(tuple(_y))
    plt.xlabel('Number of character sets contained')
    plt.ylabel('Number of guesses needed to crack')
    plt.title('Password strength based on character sets')
    plt.plot(c, y)
    plt.savefig('variable_con.png')
    plt.close()


def main():
    password_strength()

if __name__ == '__main__':
    main()
