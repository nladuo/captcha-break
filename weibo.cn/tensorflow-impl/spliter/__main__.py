# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""

"""
import os
import sys
from spliter import *


def cli():
    if len(sys.argv) != 2:
        print("Usage: ./recoginze.py [image_path]")
        exit(-1)

    if not os.path.exists(sys.argv[1]):
        print(sys.argv[1], "is not exists.")
        exit(-1)
    ispliter = Spliter("./")
    ispliter.split_and_save(sys.argv[1])

if __name__ == '__main__':
    cli()
