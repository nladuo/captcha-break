# coding=utf-8

from __future__ import print_function
from gen.gen_captcha import gen_dataset, load_templates
import cPickle as pickle
from PIL import Image
import numpy as np
from gen.utils import vec2str


def check_dataset(dataset, labels, index):
	data = np.uint8(dataset[index]).reshape((40, 100)) * 255
	im = Image.fromarray(data)
	im.show()
	print("label:", vec2str(labels[index]))


if __name__ == '__main__':
	templates = load_templates()
	dataset, labels = gen_dataset(1, templates)  # generate one image
	check_dataset(dataset, labels, 0)

