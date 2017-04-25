#!/usr/bin/env python
# coding:utf-8
import os
downloader_dir = os.path.dirname(os.path.abspath(__file__))
captchas_dir = os.path.join(downloader_dir, 'captchas')

for fn in os.listdir(captchas_dir):
    if os.path.splitext(fn)[1] == '.gif':
        os.remove(captchas_dir+fn)
