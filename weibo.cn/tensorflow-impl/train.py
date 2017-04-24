#!/usr/bin/env python
# coding:utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import os
try:
    import cPickle as pickle
except ImportError:
    import pickle
from argparse import ArgumentParser

import tensorflow as tf

from load_model_nn import load_model_nn
from common import find_model_ckpt

formatted_dataset_path = 'formatted_dataset.pickle'
graph_log_dir = './logs'

def train(alpha=5e-5):
    print("loading %s..."%formatted_dataset_path)
    with open(formatted_dataset_path, 'rb') as f:
        import sys
        if sys.version_info.major == 3:
            save = pickle.load(f, encoding='latin1')
        else:
            save = pickle.load(f)
        train_dataset = save['train_dataset']
        train_labels = save['train_labels']
        test_dataset = save['test_dataset']
        test_labels = save['test_labels']
        label_map = save['label_map']

    num_labels = len(label_map)

    print("train_dataset:", train_dataset.shape)
    print("train_labels:", train_labels.shape)
    print("test_dataset:", test_dataset.shape)
    print("test_labels:", test_labels.shape)
    print("num_labels:", num_labels)

    model = load_model_nn()
    x = model['x']
    y = model['y']
    loss = model['loss']
    optimizer = model['optimizer']
    accuracy = model['accuracy']
    keep_prob = model['keep_prob']
    saver = model['saver']
    graph = model['graph']

    batch_size = 64
    with tf.Session(graph=graph) as session:
        merged = tf.summary.merge_all()
        writer = tf.summary.FileWriter(graph_log_dir, session.graph)
        tf.global_variables_initializer().run()


        step = 0
        try:
            model_ckpt_path, global_step = find_model_ckpt('.checkpoint') #try to continue ....
        except FileNotFoundError:
            print("Initialized")
        else: # try continue to train
            saver.restore(session, model_ckpt_path)
            step = global_step
            print('found %s, step from %d'%(model_ckpt_path, step))

        origin_step = step
        while True:
            offset = (step * batch_size) % (train_labels.shape[0] - batch_size)
            # Generate a minibatch.
            # `:` np.array op which from matlab
            batch_data = train_dataset[offset:(offset + batch_size), :]
            batch_labels = train_labels[offset:(offset + batch_size), :]
            #print(batch_data, batch_labels)
            session.run(
                [optimizer, loss],
                feed_dict={
                    x: batch_data,
                    y: batch_labels,
                    keep_prob: 0.5
                }
            )
            step += 1
            if step % 50 == 0:
                train_accuracy=session.run(
                    accuracy,
                    feed_dict={
                        x: batch_data,
                        y: batch_labels,
                        keep_prob: 1.0
                    }
                )
                test_accuracy=session.run(
                    accuracy,
                    feed_dict={
                        x: test_dataset,
                        y: test_labels,
                        keep_prob: 1.0
                    }
                )

                print(("Step %d, Training accuracy: %g, Test accuracy: %g" %
                       (step, train_accuracy, test_accuracy)))

                if test_accuracy > 0.99 or step-origin_step>4000:
                    if not os.path.isdir('.checkpoint'):
                        os.mkdir('.checkpoint')
                    save_dir = os.path.join(os.curdir, '.checkpoint')
                    save_path = saver.save(
                        session,
                        os.path.join(save_dir, 'weibo.cn-model.ckpt'),
                        global_step=step
                    )
                    print("Model saved in file: ", save_path)
                    break

        print("Test accuracy: %g" %
               session.run(
                   accuracy,
                   feed_dict={
                       x: test_dataset,
                       y: test_labels,
                       keep_prob: 1.0
                   }
               )
              )

def cli():
    parser = ArgumentParser()
    parser.add_argument('-a', '--alpha', type=float, default='5e-5',
                        help='convergence raet for train')

    kwargs = parser.parse_args().__dict__
    #print(kwargs)
    train(**kwargs)


if __name__ == '__main__':
    cli()
