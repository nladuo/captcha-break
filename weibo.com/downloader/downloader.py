# coding:utf-8
import requests
import uuid
import os

url = "http://login.sina.com.cn/cgi/pin.php?r=8787878&s=0"
for i in range(10000):
    resp = requests.get(url)
    filename = "./captchas/" + str(uuid.uuid4()) + ".png"
    with open(filename, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()
    print filename
