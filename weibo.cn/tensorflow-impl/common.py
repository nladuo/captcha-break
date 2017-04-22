# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
import os
try:
    import cpickle as pickle
except ImportError:
    import pickle

__all__ = ['IMAGE_HEIGHT', 'IMAGE_WIDTH', 'IMAGE_SIZE', 'load_label_map']

IMAGE_WIDTH = 32
IMAGE_HEIGHT = 32
IMAGE_SIZE = IMAGE_HEIGHT * IMAGE_WIDTH

def load_label_map(pickle_dir=os.curdir):
    label_map_pickle = os.path.join(pickle_dir, "label_map.pickle")

    formatted_dataset_pickle = os.path.join(pickle_dir,
                                            "formatted_dataset.pickle")

    import sys
    if os.path.exists(label_map_pickle):
        with open(label_map_pickle, 'rb') as f:
            if sys.version_info.major == 3:
                label_map = pickle.load(f, encoding='latin1')# compatiable with python2 pickle
            else:
                label_map = pickle.load(f)
    else:
        with open(formatted_dataset_pickle, 'rb') as f:
            if sys.version_info.major == 3:
                formatted_dataset = pickle.load(f, encoding='latin1')
            else:
                formatted_dataset = pickle.load(f)
            label_map = formatted_dataset['label_map']
            with open(label_map_pickle, 'wb') as f2:
                pickle.dump(label_map, f2, protocol=2)

    return label_map