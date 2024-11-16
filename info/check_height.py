# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm


def check_height(base_dir: str, clean_scan: bool = False, check_ext_only: bool = False):
    """
    Checks the height of images in the given directory.

    Args:
        base_dir (str): The base directory to check.
        clean_scan (bool): Whether to mark as clean scan. Defaults to False.
        check_ext_only (bool): Whether to only check the extension. Defaults to False.

    Returns:
        None
    """
    supported_exts = [".jpg", ".png", ".gif"]
    dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    if not check_ext_only:
        csv_head = ["Vol.", "Clean.Scan", "Height.Med", "Height.Min", "Height.Max"]
        df = pd.DataFrame(columns=csv_head)

    for folder in tqdm(dirs):
        target_dir = os.path.join(base_dir, folder)
        files = [
            f
            for f in os.listdir(target_dir)
            if os.path.splitext(f)[1].lower() in supported_exts
        ]
        heights = []
        for file in files:
            file_path = os.path.join(target_dir, file)
            if not check_ext_only:
                img = cv2.imdecode(
                    np.fromfile(file_path, np.uint8), cv2.IMREAD_GRAYSCALE
                )
                if img is not None:
                    heights.append(img.shape[0])
        if not check_ext_only:
            if heights:
                median = int(np.median(heights))
                min_height = int(np.min(heights))
                max_height = int(np.max(heights))
                df = df._append(
                    {
                        "Vol.": folder,
                        "Clean.Scan": "O" if clean_scan else "X",
                        "Height.Med": f"{median:4d}",
                        "Height.Min": f"{min_height:4d}",
                        "Height.Max": f"{max_height:4d}",
                    },
                    ignore_index=True,
                )
    if not check_ext_only:
        df.to_csv(os.path.join(base_dir, "info.csv"), index=False)


if __name__ == "__main__":
    base_dir = "c:/comix/etc/d"
    clean_scan = True
    check_ext_only = True
    check_ext_only = False

    check_height(base_dir, clean_scan, check_ext_only)
