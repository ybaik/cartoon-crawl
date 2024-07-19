# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm

exts = [".jpg", ".png", ".gif"]


def check_height(base_path, clean_scan=False, check_ext_only=False):
    exts_ = set()
    targets = os.listdir(base_path)
    dirs = []
    for target in targets:
        target_path = f"{base_path}/{target}"
        if not os.path.isdir(target_path):
            continue
        dirs.append(target)

    if not check_ext_only:
        cnt = len(dirs)
        csv_head = ["Vol.", "Clean.Scan", "Height.Med", "Height.Min", "Height.Max"]
        df = pd.DataFrame(index=range(0, cnt), columns=csv_head)

    cnt = 0
    for folder in tqdm(dirs):
        target_dir = f"{base_path}/{folder}"
        if not os.path.isdir(target_dir):
            continue
        # print(folder)
        files = os.listdir(target_dir)
        heights = []
        for file in files:
            name, ext = os.path.splitext(file)
            exts_.add(ext)

            fsize = os.path.getsize(f"{target_dir}/{file}")
            if fsize < 10000:
                print(f"{target_dir}/{file}: {fsize} byte")
            if ext not in exts:
                if ext in [".JPG", ".jpeg"]:
                    os.rename(f"{target_dir}/{file}", f"{target_dir}/{name}.jpg")
                print(target_dir, file)
                continue

            if not check_ext_only:
                file_path = f"{target_dir}/{file}"
                img_array = np.fromfile(file_path, np.uint8)
                # img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)

                if img is None:
                    print(f"None: {target_dir}/{file}")
                    continue
                h, wc = img.shape
                heights.append(h)

        if not check_ext_only:
            median = int(np.median(heights))
            min = int(np.min(heights))
            max = int(np.max(heights))
            df.iloc[cnt] = {
                "Vol.": folder,
                "Clean.Scan": "O" if clean_scan else "X",
                "Height.Med": f"{median:4d}",
                "Height.Min": f"{min:4d}",
                "Height.Max": f"{max:4d}",
            }
        cnt += 1

    if not check_ext_only:
        df.to_csv(f"{base_path}/info.csv", index=False)
    print(exts_)


if __name__ == "__main__":
    base_path = "D:\comix\etc\c"
    clean_scan = True
    check_ext_only = False

    check_height(base_path, clean_scan, check_ext_only)
