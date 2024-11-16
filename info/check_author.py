import json
from pathlib import Path


def main():
    json_path = Path("./db/comix_info.json")
    json_data = (
        json_path.exists() and json.load(open(json_path, encoding="utf-8")) or dict()
    )

    author_keys = {}
    for _, data in json_data.items():
        for author in data["author"]["kor"].split(","):
            author_keys[author] = author_keys.get(author, 0) + 1
    author_keys = sorted(author_keys.items(), key=lambda x: x[1], reverse=True)
    print(1)


if __name__ == "__main__":
    main()
