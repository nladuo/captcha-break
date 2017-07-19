# -*- coding:utf-8 -*-
import os
import cPickle as pickle

IMAGE_WIDTH = 100
IMAGE_HEIGHT = 40
IMAGE_SIZE = IMAGE_HEIGHT * IMAGE_WIDTH
CAPTCHA_LEN = 4
CHAR_SET_LEN = 10
NUM_LABELS = CAPTCHA_LEN * CHAR_SET_LEN




def find_model_ckpt(model_ckpt_dir=os.path.join('..', 'trainer', '.checkpoint')):
    """ Find Max Step model.ckpt """
    if not os.path.isdir(model_ckpt_dir):
        os.mkdir(model_ckpt_dir)

    from distutils.version import LooseVersion
    model_ckpt_tuple_list = []
    for fn in os.listdir(model_ckpt_dir):
        bare_fn, ext = os.path.splitext(fn)
        if bare_fn.startswith('jikexueyuan-model.ckpt') and ext == '.index':
            version = bare_fn.split('jikexueyuan-model.ckpt-')[1]
            model_ckpt_tuple_list.append((version, bare_fn))

    if len(model_ckpt_tuple_list) == 0:
        raise IOError('file like jikexueyuan-model.ckpt')
    model_ckpt_list = list(sorted(model_ckpt_tuple_list,
                                  key=lambda item: LooseVersion(item[0])))
    fn = model_ckpt_list[-1][1]
    global_step = int(model_ckpt_list[-1][0])
    path = os.path.join(model_ckpt_dir, fn)

    return path, global_step
