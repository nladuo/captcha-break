#!/usr/bin/env python
# coding:utf-8
from __future__ import print_function

import os

import requests
import uuid
from PIL import Image
from bs4 import BeautifulSoup

url = "http://login.weibo.cn/login/"
downloader_dir = os.path.dirname(os.path.abspath(__file__))
captchas_dir = os.path.join(downloader_dir, 'captchas')
for i in range(2000):
    try:
        resp = requests.get(url)
        bsObj = BeautifulSoup(resp.content, "html.parser")
        print(resp.content.decode('gbk', errors='ignore'))
        image_url = str(bsObj.img['src'])
        resp = requests.get(image_url)
        filename = str(uuid.uuid4()) + ".gif"
        filepath = os.path.join(captchas_dir, filename)
        #print(filepath, image_url)
        with open(filepath, 'wb') as f:
           f.write(resp.content)

        try:
            with Image.open(os.path.join(captchas_dir, filename)) as im:
                im.save(filepath.split('.gif')[0] + ".png")

        except Exception as ex:
            print(Exception, ":", ex)
        print(filename)
    except Exception as ex:
        raise
        #print(Exception, ":", ex)
