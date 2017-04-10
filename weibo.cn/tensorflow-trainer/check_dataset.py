#!/usr/bin/env python
# coding:utf-8

import cPickle as pickle
from PIL import Image
import numpy as np

def check_dataset(dataset, labels, label_map, index):
    im = Image.fromarray(np.uint8(dataset[index]))
    print label_map[labels[index]]
    im.show()

if __name__ == '__main__':
    with open("save.pickle", 'rb') as f:
        save = pickle.load(f)
        train_dataset = save['train_dataset']
        train_labels = save['train_labels']
        test_dataset = save['test_dataset']
        test_labels = save['test_labels']
        label_map = save['label_map']
	
	# check if the image is correspond to it's label
	check_dataset(train_dataset, train_labels, label_map, 0)