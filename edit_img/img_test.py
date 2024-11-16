# -*- coding: utf-8 -*-

import os
import cv2


def cutting(img, src_img_path, right_cut):
    _, w, _ = img.shape
    nw = w // 2
    new_img = img[:, nw:, :] if right_cut else img[:, :nw, :]
    cv2.imwrite(src_img_path, new_img)


def main():
    vol = 1
    base_path = f"c:/comix/etc/c/{vol:02d}"
    # base_path = f"c:/comix/etc/c"
    page = 2

    src_img_path = f"{base_path}/{vol:02d}-000-{page:03d}.png"
    if os.path.exists(src_img_path):
        img = cv2.imread(src_img_path)
        cutting(img, src_img_path, right_cut=True)


if __name__ == "__main__":
    main()
