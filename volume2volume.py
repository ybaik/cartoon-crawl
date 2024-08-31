# -*- coding: utf-8 -*-

import os
import shutil
from pathlib import Path


def main():
    src_dir = Path("c:/comix/etc/a")
    dst_dir = Path("c:/comix/etc/a")

    volumes = [78]

    index = 1

    for vol in volumes:

        dst_vol_dir = dst_dir / str(vol)
        if not dst_vol_dir.exists():
            dst_vol_dir.mkdir()

        for sub in ["1화", "2화", "3화"]:
            src_vol_dir = src_dir / f"{vol}-{sub}"
            files = os.listdir(src_vol_dir)
            files.sort()

            for f in files:
                src_path = src_vol_dir / f
                ext = src_path.suffix
                dst_path = dst_vol_dir / f"{index:03d}{ext}"
                shutil.copy2(src_path, dst_path)
                index += 1


if __name__ == "__main__":
    main()
