#!/usr/bin/env python
# coding:utf-8

from __future__ import absolute_import
from __future__ import print_function

import os
from _recognize_p import start_recognize_daemon


def recognize(captcha_path_set):
    p = start_recognize_daemon()

    result_set = []
    for captcha_path in captcha_path_set:
        p.stdin.write(captcha_path.encode()+b'\n')
        try:
            p.stdin.flush()
        except OSError:
            cracked = True
        else:
            cracked = False

        if cracked:
            raise OSError('the recognize daemon process cracked up :(')
        result = p.stdout.readline().strip().decode()
        result_set.append(result)
        #print(result)

    p.stdin.write(b'$exit\n')
    p.stdin.flush()

    p.kill()

    return result_set

def cli():
    import sys
    captcha_path_set=[]
    for captcha_path in sys.argv[1:]:
        captcha_path_set.append(os.path.abspath(captcha_path))

    result_list = recognize(captcha_path_set)
    for result in result_list:
        print(result)


if __name__ == '__main__':
    cli()
