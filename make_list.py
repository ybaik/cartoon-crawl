import os
import pandas as pd
from common.info import MAIN_DIRS


def main():
    base_dir = "d:/comix"
    save_dir = "c:/comix"

    # Gather information
    doc_dict = dict()
    for main in MAIN_DIRS:
        main_dir = os.path.join(base_dir, main)
        titles = os.listdir(main_dir)

        for title in titles:
            verified = False
            if "[o]" in title:
                # title = title.replace("[o]", "").strip()
                verified = True

            vols = title.split(" ")[-1]
            title = title[: len(title) - len(vols)].strip()

            doc_info = {
                "title": title,
                "vols": vols,
                "verified": "O" if verified else "X",
                "status": main,
            }
            doc_dict[title] = doc_info

    # Save to csv
    doc_list = list(doc_dict.keys())
    doc_list.sort()
    csv_head = ["Title", "Volumns", "Verified", "Status"]
    df = pd.DataFrame(index=range(0, len(doc_list)), columns=csv_head)

    for i, key in enumerate(doc_list):
        doc_info = doc_dict[key]
        df.iloc[i] = {
            "Title": doc_info["title"],
            "Volumns": doc_info["vols"],
            "Verified": doc_info["verified"],
            "Status": doc_info["status"],
        }
    df.to_csv(f"{save_dir}/info.csv", index=False, encoding="cp949")


if __name__ == "__main__":
    main()
