# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
from pathlib import Path


def cutting(img, src_img_path, right_cut):
    h, w, c = img.shape
    nw = int(w / 2)
    new_img = np.zeros((h, nw, c), np.uint8)

    if right_cut:
        new_img = img[:, nw:, :]
    else:
        new_img = img[:, :nw, :]
    cv2.imwrite(src_img_path, new_img)


def main():
    vol = 58
    src_dir = Path(f"c:/comix/etc/b/{vol:02d}")
    dst_dir = Path(f"c:/comix/etc/a/{vol:02d}")

    src_img_path = src_dir / "018.jpg"
    img = cv2.imread(src_img_path)
    h, w, c = img.shape
    nh = int(h / 7)

    start = 0
    end = nh
    for i in range(7):
        new_img = img[start:end, :, :]
        dst_img_path = dst_dir / f"{i+18:03d}.png"
        cv2.imwrite(dst_img_path, new_img)
        start += nh
        end += nh


if __name__ == "__main__":
    main()
