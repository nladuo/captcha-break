# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""

"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division


import os

import cv2
import numpy as np

from captcha_utils import CaptchaUtils

__all__ = ["Spliter"]

class Spliter:

    HEIGHT_STANDRAD = 32
    WIDTH_STANDARD = 32
    def __init__(self, save_dir):
        self.save_dir = save_dir
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)

    def split_letters(self, path):
        letters = [0]*4

        bare_name, ext = os.path.splitext(path)
        if ext == '.gif':
            from PIL import Image
            with Image.open(path) as im:
                path = bare_name+'.png'
                im.save(path)

        image = cv2.imread(path, cv2.IMREAD_COLOR)
        #cv2.imshow("init", image)

        image = self.clear_noise(image)
        splits = [0]*8
        CaptchaUtils.vertical_project(image, splits)
        if splits[7] < image.shape[1]:#assume the final split is in the range of image.
            for i in range(0, 8, 2):
                letters[i//2] = image[0:image.shape[0], splits[i]:splits[i+1],].copy()

        return letters

    def split_and_save(self, filename):

        letters = self.split_letters(filename)
        for (i, every_letter) in enumerate(letters):
            every_letter = self.format_splited_image(every_letter)
            self._save_image(every_letter, i)

    def clear_noise(self, image):
        image = cv2.flip(image, -1,)
        clear_horizontal_noise_line(image)
        image = cv2.flip(image, -1, )
        clear_horizontal_noise_line(image)
        clear_color(image)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)[1]
        CaptchaUtils.clear_peper_noise(image, 2)

        return image

    def format_splited_image(self, splited_image):
        if splited_image.shape[1] > Spliter.WIDTH_STANDARD: return
        if splited_image.shape[0] <=0 or splited_image.shape[1] <= 0: return

        out_width = Spliter.WIDTH_STANDARD
        out_height = Spliter.HEIGHT_STANDRAD

        offset_x = abs(out_width - splited_image.shape[1]) / 2
        offset_y = abs(out_height - splited_image.shape[0]) / 2

        TransMat = np.float32([[1,0,offset_x],
                             [0,1,offset_y]])

        # print(TransMat)
        new_image = cv2.warpAffine(splited_image, TransMat,
                                   (out_height, out_width)[::-1],
                                   borderValue=255)#reversed
        return new_image

    def _save_image(self, formatted_image, i):
        path = os.path.join(self.save_dir, str(i))+'.png'
        cv2.imwrite(path, formatted_image)


def is_black(i, j, image):
    b = image[j, i][0]
    g = image[j, i][1]
    r = image[j, i][2]
    average = (int(r) + int(g) + int(b))/3
    if r < 244 and abs(average-b)<4 and abs(average-g)<4 and abs(average-r)<4:
        return True
    return False

def clear_color(image):
    for i in range(image.shape[1]):
        for j in range(image.shape[0]):
            if is_black(i, j, image):
                image[j][i][0]=20
                image[j][i][1]=20
                image[j][i][2]=20

def get_horizontal_noise_line_width(image, now_height, now_width):
    end_width = now_width
    while end_width < image.shape[1] \
        and image[now_height][now_width][0] < 12 \
        and image[now_height][now_width][1] < 12 \
        and image[now_height][now_width][2] < 12 :

        end_width += 1

    return end_width - now_width

def clear_horizontal_noise_line(image):
    first_height = 0
    has_find = False
    for i in range(image.shape[0]):
        if image[i][0][0] < 12 and image[i][0][1] < 12 and image[i][0][2] < 12 \
                and get_horizontal_noise_line_width(image, i, 0) >= 2:
            first_height = i
            has_find = True

    if not has_find: return
    now_width = 0
    now_height = first_height-2
    while now_width < image.shape[1]:
        #print((now_height, now_width), image.shape)
        width = get_horizontal_noise_line_width(image, now_height, now_width)

        #clear the horizontal noise line
        for i in range(now_width, now_width+width-1):
            top_num = 0
            bottom_num = 0
            #the upper pixel
            if is_black(i, now_height-1, image): top_num += 1
            #the upper left pixel
            if is_black(i-1, now_height-1, image): top_num += 1
            #the upper right pixel
            if is_black(i+1, now_height-1, image): top_num += 1
            #the lower pixel
            if is_black(i, now_height+1, image): bottom_num += 1
            #the left lower pixel
            if is_black(i-1, now_height+1, image): bottom_num += 1
            # the right lower pixel
            if is_black(i+1, now_height+1, image): bottom_num += 1

            if now_height != 0 and now_height != image.shape[0]:
                if top_num>0 and bottom_num>0: continue

            image[now_height][i][0] = 255
            image[now_height][i][1] = 255
            image[now_height][i][2] = 255

        # find the next noise pixel
        a = get_horizontal_noise_line_width(image, now_height - 1, now_width + width -1)
        b = get_horizontal_noise_line_width(image, now_height + 1, now_width + width -1)
        c = get_horizontal_noise_line_width(image, now_height - 1, now_width + width)
        d = get_horizontal_noise_line_width(image, now_height + 1, now_width + width)
        if now_height == 0:
            a=0
            c=0

        if now_height == (image.shape[0] - 1):
            b=0
            d=0

        max_a_b = max(a, b)
        max_c_d = max(c, d)
        max_a_b_c_d = max(max_a_b, max_c_d)
        if max_a_b_c_d < 2: break
        if max_a_b == max_a_b_c_d:
            now_width += width-1
            if max_a_b == a:
                now_height -= 1
            else:
                now_height += 1

        else:
            now_width += width
            if max_c_d == c:
                now_height -= 1
            else:
                now_height += 1
