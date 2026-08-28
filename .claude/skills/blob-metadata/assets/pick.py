#!/usr/bin/env python
"""Pull random strings from a named array in blob-data.json.

Usage: python pick.py <array_name> [number]
"""
import json
import random
import sys
from pathlib import Path

DATA = Path(__file__).with_name("blob-data.json")


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python pick.py <array_name> [number]")

    name = sys.argv[1]
    data = json.loads(DATA.read_text(encoding="utf-8"))

    if name not in data:
        sys.exit(f"No such array '{name}'. Options: {', '.join(data)}")

    items = data[name]

    if len(sys.argv) >= 3:
        n = int(sys.argv[2])
        if n < len(items):
            items = random.sample(items, n)

    print(json.dumps(items))


if __name__ == "__main__":
    main()
