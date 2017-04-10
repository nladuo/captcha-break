#!/usr/bin/env python
# coding:utf-8

import cPickle as pickle
import numpy as np
import tensorflow as tf


if __name__ == '__main__':
    print "loading save.pickle..."
    with open("save.pickle", 'rb') as f:
        save = pickle.load(f)
        train_dataset = save['train_dataset']
        train_labels = save['train_labels']
        test_dataset = save['test_dataset']
        test_labels = save['test_labels']
        label_map = save['label_map']

    image_size = 32
    num_labels = len(label_map)

    print "train_dataset:", train_dataset.shape
    print "train_labels:", train_labels.shape
    print "test_dataset:", test_dataset.shape
    print "test_labels:", test_labels.shape
    print "num_labels:", num_labels

    
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
        y_ = tf.placeholder(tf.float32, shape=[None, num_labels])

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

        cross_entropy = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))

        train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
        correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    batch_size = 128
    with tf.Session(graph=graph) as session:
        tf.global_variables_initializer().run()
        print("Initialized")

        for step in range(2001):
            offset = (step * batch_size) % (train_labels.shape[0] - batch_size)
            # Generate a minibatch.
            batch_data = train_dataset[offset:(offset + batch_size), :]
            batch_labels = train_labels[offset:(offset + batch_size), :]

            if step % 50 == 0:
                train_accuracy = accuracy.eval(feed_dict={
                    x: batch_data, y_: batch_labels, keep_prob: 1.0})
                test_accuracy = accuracy.eval(feed_dict={
                    x: test_dataset, y_: test_labels, keep_prob: 1.0})
                print("Step %d, Training accuracy: %g, Test accuracy: %g" % (step, train_accuracy, test_accuracy))

            train_step.run(feed_dict={x: batch_data, y_: batch_labels, keep_prob: 0.5})

        print("Test accuracy: %g" % accuracy.eval(feed_dict={
            x: test_dataset, y_: test_labels, keep_prob: 1.0}))

