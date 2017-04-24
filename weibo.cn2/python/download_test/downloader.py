#!/usr/bin/env python
# coding:utf-8
import requests
import uuid
from PIL import Image
import os
from bs4 import BeautifulSoup

url = "http://login.weibo.cn/login/"
for i in range(2000):
    try:
        resp = requests.get(url)
        bsObj = BeautifulSoup(resp.content, "lxml")
        image_url = str(bsObj.img['src'])
        resp = requests.get(image_url)
        filename = str(uuid.uuid4()) + ".gif"
        with open("./tests/" + filename, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
            f.close()
        im = Image.open("./tests/" + filename)
        try:
            im = Image.open("./tests/" + filename)
            im.save("./tests/" + filename.split('.gif')[0] + ".png")
        except Exception, ex:
            print Exception, ":", ex
        os.remove("./tests/" + filename)
        print filename
    except Exception, ex:
        print Exception, ":", ex
