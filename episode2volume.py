# -*- coding: utf-8 -*-

import os
import shutil

episode2vol = {
    1: [1, 9],
    2: [10, 18],
    3: [19, 27],
    4: [28, 36],
    5: [37, 45],
    6: [46, 54],
    7: [55, 63],
    8: [64, 72],
    9: [73, 81],
    10: [82, 90],
    11: [91, 99],
    12: [100, 108],
    13: [109, 117],
}


def main():
    base_path = "D:\comix\기타작업\엿보기 구멍"
    base_path1 = "D:\comix\기타작업\엿보기 구멍a"

    for k in episode2vol.keys():
        [s, e] = episode2vol.get(k)
        target = f"{base_path1}/{k:02d}권"
        os.makedirs(target, exist_ok=True)

        first_start_index = True
        for i in range(s, e + 1):
            src_dir = f"{base_path}/{i}화"

            if not os.path.exists(src_dir):
                print(src_dir)
                continue

            files = os.listdir(src_dir)

            for j, f in enumerate(files):

                if j == 0:
                    if not first_start_index:
                        continue
                    first_start_index = False

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
