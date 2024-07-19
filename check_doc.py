# -*- coding: utf-8 -*-

import os
import pandas as pd


def main():
    base_path = "D:/comix/verified/완결_스캔"
    base_path = "D:/comix/미완"

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
