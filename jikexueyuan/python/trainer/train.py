# coding=utf-8

from __future__ import print_function
from gen.gen_captcha import gen_dataset, load_templates
from model.nn import load_model_nn
from model.common import find_model_ckpt
import os
import tensorflow as tf

trainer_dir = os.path.dirname(os.path.abspath(__file__))
home_dir = os.path.dirname(trainer_dir)
graph_log_dir = os.path.join(trainer_dir, 'logs')


def train():
    templates = load_templates()

    model = load_model_nn()
    x = model["x"]
    y = model['y']
    loss = model['loss']
    optimizer = model['optimizer']
    accuracy = model['accuracy']
    keep_prob = model['keep_prob']
    saver = model['saver']
    graph = model['graph']

    save_dir = os.path.join(".", '.checkpoint')
    print("Model saved path: ", save_dir)

    def save_model(_step):
        saver.save(
            session,
            os.path.join(save_dir, 'jikexueyuan-model.ckpt'),
            global_step=_step
        )

    with tf.Session(graph=graph) as session:
        merged = tf.summary.merge_all()
        writer = tf.summary.FileWriter(graph_log_dir, session.graph)
        tf.global_variables_initializer().run()

        step = 0
        try:
            model_ckpt_path, global_step = find_model_ckpt()  # try to continue ....
        except IOError:
            print("Initialized")
        else:  # try continue to train
            saver.restore(session, model_ckpt_path)
            step = global_step
            print('found %s, step from %d' % (model_ckpt_path, step))

        while True:
            batch_data, batch_labels = gen_dataset(64, templates)

            _, l = session.run(
                [optimizer, loss],
                feed_dict={
                    x: batch_data,
                    y: batch_labels,
                    keep_prob: 0.75
                }
            )
            step += 1
            print(("Step: %d, Loss: %4f" % (step, l)))
            if step % 50 == 0:
                test_dataset, test_labels = gen_dataset(100, templates)
                test_accuracy = session.run(
                    accuracy,
                    feed_dict={
                        x: test_dataset,
                        y: test_labels,
                        keep_prob: 1.0
                    }
                )

                print(("Step: %d, Test Accuracy: %s" % (step, test_accuracy)))

                save_model(step)  # save the model every 50 step

                if test_accuracy >= 0.92 or step >= 10000:  # stop when accuracy above 92%
                    save_model(step)
                    break

        print("Test accuracy: %g" %
              session.run(
                  accuracy,
                  feed_dict={
                      x: test_dataset,
                      y: test_labels,
                      keep_prob: 1.0
                  })
              )


if __name__ == "__main__":
    train()
