# -*- coding: utf-8 -*-

import os
import shutil


def main():
    vol = 23
    base_dir = f"c:/comix/etc/b/{vol:02d}"

    bg_file = "c:/comix/etc/c/01-002-026.png"

    ch_max = 0
    ch_page = dict()

    files = os.listdir(base_dir)
    for file in files:
        name, ext = os.path.splitext(file)
        tags = name.split("-")
        if len(tags) != 3:
            continue

        if tags[1] == "ext":
            continue

        ch = int(tags[1])

        if ch < 1:
            continue

        page = int(tags[2])

        if ch not in ch_page:
            ch_page[ch] = page
        else:
            if page > ch_page[ch]:
                ch_page[ch] = page

        ch_max = max(ch_max, ch)

    for k, v in ch_page.items():
        if k != ch_max:
            target_path = f"{base_dir}/{vol:02d}-{k:03d}-{v+1:03d}.png"
            shutil.copyfile(bg_file, target_path)


if __name__ == "__main__":
    main()
