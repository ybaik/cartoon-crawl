# -*- coding: utf-8 -*-

import os


def rename(base_path, files):
    for i, file in enumerate(files, start=1):
        os.rename(
            os.path.join(base_path, file),
            f"{base_path}/{i:03d}{os.path.splitext(file)[1]}",
        )


def main():

    base_dir = "C:/comix/etc/a"
    vol_range = [31]

    for vol in range(vol_range[0], vol_range[-1] + 1):
        target_dir = f"{base_dir}/{vol:02d}"
        rename(target_dir, sorted(os.listdir(target_dir)))


if __name__ == "__main__":
    main()
