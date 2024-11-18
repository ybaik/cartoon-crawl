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
    vol = 10
    base_dir = f"c:/comix/etc/c"
    # base_path = f"c:/comix/etc/c"
    page = 3
    crop_right = True
    src_img_path = f"{base_dir}/{vol:02d}-000-{page:03d}.png"
    dst_img_path = f"{base_dir}/{vol:02d}/{vol:02d}-000-{page:03d}.png"

    if os.path.exists(src_img_path):
        img = cv2.imread(src_img_path)
        img_crop(img, dst_img_path, crop_right)


if __name__ == "__main__":
    main()
