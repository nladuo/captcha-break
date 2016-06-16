#!/usr/bin/env python
#-*- coding: utf-8 -*-
from PIL import Image
import os

files = os.listdir("./captchas")
for file in files:
    if file.split('.')[-1] == 'gif':
        print file
        try:
            im = Image.open("./captchas/" + file)
            im.save("./captchas/" + file.split('.gif')[0] + ".png")
        except Exception,ex:
               print Exception,":",ex
        os.remove("./captchas/" + file)
