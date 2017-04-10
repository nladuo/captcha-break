#!/usr/bin/env python
# coding:utf-8
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt

im = Image.open('test2.png').convert('RGB')
# im.show()
im.show()

pixels = im.load()

# print im.size
#
# print im.getpixel((1, 1))

data = {}
for x in xrange(im.size[0]):
    for y in xrange(im.size[1]):
        variance = np.var(pixels[x, y])
        if variance in data:
            data[variance] += 1
        else:
            data[variance] = 1
        if np.var(pixels[x, y]) > 200:
            pixels[x, y] = (255, 255, 255)
im.show()

x = []
y  = []
for k in data:
    x.append(k)
    y.append(data[k])



plt.scatter(x,y,marker='o')
plt.show()


#         if np.var(pixels[x, y]) > 200:
#             pixels[x, y] = (255, 255, 255)
#
#
#
#
# # show_histogram2d(im)
# # im = img_threshold(im, 150)
# im.show()
#


