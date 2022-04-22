#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 进制转换工具
def d2x(d):
    """
    :param d: int
    :return: str
    """
    return hex(d)


def d2x8(d):
    """
    :param d: int
    :return: str(len = 8)
    """
    x = d2x(d)[2:]
    if len(x) < 8:
        x = "0" * (8 - len(x)) + x
    return "0x" + x


def d2xK(d, k):
    """
    :param d: int
    :param k: int
    :return: str(len = k)
    """
    x = d2x(d)[2:]
    if len(x) < k:
        x = "0" * (k - len(x)) + x
    return "0x" + x


def d2b(d):
    """
    :param d: int
    :return: str
    """
    return bin(d)


def d2bK(d, k):
    """
    :param d: int
    :param k: int
    :return: str(len = k)
    """
    b = d2b(d)[2:]
    if len(b) < k:
        b = "0" * (k - len(b)) + b
    return "0b" + b


if __name__ == '__main__':
    binary = d2bK(255, 16)
    print("255 =", binary, type(binary))
    hexadecimal = d2xK(65535, 8)
    print("65535 =", hexadecimal, type(hexadecimal))
