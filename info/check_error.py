import os
from pathlib import Path
from common.info import MAIN_DIRS


def main():
    check_dir = Path("e:/comix")
    count_zip = 0
    for main in MAIN_DIRS:
        main_dir = check_dir / main
        for title in os.listdir(main_dir):
            vol_dir = main_dir / title
            for file in os.listdir(vol_dir):
                if file.endswith(".txt"):
                    print(f"readme: {vol_dir}/{file}")
                else:
                    count_zip += 1

    print(count_zip)


if __name__ == "__main__":
    main()
