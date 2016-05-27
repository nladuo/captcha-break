from PIL import Image
import os

files = os.listdir("./captchas")
for file in files:
    if file.split('.')[-1] == 'gif':
        print file
        im = Image.open("./captchas/" + file)
        im.save("./captchas/" + file.split('.gif')[0] + ".png")
        os.remove("./captchas/" + file)
