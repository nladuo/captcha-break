# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import sys
import os
from recognize import recognize

def cli():

    if len(sys.argv)>1:
        path = sys.argv[1]
    else:
        path = 'test_set'

    capcha_tuple_list = []
    captcha_list = []
    for fn in os.listdir(path):
        name, ext = os.path.splitext(fn)
        if ext == '.png' and len(name)==4: # assure that is test image file
            captcha_list.append(os.path.join(path, fn))

    result_list = recognize(captcha_list)
    correct = 0
    for label, result in zip(captcha_list, result_list):
        print('%s %s '%(label, result), end='')
        if label.lower() == result.lower():
            print(True)
            correct += 1
        else:
            print(False)

    print('accuracy: %f'%(correct/len(captcha_list)))

if __name__ == '__main__':
    cli()

