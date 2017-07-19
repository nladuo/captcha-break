# coding=utf-8

from __future__ import print_function
from gen.gen_captcha import gen_dataset, load_templates
from model.nn import load_model_nn
from model.common import find_model_ckpt
import os
import tensorflow as tf
from gen.utils import vec2str
import numpy as np
from PIL import Image

trainer_dir = os.path.dirname(os.path.abspath(__file__))
home_dir = os.path.dirname(trainer_dir)
graph_log_dir = os.path.join(trainer_dir, 'logs')


def show_im(dataset):
    data = np.uint8(dataset[0]).reshape((40, 100)) * 255
    im = Image.fromarray(data)
    im.show()

def test_model():
    templates = load_templates()

    model = load_model_nn()
    x = model['x']
    keep_prob = model['keep_prob']
    saver = model['saver']
    prediction = model['prediction']
    graph = model['graph']
    model_ckpt_path, _ = find_model_ckpt()
    print("Used the model:", model_ckpt_path)


    with tf.Session(graph=graph) as session:
        tf.global_variables_initializer().run()
        saver.restore(session, model_ckpt_path)

        dataset, labels = gen_dataset(1, templates)  # generate one image

        label = prediction.eval(feed_dict={x: dataset, keep_prob: 1.0}, session=session)[0]
        print("predict label:", label)
        show_im(dataset)
        print("actual label:", vec2str(labels[0]))


if __name__ == "__main__":
    test_model()
