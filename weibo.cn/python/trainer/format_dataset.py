#!/usr/bin/env python
# coding:utf-8
from __future__ import print_function
from __future__ import division

import os
import sys
import io
try:
    import cPickle as pickle
except ImportError:
    import pickle

from sklearn.model_selection import train_test_split
import numpy as np
from PIL import Image

trainer_dir =os.path.dirname(os.path.abspath(__file__))
home_dir= os.path.dirname(trainer_dir)
sys.path.append(home_dir)
from common.common import IMAGE_SIZE


def load_dataset():
    dataset = []
    labelset = []
    label_map = {}

    base_dir = os.path.join(trainer_dir, "training_set")
    labels = os.listdir(base_dir)
    index = 0
    for label in labels:
        if label == "ERROR" or label == ".DS_Store":
            continue
        print("loading:", label, "index:", index)
        try:
            image_files = os.listdir(os.path.join(base_dir, label))
            for image_file in image_files:
                image_path = os.path.join(base_dir, label, image_file)
                im = Image.open(image_path).convert('L')
                dataset.append(np.asarray(im, dtype=np.float32))
                # im = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                # dataset.append(im)
                labelset.append(index)
            label_map[index] = label
            index += 1
        except:
            raise

    return np.array(dataset), np.array(labelset), label_map


def randomize(dataset, labels):
    permutation = np.random.permutation(labels.shape[0])
    shuffled_dataset = dataset[permutation, :, :]
    shuffled_labels = labels[permutation]
    return shuffled_dataset, shuffled_labels


def _format_dataset(dataset, labels, image_size, num_labels):
    dataset = dataset.reshape((-1, image_size)).astype(np.float32)
    # Map 1 to [0.0, 1.0, 0.0 ...], 2 to [0.0, 0.0, 1.0 ...]
    labels = (np.arange(num_labels) == labels[:, None]).astype(np.float32)
    return dataset, labels

DEFAULT_FORMATTED_DATATSET_PATH = os.path.join(trainer_dir, 'formatted_dataset.pickle')

def format_dataset(formatted_dataset_path=DEFAULT_FORMATTED_DATATSET_PATH,
                   log_file=io.StringIO()):

    dataset, labelset, label_map = load_dataset()
    print("randomizing the dataset...", file=log_file)
    dataset, labelset = randomize(dataset, labelset)

    print("train_test_split the dataset...", file=log_file)
    train_dataset, test_dataset, train_labels, test_labels = train_test_split(dataset, labelset)

    print("reformating the dataset...", file=log_file)
    train_dataset, train_labels = _format_dataset(train_dataset, train_labels, IMAGE_SIZE, len(label_map))
    test_dataset, test_labels = _format_dataset(test_dataset, test_labels, IMAGE_SIZE, len(label_map))
    print("train_dataset:", train_dataset.shape, file=log_file)
    print("train_labels:", train_labels.shape, file=log_file)
    print("test_dataset:", test_dataset.shape, file=log_file)
    print("test_labels:", test_labels.shape, file=log_file)

    print("pickling the dataset...", file=log_file)

    formatted_dataset = {
        'train_dataset': train_dataset,
        'train_labels': train_labels,
        'test_dataset': test_dataset,
        'test_labels': test_labels,
        'label_map': label_map
    }

    with open(formatted_dataset_path, 'wb') as f:
        pickle.dump(formatted_dataset, f, protocol=2) # for compatible with python27

    print("dataset has saved at %s"%formatted_dataset_path, file=log_file)
    print("load_model has finished", file=log_file)


def cli():
    import sys
    if len(sys.argv) > 1:
        formatted_dataset_path = sys.argv[1]
        format_dataset(formatted_dataset_path, sys.stdout)
    else:
        format_dataset(log_file=sys.stdout)

if __name__ == '__main__':
    cli()
