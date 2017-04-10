#!/usr/bin/env python
# coding:utf-8

import cPickle as pickle
from PIL import Image
import numpy as np

def check_dataset(dataset, labels, label_map, index):
    data = np.uint8(dataset[index]).reshape((32, 32))
    i = np.argwhere(labels[index] == 1)[0][0]
    im = Image.fromarray(data)
    im.show()
    print "label:", label_map[i]

if __name__ == '__main__':
    with open("save.pickle", 'rb') as f:
        save = pickle.load(f)
        train_dataset = save['train_dataset']
        train_labels = save['train_labels']
        test_dataset = save['test_dataset']
        test_labels = save['test_labels']
        label_map = save['label_map']
	
	# check if the image is corresponding to it's label
	check_dataset(train_dataset, train_labels, label_map, 0)