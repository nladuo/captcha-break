# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
# add spliter into sys.path
import os
import sys
tensorflow_impl_dir = os.path.dirname(__file__)
weibo_cn_dir = os.path.dirname(tensorflow_impl_dir)
spliter_dir = os.path.join(weibo_cn_dir, 'spliter')
spliter_py_dir = os.path.join(spliter_dir, 'spliter_py')
sys.path.append(spliter_py_dir)

