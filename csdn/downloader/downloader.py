# coding:utf-8
import requests
import uuid
from PIL import Image
import os

url = "http://download.csdn.net/index.php/rest/tools/validcode/source_ip_validate/10.5711163911089325"
for i in range(100):
    resp = requests.get(url)
    filename = "./captchas/" + str(uuid.uuid4()) + ".png"
    with open(filename, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()
    im = Image.open(filename)
    if im.size != (48, 20):
        os.remove(filename)
    else:
        print filename


