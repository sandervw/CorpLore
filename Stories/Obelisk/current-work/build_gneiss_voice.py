import argparse
import json
import random
from pathlib import Path

# Generates the Necromancer voice guide by stitching gneiss_template.json
# (fixed structure + sample directives) together with freshly-sampled entries
# from gneiss_vocabulary.json. Run once per session to get a varied voice reference.
#
# Usage:
# - 'python build_gneiss_voice.py' writes the guide to ../references/gneiss-voice.md
# - 'python build_gneiss_voice.py path/to/out.md' writes to the given path instead

HERE = Path(__file__).parent
VOCAB_PATH = HERE / "gneiss_vocabulary.json"
TEMPLATE_PATH = HERE / "gneiss_template.json"
# Default lands in the skill's references/ folder, alongside the static voices.
DEFAULT_OUTPUT = HERE.parent / "references" / "gneiss-voice.md"


def format_sample(items: list[str], fmt: str) -> str:
    if fmt == "lines":
        return "\n\n".join(items)
    if fmt == "blockquote_lines":
        return "\n".join(f"> {x}" for x in items)
    if fmt == "blockquote_comma":
        return "> " + ", ".join(items)
    if fmt == "inline_comma":
        return ", ".join(items)
    raise ValueError(f"Unknown format: {fmt}")


def build(output_path: Path) -> None:
    with VOCAB_PATH.open(encoding="utf-8") as f:
        vocab = json.load(f)
    with TEMPLATE_PATH.open(encoding="utf-8") as f:
        template = json.load(f)

    parts: list[str] = []
    for block in template:
        kind = block["type"]
        if kind == "static":
            parts.append(block["text"])
        elif kind == "sample":
            source = block["source"]
            n = block["n"]
            arr = vocab[source]
            if n > len(arr):
                raise ValueError(f"Requested {n} from '{source}' but only {len(arr)} available.")
            items = random.sample(arr, n)
            parts.append(format_sample(items, block["format"]))
        else:
            raise ValueError(f"Unknown block type: {kind}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("".join(parts), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build the Necromancer voice guide from gneiss_template.json and gneiss_vocabulary.json.")
    parser.add_argument("filename", nargs="?", default=None, help="Output path (defaults to ../references/gneiss-voice.md).")
    args = parser.parse_args()
    output = Path(args.filename) if args.filename else DEFAULT_OUTPUT
    build(output)
