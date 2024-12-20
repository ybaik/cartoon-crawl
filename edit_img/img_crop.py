# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np


def img_crop(img: np.ndarray, dst_img_path: str, crop_right: bool = True):
    """
    Crops an image in half either on the right or left side and saves it to a specified path.

    Args:
        img (np.ndarray): The source image to be cropped.
        dst_img_path (str): The path to save the cropped image.
        get_right (bool, optional): Whether to get the right half of the image. Defaults to True.

    Returns:
        None
    """
    _, w, _ = img.shape
    nw = w // 2
    new_img = img[:, nw:, :] if crop_right else img[:, :nw, :]
    cv2.imwrite(dst_img_path, new_img)


def main():
    vol = 17
    base_dir = f"c:/comix/etc/c"
    # base_path = f"c:/comix/etc/c"
    page = 5
    crop_right = True  # True
    src_img_path = f"{base_dir}/{vol:02d}/{vol:02d}-000-{page:03d}.png"
    dst_img_path = f"{base_dir}/{vol:02d}/{vol:02d}-000-{page:03d}.png"
    # src_img_path = f"{base_dir}/{vol:02d}-000-{page:03d}.png"
    # dst_img_path = f"{base_dir}/{vol:02d}-000-{page:03d}.png"

    if os.path.exists(src_img_path):
        img = cv2.imread(src_img_path)
        img_crop(img, dst_img_path, crop_right)


def main2():
    base_dir = "C:/comix/etc/b/68"
    dst_dir = "C:/comix/etc/b/68-1"

    cnt = 1
    for i in range(1, 4):
        src_img_path = f"{base_dir}/{i:03d}.jpg"
        img = cv2.imread(src_img_path)
        h, w, _ = img.shape
        nh = h // 2
        new_img = img[:nh, :, :]

        dst_img_path = f"{dst_dir}/{cnt:03d}.png"
        cnt += 1
        cv2.imwrite(dst_img_path, new_img)

        new_img = img[nh:, :, :]
        dst_img_path = f"{dst_dir}/{cnt:03d}.png"
        cnt += 1
        cv2.imwrite(dst_img_path, new_img)

    for i in range(4, 17):
        os.rename(f"{base_dir}/{i:03d}.jpg", f"{dst_dir}/{cnt:03d}.jpg")
        cnt += 1


if __name__ == "__main__":
    main()
    # main2()
