# -*- coding: utf-8 -*-

import os
import pandas as pd
from common.info import MAIN_DIRS


def main():
    base_dir = "d:/comix"

    for main_name in MAIN_DIRS:
        main_dir = f"{base_dir}/{main_name}"
        dirs = os.listdir(main_dir)
        dirs.sort()

        for d in dirs:
            full_d = f"{main_dir}/{d}"
            files = os.listdir(full_d)
            for file in files:
                name, ext = os.path.splitext(file)
                if ext != ".txt":
                    continue
                if name != "error":
                    continue
                print(full_d, file)

    return
    # Check Dir
    ds = os.listdir(base_path)
    dirs = []
    for d in ds:
        full_path = os.path.join(base_path, d)
        if os.path.isdir(full_path):
            dirs.append(full_path)

    for d in dirs:
        files = os.listdir(d)
        for file in files:
            name, ext = os.path.splitext(file)
            if ext != ".csv":
                continue
            print(d)
            df = pd.read_csv(os.path.join(d, file), dtype=str)


if __name__ == "__main__":
    main()
