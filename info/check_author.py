import json
from pathlib import Path


def main():
    json_path = Path("./db/comix_info.json")

    # Read comix list
    if json_path.exists():
        with open(json_path, encoding="utf-8") as f:
            json_data = json.load(f)
    else:
        json_data = dict()

    # Check
    author_keys = dict()
    for key in json_data.keys():
        data = json_data[key]
        authors = data["author"]["kor"].split(",")

        if "[o]" in key:
            if data["verified"] == "X":
                print(key)
        else:
            if data["verified"] == "O":
                print(key)
        for author in authors:
            if author_keys.get(author) is not None:
                author_keys[author] += 1
            else:
                author_keys[author] = 1

    author_keys = sorted(author_keys.items(), key=lambda x: x[1], reverse=True)
    print(1)


if __name__ == "__main__":
    main()
