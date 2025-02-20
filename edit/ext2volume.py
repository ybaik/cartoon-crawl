# -*- coding: utf-8 -*-

import os
import shutil
import numpy as np


def main():

    src_base_dir = "c:/comix/etc/a"
    dst_base_dir = "c:/comix/etc/c"

    vol = 32
    episode = "번외편"
    target_episode = "ext"

    dst_dir = f"{dst_base_dir}/{vol:02d}"

    src_dir = f"{src_base_dir}/{episode}"
    if not os.path.exists(src_dir):
        print(f"Skipping non-existent directory: {src_dir}")
        return

    files = sorted(os.listdir(src_dir))
    for i, f in enumerate(files):
        dst_filename = (
            f"{vol:02d}-{target_episode}-{(i + 11):03d}{os.path.splitext(f)[1]}"
        )
        shutil.copyfile(f"{src_dir}/{f}", f"{dst_dir}/{dst_filename}")


if __name__ == "__main__":
    main()
