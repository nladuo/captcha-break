#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import uuid

files = os.listdir("../downloader/vcodes/")
for file in files:
    if file.split('.')[-1] == 'png':
        filename = "../downloader/vcodes/" + file
        print filename
        os.system('./spliter ' + filename )
