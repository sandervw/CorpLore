import json
import random
import sys
from pathlib import Path


def get_random_tags(filename: str, count: int) -> list[str]:
    """
    Randomly select tags from a JSON file containing a 'tags' array.

    Args:
        filename: Relative path to the JSON file
        count: Number of tags to select (no repeats)

    Returns:
        List of randomly selected tag strings
    """
    script_dir = Path(__file__).parent
    filepath = script_dir / filename

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    tags = data.get('tags', [])

    if count > len(tags):
        count = len(tags)

    return random.sample(tags, count)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <filename> <count>")
        sys.exit(1)

    filename = sys.argv[1]
    count = int(sys.argv[2])

    result = get_random_tags(filename, count)
    print(json.dumps(result))
