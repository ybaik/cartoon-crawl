# -*- coding: utf-8 -*-

import os
import shutil


def main():

    base_path = "D:/cartoon/download1"

    for i in [14]:
        target = f"{base_path}/{i:02d}화"
        # ful = len(os.listdir(target))

        # src_path1 = f"{base_path}/{i:02d}-1화"
        # src_path2 = f"{base_path}/{i:02d}-2화"

        # ful = len(os.listdir(target))
        # p1 = len(os.listdir(src_path1))
        # p2 = len(os.listdir(src_path2))
        # print(ful, p1 + p2)
        # if ful != (p1 + p2):
        #     print(i)
        #     continue

        target = f"{base_path}/{i:02d}화"
        os.makedirs(f"{base_path}/{i:02d}화", exist_ok=True)

        src_path1 = f"{base_path}/{i:02d}-1화"
        dir_list = os.listdir(src_path1)
        idx_max = 0
        for f in dir_list:
            idx = int(f.split(".")[0])
            idx_max = max(idx_max, idx)
            shutil.copyfile(f"{src_path1}/{f}", f"{target}/{f}")

        src_path2 = f"{base_path}/{i:02d}-화"
        dir_list = os.listdir(src_path2)
        for f in dir_list:
            idx = int(f.split(".")[0])
            ext = f.split(".")[1]
            idx += idx_max
            shutil.copyfile(f"{src_path2}/{f}", f"{target}/{idx:03d}.{ext}")


if __name__ == "__main__":
    main()
