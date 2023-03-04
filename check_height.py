# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm

exts = [".jpg", ".png", ".gif"]


def main():
    base_path = "D:\comix\etc/허리케인 죠"
    check_ext_only = True
    check_ext_only = False

    exts_ = dict()
    dirs = os.listdir(base_path)

    if not check_ext_only:
        cnt = 0
        for folder in dirs:
            target_path = f"{base_path}/{folder}"
            if not os.path.isdir(target_path):
                continue
            cnt += 1
        csv_head = ["volumn", "median height(px)", "min height(px)", "max height(px)"]
        df = pd.DataFrame(index=range(0, cnt), columns=csv_head)

    cnt = 0
    for folder in tqdm(dirs):
        target_path = f"{base_path}/{folder}"
        if not os.path.isdir(target_path):
            continue
        # print(folder)
        files = os.listdir(target_path)
        heights = []
        for file in files:
            name, ext = os.path.splitext(file)
            exts_[ext] = 1

            fsize = os.path.getsize(f"{target_path}/{file}")
            if fsize < 10000:
                print(f"{target_path}/{file}: {fsize} byte")

            if ext not in exts:
                if ext in [".JPG", ".jpeg"]:
                    os.rename(f"{target_path}/{file}", f"{target_path}/{name}.jpg")
                print(target_path, file)
                continue

            if not check_ext_only:
                file_path = f"{target_path}/{file}"
                img_array = np.fromfile(file_path, np.uint8)
                # img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)

                if img is None:
                    print(f"None: {target_path}/{file}")
                    continue
                h, wc = img.shape
                heights.append(h)

        if not check_ext_only:
            median = int(np.median(heights))
            min = int(np.min(heights))
            max = int(np.max(heights))
            df.iloc[cnt] = {
                "volumn": folder,
                "median height(px)": median,
                "min height(px)": min,
                "max height(px)": max,
            }
        cnt += 1

    if not check_ext_only:
        df.to_csv(f"{base_path}/info.csv", index=False)
    print(exts_)


if __name__ == "__main__":
    main()
