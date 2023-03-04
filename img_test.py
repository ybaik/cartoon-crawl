# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np


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
    vol = 2
    base_path = f"D:/comix/etc/a/{vol:02d}"

    for i in range(0, 2):
        src_img_path = f"{base_path}/{vol:02d}-000-{i:03d}.png"
        if not os.path.exists(src_img_path):
            continue
        img = cv2.imread(src_img_path)
        cutting(img, src_img_path, right_cut=False)

    # for i in range(2, 3):
    #     src_img_path = f"{base_path}/{vol:02d}-000-{i:03d}.png"
    #     if not os.path.exists(src_img_path):
    #         continue
    #     img = cv2.imread(src_img_path)
    #     cutting(img, src_img_path, right_cut=True)

    print(1)

    # for i in range(14, 15):
    #     src_img_path = f"{base_path}/{i:02d}-000-005.png"
    #     dst_img_path = f"{base_path}/{i:02d}-000-007.png"
    #     img = cv2.imread(src_img_path)
    #     h, w, c = img.shape

    #     # if h != 1800 or w != 2400 or c != 3:
    #     #     print(i)
    #     #     continue
    #     # if h != 1920 or w != 2730 or c != 3:
    #     #     print(i)
    #     #     continue

    #     nw = int(w / 2)
    #     new_img = np.zeros((h, nw, c), np.uint8)
    #     new_img = img[:, nw:, :]

    #     cv2.imwrite(dst_img_path, new_img)

    # cv2.imshow("a", img)
    # cv2.waitKey(0)


if __name__ == "__main__":
    main()
