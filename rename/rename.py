# -*- coding: utf-8 -*-

import os
from pathlib import Path


def main():
    base_dir = Path("c:/comix/etc/a")
    vols = os.listdir(base_dir)
    for vol in vols:
        src_path = base_dir / vol
        if not src_path.is_dir():
            continue

        new = vol
        new = new.replace(" ", "")
        # new = f"{int(new):02d}"
        if new != vol:
            os.rename(src_path, base_dir / new)


if __name__ == "__main__":
    main()
