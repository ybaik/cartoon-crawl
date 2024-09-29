# -*- coding: utf-8 -*-

import os
import shutil


episode2vol = {
    "volumn": 23,
}

start = 331

for i in range(155, 167):
    episode2vol[i] = [start, start + 1]
    start += 2

episode2vol["ext"] = [f"{start+1}화"]

print(episode2vol)


def main():
    base_path = "D:/comix/etc/도로헤도로"
    base_path1 = "D:/comix/etc/a"
    v = episode2vol["volumn"]
    target = f"{base_path1}/{v:02d}"
    os.makedirs(target, exist_ok=True)

    for k in episode2vol.keys():
        if not isinstance(k, int):
            continue

        [s, e] = episode2vol.get(k)

        cnt = 1
        for i in range(s, e + 1):
            src_dir = f"{base_path}/{i}화"

            if not os.path.exists(src_dir):
                print(src_dir)
                continue

            files = os.listdir(src_dir)
            for j, f in enumerate(files):
                if j == 0:
                    continue
                [id, ext] = f.split(".")
                shutil.copyfile(
                    f"{src_dir}/{f}", f"{target}/{v:02d}-{k:03d}-{cnt:03d}.{ext}"
                )
                cnt += 1
    if episode2vol.get("ext") is not None:
        dsts = episode2vol.get("ext")
        cnt = 1
        for dst in dsts:
            src_dir = f"{base_path}/{dst}"

            if not os.path.exists(src_dir):
                print(src_dir)
                continue

            files = os.listdir(src_dir)

            for j, f in enumerate(files):
                if j == 0:
                    continue
                [id, ext] = f.split(".")
                shutil.copyfile(
                    f"{src_dir}/{f}", f"{target}/{v:02d}-ext-{cnt:03d}.{ext}"
                )
                cnt += 1


if __name__ == "__main__":
    main()
