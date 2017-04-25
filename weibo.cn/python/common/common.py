#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
try:
    import cPickle as pickle
except ImportError:
    import pickle

__all__ = ['IMAGE_HEIGHT', 'IMAGE_WIDTH', 'IMAGE_SIZE', 'load_label_map']

IMAGE_WIDTH = 32
IMAGE_HEIGHT = 32
IMAGE_SIZE = IMAGE_HEIGHT * IMAGE_WIDTH

try:
    FileNotFoundError
except NameError:
    # py2
    FileNotFoundError = IOError

home_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
trainer_dir = os.path.join(home_dir, 'trainer')
def load_label_map(pickle_dir=trainer_dir):
    label_map_pickle = os.path.join(pickle_dir, "label_map.pickle")

    formatted_dataset_pickle = os.path.join(pickle_dir,
                                            "formatted_dataset.pickle")

    import sys
    if os.path.exists(label_map_pickle):
        with open(label_map_pickle, 'rb') as f:
            if sys.version_info.major == 3:
                label_map = pickle.load(f, encoding='latin1')  # compatiable with python2 pickle
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


def find_model_ckpt(model_ckpt_dir=os.path.join(trainer_dir, '.checkpoint')):
    """ Find Max Step model.ckpt """
    if not os.path.isdir(model_ckpt_dir):
        os.mkdir(model_ckpt_dir)

    from distutils.version import LooseVersion
    model_ckpt_tuple_list = []
    for fn in os.listdir(model_ckpt_dir):
        bare_fn, ext = os.path.splitext(fn)
        if bare_fn.startswith('weibo.cn-model.ckpt') and ext == '.index':
            version = bare_fn.split('weibo.cn-model.ckpt-')[1]
            model_ckpt_tuple_list.append((version, bare_fn))

    if len(model_ckpt_tuple_list) == 0:
        raise FileNotFoundError('file like weibo.cn-model.ckpt')
    model_ckpt_list = list(sorted(model_ckpt_tuple_list,
                                  key=lambda item: LooseVersion(item[0])))
    fn = model_ckpt_list[-1][1]
    global_step = int(model_ckpt_list[-1][0])
    path = os.path.join(model_ckpt_dir, fn)

    return path, global_step