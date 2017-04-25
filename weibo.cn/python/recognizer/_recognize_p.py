#!/usr/bin/env python
# coding:utf-8
from __future__ import print_function

import os
import sys
from subprocess import Popen, PIPE
try:
    import cpickle as pickle
except ImportError:
    import pickle

import tensorflow as tf
import numpy as np
import cv2

home_dir= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(home_dir)
from common.common import load_label_map, find_model_ckpt, IMAGE_SIZE
from common.load_model_nn import load_model_nn
from spliter.spliter import Spliter

image_size = IMAGE_SIZE
if sys.version_info.major == 2:
    input = raw_input

def recognize_char_p():
    label_map = load_label_map()
    model = load_model_nn()

    x = model['x']
    keep_prob = model['keep_prob']
    saver = model['saver']
    prediction = model['prediction']
    graph = model['graph']
    model_ckpt_path, _ = find_model_ckpt()
    # print('load check-point %s'%model_ckpt_path, file=sys.stderr)
    with tf.Session(graph=graph) as session:
        tf.global_variables_initializer().run()
        saver.restore(session, model_ckpt_path)

        while True:
            sys.stdout.flush()
            captcha_path = input().strip()
            if captcha_path == '$exit':  # for close session
                break
            im = np.reshape(cv2.imread(captcha_path, cv2.IMREAD_GRAYSCALE), IMAGE_SIZE)
            label = prediction.eval(feed_dict={x: [im], keep_prob: 1.0}, session=session)[0]
            sys.stdout.write(label_map[label])
            sys.stdout.write('\n')


def recognize_p():
    """ 
    captcha_path
    $exit to exit
    """
    # print("recognize_p")

    label_map = load_label_map()
    model = load_model_nn()

    x = model['x']
    keep_prob = model['keep_prob']
    saver = model['saver']
    prediction = model['prediction']
    graph = model['graph']
    model_ckpt_path, _ = find_model_ckpt()
    print('load check-point %s' % model_ckpt_path, file=sys.stderr)
    with tf.Session(graph=graph) as session:
        tf.global_variables_initializer().run()
        saver.restore(session, model_ckpt_path)

        while True:
            sys.stdout.flush()
            captcha_path = input().strip()
            # print("_recoginze", captcha_path)
            if captcha_path == '$exit':  # for close session
                break

            spliter = Spliter(os.curdir)

            try:
                letters = spliter.split_letters(captcha_path)
                formatted_letters = map(spliter.format_splited_image,letters)
                formatted_letters = [letter.reshape(image_size) for letter in formatted_letters]
            except Exception as ex:
                sys.stdout.write('\n')
                continue

            result = []
            for letter in formatted_letters:
                label = prediction.eval(feed_dict={x: [letter], keep_prob: 1.0}, session=session)[0]
                result.append(label_map[label])
                sys.stdout.write(label_map[label])

            sys.stdout.write('\n')

# start a recognize daemon process
# for interactive in IPython
# p.send('test.gif')
# p.recv()
# p.close()


def send(self, msg):
    """Interactive Tools
    self: subprocess.Popen
    p.send('abc.png')
    send(p, 'abc.png')
    
    _read_time: in case of block forever for no SIGALARM on Windows 555
    """
    if sys.version_info.major == 2:
        Str = unicode
    else:
        Str = str

    if isinstance(msg, Str):
        msg = msg.encode('utf8')

    try:
        self.stdin.write(msg+b'\n')
        self.stdin.flush()
    except OSError:
        raise IOError('this process halted')

    _read_time = getattr(self, '_read_time', 0)
    if _read_time > 100:
        raise BufferError('Warning: may no have enough space in buffer')

    setattr(self, '_read_time', _read_time+1)


def recv(self, readall=False):
    """return str/unicode"""

    _read_time = getattr(self, '_read_time', 0)
    if _read_time == 0:
        raise IOError('you should send a value before recv')

    if readall:
        msg_list = []
        for i in range(_read_time):
            msg_list.append(self.stdout.readline().strip().decode())
        msg = ''.join(msg_list)
        _read_time = 0
    else:
        msg = self.stdout.readline().strip().decode()
        _read_time -= 1

    setattr(self, '_read_time', _read_time)
    return msg


def close(self):
    self.stdin.write(b'$exit\n')
    self.kill()


def enhance_popen(p):
    from types import MethodType

    p.send = MethodType(send, p)
    p.recv = MethodType(recv, p)
    p.close = MethodType(close, p)

    return p

__p_recognize = None  # private var!!!


def _close_recognize_process():
    if __p_recognize is not None:
        __p_recognize.send('$exit')
        __p_recognize.kill()


def start_recognize_char_daemon():  # singleton include recognize_char because of saver.restore
    global __p_recognize
    if __p_recognize is not None and __p_recognize.poll() is None:
        raise OSError('the checkpoint is used by another reconize process')
    else:
        p = Popen([sys.executable, __file__, 'recognize_char'],
                  bufsize=102400,
                  stdin=PIPE, stdout=PIPE, stderr=PIPE)
        # p.stdin.encoding = 'utf8'  # so we get `str` instead of `bytes` in p
        p = enhance_popen(p)
        __p_recognize = p
        return p


def start_recognize_daemon():  # singleton
    global __p_recognize
    if __p_recognize is not None and __p_recognize.poll() is None:
        raise OSError('the checkpoint is used by another reconize process')
    else:
        p = Popen([sys.executable, __file__],
                  bufsize=102400,
                  stdin=PIPE, stdout=PIPE, stderr=PIPE)
        # p.stdin.encoding = 'utf8'  # so we get `str` instead of `bytes` in p
        p = enhance_popen(p)
        __p_recognize = p
        return p


def cli():
    # print(sys.argv)
    if len(sys.argv) == 1:
        recognize_p()
    elif len(sys.argv) == 2:
        if sys.argv[1] == 'recognize_char':
            recognize_char_p()
        elif sys.argv[1] == 'recognize':
            recognize_p()

if __name__ == '__main__':
    cli()
