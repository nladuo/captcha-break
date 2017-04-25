#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function
from __future__ import division

import sys
import os
from recognize import recognize

recognize_dir = os.path.dirname(os.path.abspath(__file__))

def cli():

    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = os.path.join(recognize_dir, 'test_set')

    captcha_list = []
    for fn in os.listdir(path):
        name, ext = os.path.splitext(fn)
        if ext == '.png' and len(name) == 4:  # assure that is test image file
            captcha_list.append(os.path.join(path, fn))

    result_list = recognize(captcha_list)
    correct = 0
    for path, result in zip(captcha_list, result_list):
        label = os.path.splitext(os.path.basename(path))[0][:4]
        print('%04s %04s ' % (label, result), end='')
        if label.lower() == result.lower():
            print(True)
            correct += 1
        else:
            print(False)

    print('accuracy: %f' % (correct/len(captcha_list)))

if __name__ == '__main__':
    cli()

