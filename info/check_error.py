import os
import re
import json
from pathlib import Path


MAIN_DIRS = ["미완", "미완_스캔", "연재중", "연재중_스캔", "완결", "완결_스캔"]


def main():
    check_dir = Path("e:/comix")

    for main in MAIN_DIRS:
        main_dir = check_dir / main

        for title in os.listdir(main_dir):
            vol_dir = main_dir / title
            for vol in os.listdir(vol_dir):
                if not "error" in vol:
                    continue
                print(vol_dir)


if __name__ == "__main__":
    main()
