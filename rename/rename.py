# -*- coding: utf-8 -*-

import os
from pathlib import Path


def main():
    base_dir = Path("c:/comix/etc/a")
    vols = os.listdir(base_dir)
    vols.sort()
    for vol in vols:
        src_path = base_dir / vol
        if not src_path.is_dir():
            continue

        new = vol.replace("화", "")
        # new = f"{int(new):02d}"
        if new != vol:
            os.rename(src_path, base_dir / new)


def main2():

    vol_range = [21, 25]

    for vol in range(vol_range[0], vol_range[-1] + 1):

        base_dir = Path(f"c:/comix/etc/cc/{vol:02d}")

        target_page = 5
        files = os.listdir(base_dir)
        files.sort()

        for file in files:
            name, ext = os.path.splitext(file)
            tags = name.split("-")

            if tags[1] == "000":
                continue

            page = int(tags[2])
            if page > target_page:
                break

            renamed = f"{tags[0]}-000-{page:03d}{ext}"
            os.rename(base_dir / file, base_dir / renamed)


if __name__ == "__main__":
    # main()
    main2()
