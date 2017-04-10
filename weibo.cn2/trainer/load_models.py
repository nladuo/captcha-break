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

    base_dir = "../generate_dataset/dataset/"
    labels = os.listdir(base_dir)

    for index, label in enumerate(labels):
        print "loading:", label, "index:", index
        try:
            image_files = os.listdir(base_dir + label)
            for image_file in image_files:
                image_path = base_dir + label + "/" + image_file
                im = Image.open(image_path).convert('L')
                dataset.append(np.asarray(im, dtype=np.float32))
                labelset.append(index)
            label_map[index] = label
        except: pass

    return np.array(dataset), np.array(labelset), label_map


def randomize(dataset, labels):
    permutation = np.random.permutation(labels.shape[0])
    shuffled_dataset = dataset[permutation, :, :]
    shuffled_labels = labels[permutation]
    return shuffled_dataset, shuffled_labels


if __name__ == '__main__':
    dataset, labelset, label_map = load_dataset()
    print "randomizing the dataset..."
    dataset, labelset = randomize(dataset, labelset)

    print "train_test_split the dataset..."
    train_dataset, test_dataset, train_labels, test_labels = train_test_split(dataset, labelset)

    print "pickling the label_map..."
    f = open("label_map.pickle", 'wb')
    pickle.dump(label_map, f)
    f.close()
    print "label_map has saved at label_map.pickle"

    print "pickling the dataset..."
    save = {
        'train_dataset': train_dataset,
        'train_labels': train_labels,
        'test_dataset': test_dataset,
        'test_labels': test_labels,
    }
    f = open("dataset.pickle", 'wb')
    pickle.dump(save, f)
    f.close()

    print "dataset has saved at dataset.pickle"
    print "load_model has finished"
