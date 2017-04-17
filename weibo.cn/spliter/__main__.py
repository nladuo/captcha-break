# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
import os
#os.path.abspath(os.path.abspath(os.path.dirname(__file__)))

from spliter import *


def cli():
    parent_dir = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(parent_dir, '..', 'downloader', 'captchas'))
    images = []

    images = filter(lambda fn:os.path.splitext(fn)[1].lower() == '.png',
                    os.listdir(path))

    path2 = os.path.join(parent_dir, "dataset")
    ispliter = Spliter(path2)
    for im in images:
        im_path = os.path.join(path, im)
        print(im_path)
        ispliter.split_and_save(im_path)

if __name__ == '__main__':
    cli()