# coding:utf-8
import os
from PIL import Image
import numpy as np
import uuid


def split_and_save(path):
    path = "../downloader/captchas/" + path
    pix = np.array(Image.open(path).convert("L"))
    # threshold image
    pix = (pix > 100) * 255

    col_ranges = [
        [5, 5 + 8],
        [14, 14 + 8],
        [23, 23 + 8],
        [32, 32 + 8]
    ]
    # split and save
    for col_range in col_ranges:
        letter = pix[:, col_range[0]: col_range[1]]
        im = Image.fromarray(np.uint8(letter))
        save_path = "./letters/" + str(uuid.uuid4()) + ".png"
        im.save(save_path)


if __name__ == "__main__":

    im_paths = filter(lambda fn: os.path.splitext(fn)[1].lower() == '.png',
                      os.listdir("../downloader/captchas"))

    for im_path in im_paths:
        print im_path
        split_and_save(im_path)
