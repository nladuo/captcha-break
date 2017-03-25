#!/usr/bin/env python
# coding:utf-8

import os
import Image, ImageFont, ImageDraw
import uuid
import sys
import random

reload(sys)
sys.setdefaultencoding('utf8')


def generate_data(ch, rotate_angle, save_path):
    im = Image.new("RGBA", (24, 24), (255, 255, 255, 0))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype("华文楷体.ttf", 21)

    dr.text((1, 0), ch, font=font, fill="#000000")

    # add peper noise
    for i in range(10):
        dr.point((random.randint(0, 24), random.randint(0, 24)), fill="#000000")

    im = im.rotate(rotate_angle)

    result = Image.new("RGB", (24, 24), (255, 255, 255))
    result.paste(im, (0, 0), mask=im)
    filename = save_path + "/" +str(uuid.uuid4()) + ".png"

    result.save(filename)


f = open("chars.txt", "r")
chars = unicode(f.read())
for ch in chars:
    save_path = "./dataset/" + str(ch)
    print save_path
    if ~os.path.exists(save_path):
        os.mkdir(save_path)
    for i in range(-15, 15, 3):
        generate_data(ch, i, save_path)
        generate_data(ch, i, save_path)
        generate_data(ch, i, save_path)
