import argparse
import json
import random
from pathlib import Path

DEFAULT_FILE = Path(__file__).resolve().parent.parent / "assets" / "Grounding-Details.json"


def sample_strings(file_path, count):
    strings = json.loads(Path(file_path).read_text(encoding="utf-8"))
    if count >= len(strings):
        return strings
    return random.sample(strings, count)


def main():
    parser = argparse.ArgumentParser(description="Randomly sample strings from a JSON array file.")
    parser.add_argument("count", type=int, help="Number of strings to sample")
    parser.add_argument("--file", default=DEFAULT_FILE, help="Path to JSON file (array of strings)")
    args = parser.parse_args()

    for s in sample_strings(args.file, args.count):
        print(s)


if __name__ == "__main__":
    main()
