# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""

"""
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
from spliter import Spliter

def split_dataset():
    weibo_cn_dir = os.path.dirname(os.path.dirname(__file__))
    path = os.path.abspath(os.path.join(weibo_cn_dir, 'downloader', 'captchas'))

    images = filter(lambda fn:os.path.splitext(fn)[1].lower() == '.png',
                    os.listdir(path))

    dataset_path = os.path.join(os.path.dirname(__file__), "dataset")
    ispliter = Spliter(dataset_path)
    for im in images:
        im_path = os.path.join(path, im)
        print(im_path)
        ispliter.split_and_save(im_path)


def cli():
    if len(sys.argv) == 1:
        split_dataset()
    else:
        ispliter = Spliter("./")
        ispliter.split_and_save(sys.argv[1])

if __name__ == '__main__':
    cli()
