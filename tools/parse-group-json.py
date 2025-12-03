import argparse
import json
import pathlib


class Args:
    groups_file: pathlib.Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("groups_file", type=pathlib.Path)
    ns = Args()
    return parser.parse_args(namespace=ns)


def main():
    args = parse_args()
    data = json.loads(args.groups_file.read_text())
    for g in data:
        email = g.get("user").get("email")
        group_name = g.get("user").get("username")
        print(f"{email},{group_name}")


if __name__ == "__main__":
    main()
