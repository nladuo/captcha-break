#!/usr/bin/env python
import numpy as np
import os
from sklearn.model_selection import train_test_split
from PIL import Image
import cPickle as pickle


def load_dataset():
    dataset = []
    labelset = []
    label_map = {}

    base_dir = "../trainer/training_set/"
    labels = os.listdir(base_dir)
    index = 0
    for label in labels:
        if label == "ERROR" or label == ".DS_Store": 
            continue
        print "loading:", label, "index:", index
        try:
            image_files = os.listdir(base_dir + label)
            for image_file in image_files:
                image_path = base_dir + label + "/" + image_file
                im = Image.open(image_path).convert('L')
                dataset.append(np.asarray(im, dtype=np.float32))
                labelset.append(index)
            label_map[index] = label
            index += 1
        except: pass

    return np.array(dataset), np.array(labelset), label_map


def randomize(dataset, labels):
    permutation = np.random.permutation(labels.shape[0])
    shuffled_dataset = dataset[permutation, :, :]
    shuffled_labels = labels[permutation]
    return shuffled_dataset, shuffled_labels


def reformat(dataset, labels, image_size, num_labels):
    dataset = dataset.reshape((-1, image_size * image_size)).astype(np.float32)
    # Map 1 to [0.0, 1.0, 0.0 ...], 2 to [0.0, 0.0, 1.0 ...]
    labels = (np.arange(num_labels) == labels[:, None]).astype(np.float32)
    return dataset, labels


if __name__ == '__main__':
    dataset, labelset, label_map = load_dataset()
    print "randomizing the dataset..."
    dataset, labelset = randomize(dataset, labelset)

    print "train_test_split the dataset..."
    train_dataset, test_dataset, train_labels, test_labels = train_test_split(dataset, labelset)

    print "reformating the dataset..."
    train_dataset, train_labels = reformat(train_dataset, train_labels, 32, len(label_map))
    test_dataset, test_labels = reformat(test_dataset, test_labels, 32, len(label_map))
    print "train_dataset:", train_dataset.shape
    print "train_labels:", train_labels.shape
    print "test_dataset:", test_dataset.shape
    print "test_labels:", test_labels.shape

    print "pickling the dataset..."
    save = {
        'train_dataset': train_dataset,
        'train_labels': train_labels,
        'test_dataset': test_dataset,
        'test_labels': test_labels,
        'label_map': label_map
    }
    with open("save.pickle", 'wb') as f:
        pickle.dump(save, f)

    print "dataset has saved at save.pickle"
    print "load_model has finished"
