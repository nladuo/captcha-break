# -*- coding:utf-8 -*-

from __future__ import print_function
from __future__ import division

import tensorflow as tf

from common import IMAGE_HEIGHT, IMAGE_SIZE, IMAGE_WIDTH, CAPTCHA_LEN, CHAR_SET_LEN, NUM_LABELS


def weight_variable(shape):
    initial = tf.random_normal(shape, stddev=0.01)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.random_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                          strides=[1, 2, 2, 1], padding='SAME')


def load_model_nn(alpha=1e-3):  # `cnn` up to now
    with tf.Graph().as_default() as graph:
        # Define the PlaceHolder
        x = tf.placeholder(tf.float32, shape=[None, IMAGE_SIZE])
        y = tf.placeholder(tf.float32, shape=[None, NUM_LABELS])
        keep_prob = tf.placeholder(tf.float32)

        x_image = tf.reshape(x, shape=[-1, IMAGE_WIDTH, IMAGE_HEIGHT, 1])

        # First Convolutional Layer, input@(100, 40), output@(50, 20)
        conv_layer1_weight = weight_variable([5, 5, 1, 32])
        conv_layer1_bias = bias_variable([32])
        pool_layer1 = max_pool(
            tf.nn.relu(
                conv2d(x_image, conv_layer1_weight) + conv_layer1_bias
            )
        )

        # Second Convolutional Layer, input@(50, 20), output@(25, 10)
        conv_layer2_weight = weight_variable([5, 5, 32, 64])
        conv_layer2_bias = bias_variable([64])
        pool_layer2 = max_pool(
            tf.nn.relu(
                conv2d(pool_layer1, conv_layer2_weight) + conv_layer2_bias
            )
        )

        # Third Convolutional Layer, input@(25, 10), output@(13, 5)
        conv_layer3_weight = weight_variable([5, 5, 64, 64])
        conv_layer3_bias = bias_variable([64])
        pool_layer3 = max_pool(
            tf.nn.relu(
                conv2d(pool_layer2, conv_layer3_weight) + conv_layer3_bias
            )
        )

        # Fully Connected Layer
        fc_layer_weight = weight_variable([13 * 5 * 64, 1024])
        fc_layer_bias = bias_variable([1024])

        pool_layer3_flat = tf.reshape(pool_layer3, [-1, 13 * 5 * 64])
        fc_layer = tf.nn.relu(tf.add(tf.matmul(pool_layer3_flat, fc_layer_weight), fc_layer_bias))

        # Dropout
        fc_layer_drop = tf.nn.dropout(fc_layer, keep_prob)

        # Readout Layer
        output_layer_weight = weight_variable([1024, NUM_LABELS])
        output_layer_bias = bias_variable([NUM_LABELS])

        y_conv = tf.add(tf.matmul(fc_layer_drop, output_layer_weight), output_layer_bias)
        
        loss = tf.reduce_mean(
            tf.nn.sigmoid_cross_entropy_with_logits(labels=y, logits=y_conv)
        )

        optimizer = tf.train.AdamOptimizer(alpha).minimize(loss)

        prediction = tf.argmax(tf.reshape(y_conv, [-1, CAPTCHA_LEN, CHAR_SET_LEN]), 2)
        correct = tf.argmax(tf.reshape(y, [-1, CAPTCHA_LEN, CHAR_SET_LEN]), 2)
        correct_prediction = tf.equal(prediction, correct)
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


        saver = tf.train.Saver(max_to_keep=2)
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
