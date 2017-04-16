#!/usr/bin/env python
# coding:utf-8

import os
from PIL import Image, ImageFont, ImageDraw
import uuid
import sys
import random

reload(sys)
sys.setdefaultencoding('utf8')


def generate_data(ch, rotate_angle, save_path):
    im = Image.new("RGBA", (28, 28), (255, 255, 255, 0))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype("华文楷体.ttf", 21)

    dr.text((3, 3), ch, font=font, fill="#000000")

    # add salt noise
    for i in range(10):
        dr.point((random.randint(0, 24), random.randint(0, 24)), fill="#000000")

    # rotate the image
    im = im.rotate(rotate_angle)
    result = Image.new("RGB", (28, 28), (255, 255, 255))
    result.paste(im, (0, 0), mask=im)
    filename = save_path + "/" + str(uuid.uuid4()) + ".png"

    result.save(filename)


if __name__ == "__main__":
    f = open("chars.txt", "r")
    chars = unicode(f.read())
    print "num_labels:", len(chars)

    for i, ch in enumerate(chars):
        if i > 20:
            break
        save_path = "./dataset/" + str(ch)
        print "generating:", save_path
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        # generate 360 sample for every character
        for i in range(-30, 30, 1):
            for j in range(6):
                generate_data(ch, i, save_path)

    print "finished."
