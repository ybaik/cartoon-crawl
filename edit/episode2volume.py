# -*- coding: utf-8 -*-

import os
import shutil
import numpy as np


episode2vol = {
    1: [1, 14],
    2: [15, 28],
    3: [29, 42],
    4: [43, 56],
    5: [57, 70],
    6: [71, 82],
    7: [83, 94],
    8: [95, 106],
    9: [107, 118],
    10: [119, 130],
    11: [131, 142],
    12: [143, 154],
    13: [155, 166],
    14: [167, 178],
}


def gen_bg_img(h, w):
    white_image = np.full((h, w, 1), 255, dtype=np.uint8)
    return white_image


def main():
    skip_1page = True
    keep_1page_for_1st_episode = True
    skip_last_page = False
    src_base_dir = "c:/comix/etc/a"
    dst_base_dir = "c:/comix/etc/c"
    bgfile = "c:/comix/etc/c/white.png"
    add_bg_file = False

    for vol, (s, e) in episode2vol.items():
        dst_dir = f"{dst_base_dir}/{vol:02d}"
        os.makedirs(dst_dir, exist_ok=True)

        for episode in range(s, e + 1):
            src_dir = f"{src_base_dir}/{episode}화"
            if not os.path.exists(src_dir):
                print(f"Skipping non-existent directory: {src_dir}")
                continue

            files = sorted(os.listdir(src_dir))
            if skip_1page and not (keep_1page_for_1st_episode and episode == s):
                files = files[1:]  # Skip the first file if required
            if skip_last_page:
                files = files[:-1]  # Skip the last file if required

            for i, f in enumerate(files):
                if keep_1page_for_1st_episode and episode == s and i == 0:
                    dst_filename = f"{vol:02d}-000-001{os.path.splitext(f)[1]}"
                else:
                    dst_filename = (
                        f"{vol:02d}-{episode:03d}-{(i + 3):03d}{os.path.splitext(f)[1]}"
                    )
                shutil.copyfile(f"{src_dir}/{f}", f"{dst_dir}/{dst_filename}")

            if add_bg_file and episode < e:
                shutil.copyfile(
                    bgfile,
                    f"{dst_dir}/{vol:02d}-{episode:03d}-{(len(files) + 3):03d}{os.path.splitext(bgfile)[1]}",
                )


if __name__ == "__main__":
    main()
