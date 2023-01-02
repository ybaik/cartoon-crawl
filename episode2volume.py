# -*- coding: utf-8 -*-

import os
import shutil

episode2vol = {
    # 1: [1, 7],
    2: [8, 16],
    # 3: [17, 25],
    # 4: [26, 34],
    # 5: [35, 43],
    # 6: [44, 52],
    # 7: [53, 61],
    # 8: [62, 70],
    # 9: [71, 79],
    # 10: [80, 88],
    # 11: [89, 97],
    # 12: [98, 103],
    # 12: [98, 106],
    # 13: [107, 115],
    # 14: [116, 124],
    # 15: [125, 133],
    # 16: [134, 142],
    # 17: [143, 151],
    # 18: [152, 160],
    # 19: [161, 169],
    # 20: [170, 178],
    # 21: [179, 187],
    # 22: [188, 196],
    # 23: [197, 205],
}


def main():
    base_path = "D:\comix\체인소맨"
    base_path1 = "D:\comix\체인소맨a"

    for k in episode2vol.keys():
        [s, e] = episode2vol.get(k)
        target = f"{base_path1}/{k:02d}권"
        os.makedirs(target, exist_ok=True)
        for i in range(s, e + 1):
            src_dir = f"{base_path}/{i}화"
            if not os.path.exists(src_dir):
                print(src_dir)
                continue
            files = os.listdir(src_dir)
            for f in files:
                [id, ext] = f.split(".")
                if i < 1000:
                    shutil.copyfile(
                        f"{src_dir}/{f}", f"{target}/{k:02d}-{i:03d}-{id}.{ext}"
                    )
                else:
                    shutil.copyfile(
                        f"{src_dir}/{f}", f"{target}/{k:02d}-last-ball-{id}.{ext}"
                    )


if __name__ == "__main__":
    main()
