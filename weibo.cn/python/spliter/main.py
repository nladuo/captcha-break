#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import print_function

import os
from spliter import Spliter


def split_dataset():
    path = os.path.abspath(os.path.join("../", 'downloader', 'captchas'))

    images = filter(lambda fn: os.path.splitext(fn)[1].lower() == '.png',
                    os.listdir(path))
    dataset_path = os.path.join("./", "dataset")

    ispliter = Spliter(dataset_path)
    for im in images:
        im_path = os.path.join(path, im)
        print(im_path)
        ispliter.split_and_save(im_path)

if __name__ == '__main__':
    split_dataset()
