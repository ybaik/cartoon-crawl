# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np


def img_crop(
    img: np.ndarray,
    dst_img_path: str,
    crop_right: bool = True,
    dst_img_path2: str = None,
):
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

    if dst_img_path2 is not None:
        cv2.imwrite(dst_img_path2, img[:, :nw, :])


def main():
    vol = 23
    base_dir = f"c:/comix/etc/c"
    # base_path = f"c:/comix/etc/c"
    page = 3
    crop_right = True  # True
    src_img_path = f"{base_dir}/{vol:02d}/{vol:02d}-000-{page:03d}.png"
    dst_img_path = f"{base_dir}/{vol:02d}/{vol:02d}-000-{page:03d}.png"
    dst_img_path2 = f"{base_dir}/{vol:02d}/{vol:02d}-000-{page+1:03d}.png"
    # src_img_path = f"{base_dir}/{vol:02d}-000-{page:03d}.png"
    # dst_img_path = f"{base_dir}/{vol:02d}-000-{page:03d}.png"

    if os.path.exists(src_img_path):
        img = cv2.imread(src_img_path)
        img_crop(img, dst_img_path, crop_right, dst_img_path2)


def main2():
    base_dir = "C:/comix/etc/c"
    target_page = 3

    files = os.listdir(base_dir)
    for file in files:
        path = f"{base_dir}/{file}"
        if not os.path.isfile(path):
            continue
        name, ext = os.path.splitext(file)
        # if ext != ".png":
        #     continue
        tags = name.split("-")
        if len(tags) != 3:
            continue

        if int(tags[1]) != 0:
            continue

        if int(tags[2]) == target_page:
            src_img_path = path
            dst_img_path = path
            dst_img_path2 = f"{base_dir}/{tags[0]}-000-{target_page+1:03d}.png"
            img = cv2.imread(src_img_path)
            img_crop(img, dst_img_path, True, dst_img_path2)


if __name__ == "__main__":
    # main()
    main2()
