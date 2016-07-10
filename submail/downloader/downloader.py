# coding:utf-8
import requests
import uuid
import os

url = "http://submail.cn/sms/codeImg"
for i in range(100):
    resp = requests.get(url)
    filename = "./captchas/" + str(uuid.uuid4()) + ".png"
    with open(filename, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()
    print filename


