#!/usr/bin/env python
# coding:utf-8
from __future__ import absolute_import
from __future__ import print_function

import os
try:
    import cPickle as pickle
except ImportError:
    import pickle

import numpy as np

trainer_dir =os.path.dirname(os.path.abspath(__file__))
def check_dataset(dataset, labels, label_map, index):
    data = np.uint8(dataset[index]).reshape((32, 32))
    i = np.argwhere(labels[index] == 1)[0][0]
    import matplotlib.pyplot as plt  # im.show may not be implemented
                                     #  in opencv-python on Tk GUI (such as Linux)
    import pylab
    plt.ion()
    plt.imshow(data)
    pylab.waitforbuttonpress(timeout=5)
    print("label:", label_map[i])

if __name__ == '__main__':
    with open(os.path.join(trainer_dir,"formatted_dataset.pickle"), 'rb') as f:
        import sys
        if sys.version_info.major == 3:
            db = pickle.load(f, encoding='latin1')
        else:
            db = pickle.load(f)
        train_dataset = db['train_dataset']
        train_labels = db['train_labels']
        test_dataset = db['test_dataset']
        test_labels = db['test_labels']
        label_map = db['label_map']

    # check if the image is corresponding to it's label
    check_dataset(train_dataset, train_labels, label_map, 0)
