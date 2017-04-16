#!/usr/bin/env python
# coding:utf-8

from __future__ import print_function
import cPickle as pickle
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import sys


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: ./recoginze.py [image_path]")
        exit(-1)

    if not os.path.exists(sys.argv[1]):
        print(sys.argv[1], "is not exists.")
        exit(-1)

    image_size = 32
    im = Image.open(sys.argv[1]).convert('L')
    input_image = np.asarray(im, dtype=np.float32)
    input_image = input_image.reshape(image_size * image_size).astype(np.float32)

    if os.path.exists("label_map.pickle"):
        with open("label_map.pickle", 'rb') as f:
            label_map = pickle.load(f)
    else:
        with open("save.pickle", 'rb') as f:
            save = pickle.load(f)
            label_map = save['label_map']
            with open("label_map.pickle", 'wb') as f2:
                pickle.dump(label_map, f2)

    num_labels = len(label_map)


    def weight_variable(shape):
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial)


    def bias_variable(shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)


    def conv2d(x, W):
        return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


    def max_pool_2x2(x):
        return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                              strides=[1, 2, 2, 1], padding='SAME')


    graph = tf.Graph()
    with graph.as_default():
        x = tf.placeholder(tf.float32, shape=[None, image_size * image_size])
        # y_ = tf.placeholder(tf.float32, shape=[None, num_labels])

        x_image = tf.reshape(x, [-1, image_size, image_size, 1])

        # First Convolutional Layer
        W_conv1 = weight_variable([5, 5, 1, 32])
        b_conv1 = bias_variable([32])

        h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
        h_pool1 = max_pool_2x2(h_conv1)

        # Second Convolutional Layer
        W_conv2 = weight_variable([5, 5, 32, 64])
        b_conv2 = bias_variable([64])

        h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
        h_pool2 = max_pool_2x2(h_conv2)

        # Densely Connected Layer
        W_fc1 = weight_variable([image_size / 4 * image_size / 4 * 64, 1024])
        b_fc1 = bias_variable([1024])

        h_pool2_flat = tf.reshape(h_pool2, [-1, image_size / 4 * image_size / 4 * 64])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

        # Dropout
        keep_prob = tf.placeholder(tf.float32)
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

        # Readout Layer
        W_fc2 = weight_variable([1024, num_labels])
        b_fc2 = bias_variable([num_labels])

        y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

        prediction = tf.argmax(y_conv, 1)

        saver = tf.train.Saver()

    batch_size = 128
    with tf.Session(graph=graph) as session:
        tf.global_variables_initializer().run()
        saver.restore(session, "./weibo.cn-model.ckpt")

        label = prediction.eval(feed_dict={x: [input_image], keep_prob: 1.0}, session=session)[0]
        print(label_map[label], end="")
