from PIL import Image
import os
from img_process import rotate_and_cut
import random
import math
from utils import str2vec
import numpy as np


def load_templates():
    """ load the letter template from ./templates """
    templates = []
    for i in range(10):
        image_path = os.path.join(".", "templates", "%d.png" % i)
        templates.append(Image.open(image_path).convert("L"))
    return templates


def create_captcha(templates):

    captcha = Image.new('RGBA', (100, 40), (255, 255, 255, 0))
    captcha_str = ""
    for i in range(4):
        number = random.randint(0, 9)
        captcha_str += str(number)
        template = templates[number]
        template = rotate_and_cut(template, random.randint(-45, 45))
        width_range = math.fabs(25 - template.size[0])
        height_range = math.fabs(40 - template.size[1])

        start_x_pos = i * 25 + random.randint(-width_range-5, width_range+5)
        start_y_pos = random.randint(0, height_range)

        captcha.paste(template, (start_x_pos, start_y_pos), mask=template)
    return captcha, captcha_str


def gen_dataset(num, templates):
    # print("generating %d dataset..." % num)
    dataset = []
    labels = []
    for _ in range(num):
        captcha, captcha_str = create_captcha(templates)
        dataset.append(np.asarray(captcha.convert("L")).reshape([40 * 100]) / 255)
        labels.append(str2vec(captcha_str))

    return np.array(dataset), np.array(labels)
