import numpy as np


def str2vec(_str):
    """ vectorize the captcha str """
    vec = np.zeros(4 * 10)
    for i, ch in enumerate(_str):
        offset = i*10 + (ord(ch)-ord('0'))
        vec[offset] = 1
    return vec


def vec2str(vec):
    """ transform the vector to captcha str"""
    _str = ""
    for i in range(4):
        v = vec[i*10: (i+1)*10]
        _str += str(np.argwhere(v == 1)[0][0])
    return _str


# print vec2str(str2vec("0819"))
