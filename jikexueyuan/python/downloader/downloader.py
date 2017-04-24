# coding:utf-8
import requests
import uuid
from PIL import Image
import os

image_url = "http://passport.jikexueyuan.com/sso/verify"
for i in range(8000):
    try:
        resp = requests.get(image_url)
        filename = str(uuid.uuid4()) + ".gif"
        with open("./captchas/" + filename, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
            f.close()
        im = Image.open("./captchas/" + filename)
        try:
            im = Image.open("./captchas/" + filename)
            im.save("./captchas/" + filename.split('.gif')[0] + ".png")
        except Exception, ex:
            print Exception, ":", ex
        os.remove("./captchas/" + filename)
        print filename
    except Exception, ex:
        print Exception, ":", ex
