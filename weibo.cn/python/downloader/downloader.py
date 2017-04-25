#!/usr/bin/env python
# coding:utf-8
import requests
import uuid
from PIL import Image
from bs4 import BeautifulSoup

url = "http://login.weibo.cn/login/"
for i in range(2000):
    try:
        resp = requests.get(url)
        bsObj = BeautifulSoup(resp.content, "html.parser")
        image_url = str(bsObj.img['src'])
        resp = requests.get(image_url)
        filename = str(uuid.uuid4()) + ".gif"
        with open("./captchas/" + filename, 'wb') as f:
           f.write(resp.content)

        try:
            with Image.open("./captchas/" + filename) as im:
                im.save("./captchas/" + filename.split('.gif')[0] + ".png")

        except Exception as ex:
            print(Exception, ":", ex)
        print(filename)
    except Exception as ex:
        print(Exception, ":", ex)
