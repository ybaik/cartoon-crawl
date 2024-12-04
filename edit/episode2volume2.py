# -*- coding: utf-8 -*-

import os
import shutil
import numpy as np


episode2vol = {
    6: [46, 55],
    7: [56, 65],
    8: [66, 75],
    9: [76, 85],
    10: [86, 95],
    11: [96, 105],
    12: [106, 115],
    13: [116, 125],
    14: [126, 135],
    15: [136, 145],
    16: [146, 155],
    17: [156, 165],
    18: [166, 175],
    19: [176, 185],
    20: [186, 195],
    21: [196, 205],
    22: [206, 215],
    23: [216, 225],
    24: [226, 235],
    25: [236, 245],
    26: [246, 255],
    27: [256, 265],
    28: [266, 275],
    29: [276, 286],
}


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

        for new_episode, episode in enumerate(range(s, e + 1), 1):
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
                    dst_filename = f"{vol:02d}-000-000{os.path.splitext(f)[1]}"
                else:
                    dst_filename = f"{vol:02d}-{new_episode:03d}-{(i + 3):03d}{os.path.splitext(f)[1]}"
                shutil.copyfile(f"{src_dir}/{f}", f"{dst_dir}/{dst_filename}")

            if add_bg_file and episode < e:
                shutil.copyfile(
                    bgfile,
                    f"{dst_dir}/{vol:02d}-{new_episode:03d}-{(len(files) + 3):03d}{os.path.splitext(bgfile)[1]}",
                )


if __name__ == "__main__":
    main()
