#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import tensorflow as tf

from .common import IMAGE_SIZE, load_label_map, IMAGE_HEIGHT, IMAGE_WIDTH




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


def load_model_nn(alpha=5e-5):  # `cnn` up to now
    num_labels = len(load_label_map())
    with tf.Graph().as_default() as graph:
        x = tf.placeholder(tf.float32, shape=[None, IMAGE_SIZE])

        x_image = tf.reshape(x, shape=[-1, IMAGE_WIDTH, IMAGE_HEIGHT, 1])

        # First Convolutional Layer
        conv_layer1_weight = weight_variable([5, 5, 1, 32])
        conv_layer1_bias = bias_variable([32])
        pool_layer1 = max_pool_2x2(
            tf.nn.relu(
                conv2d(x_image, conv_layer1_weight) + conv_layer1_bias
            )
        )

        # Second Convolutional Layer
        conv_layer2_weight = weight_variable([5, 5, 32, 64])
        conv_layer2_bias = bias_variable([64])
        pool_layer2 = max_pool_2x2(
            tf.nn.relu(
                conv2d(pool_layer1, conv_layer2_weight) + conv_layer2_bias
            )
        )

        # Fully Connected Layer
        fc_layer_weight = weight_variable([IMAGE_HEIGHT // 4 * IMAGE_WIDTH // 4 * 64, 1024])
        fc_layer_bias = bias_variable([1024])

        pool_layer2_flat = tf.reshape(pool_layer2, [-1, IMAGE_HEIGHT // 4 * IMAGE_WIDTH // 4 * 64])
        fc_layer = tf.nn.relu(tf.matmul(pool_layer2_flat, fc_layer_weight) + fc_layer_bias)

        # Dropout
        keep_prob = tf.placeholder(tf.float32)
        fc_layer_drop = tf.nn.dropout(fc_layer, keep_prob)

        # Readout Layer
        output_layer_weight = weight_variable([1024, num_labels])
        output_layer_bias = bias_variable([num_labels])

        y_conv = tf.add(tf.matmul(fc_layer_drop, output_layer_weight),
                        output_layer_bias)

        y = tf.placeholder(tf.float32, shape=[None, num_labels])
        with tf.name_scope('loss_function'):
            loss = tf.reduce_mean(
                tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=y_conv)
            )
            tf.summary.scalar('loss_function', loss)

        optimizer = tf.train.AdamOptimizer(alpha).minimize(loss)

        correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        prediction = tf.argmax(y_conv, 1)  # for recognise
        saver = tf.train.Saver(max_to_keep=1)
        model = {'x': x,
                 'y': y,
                 'optimizer': optimizer,
                 'loss': loss,
                 'keep_prob': keep_prob,
                 'accuracy': accuracy,
                 'prediction': prediction,
                 'saver': saver,
                 'graph': graph
                 }

    return model
