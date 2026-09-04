#!/usr/bin/env python
"""Align every blob's text to the chapter outline via one OpenRouter call.

Usage:
    python fix_blobs.py <path-to-chapter.json>

Sends outline, context, and the {number, text} array to a single model,
which returns the same array minimally corrected. Writes back in place.
Reads OPENROUTER_API_KEY from the environment or from assets/.env. Stdlib only.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

MODEL = "~google/gemini-flash-latest"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MAX_ATTEMPTS = 1
TIMEOUT = 600
MAX_TOKENS = 200000
TEMPERATURE = 0.5


def load_api_key():
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key.strip()
    env_path = Path(__file__).with_name(".env")
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            if k.strip() == "OPENROUTER_API_KEY":
                return v.strip().strip('"').strip("'")
    sys.exit("No OPENROUTER_API_KEY found (checked environment and assets/.env).")


def build_messages(chapter):
    items = [
        {"number": b["number"], "text": b.get("text", "")}
        for b in chapter["blobs"]
    ]
    ctx = chapter.get("context", [])
    ctx = "\n".join(f"- {c}" for c in ctx) if isinstance(ctx, list) else str(ctx)
    system = (
        "You are a continuity editor for a work of continuous fiction. You receive "
        "the chapter outline, story context, and an array of prose passages "
        "(numbered in chapter order). Your job: make MINIMAL corrections to each "
        "passage so the written prose correctly embodies.\n"
        "Fix ONLY clear breaks between outline *intent* and what was written: "
        "logical discrepancies, contradictory events, etc.\n"
        "Hard constraints:\n"
        "- **Change as little as possible.**.\n"
        "- **Never change the delivery form of any passage.** Dialogue stays "
        "dialogue, exposition stays exposition, etc.\n"
        "- **Never rewrite whole sections or paragraphs.**\n"
        "- **Never erase creative words, details, names, or elements.**\n"
        "- **Never add new features, elements, characters, or lines.**\n"
        "- Preserve each passage's voice, tense, and style.\n"
        "**Return ONLY a JSON array of objects** {\"number\": N, \"text\": \"...\"} "
        "with exactly the same length and the same numbers as the input array. "
        "No markdown fences, no headers, no notes, no extra fields, nothing "
        "outside the array."
    )
    user = (
        f"Chapter outline:\n{chapter.get('outline', '')}\n\n"
        f"Story context:\n{ctx}\n\n"
        "Passages to correct (JSON array):\n"
        + json.dumps(items, ensure_ascii=False, indent=2)
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def call_model(api_key, messages):
    body = json.dumps({
        "model": MODEL,
        "messages": messages,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
    }).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-Title": "CorpLore blob-fixer",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return (data["choices"][0]["message"].get("content") or "").strip()


def parse_reply(raw, expected_numbers):
    """Return list of {number, text} or raise ValueError."""
    text = raw.strip()
    fence = re.match(r"^```(?:json)?\s*\n?(.*?)\n?```\s*$", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("no JSON array found in reply:" + text)
    items = json.loads(text[start:end + 1])
    if not isinstance(items, list):
        raise ValueError("reply is not a JSON array:" + text)
    if len(items) != len(expected_numbers):
        raise ValueError(
            f"array length {len(items)} != expected {len(expected_numbers)}"
        )
    got_numbers = []
    for it in items:
        if not isinstance(it, dict) or "number" not in it or "text" not in it:
            raise ValueError("array item missing number/text keys:" + it)
        if not isinstance(it["text"], str) or not it["text"].strip():
            raise ValueError(f"blob {it['number']}: text is not a non-empty string:" + it)
        got_numbers.append(it["number"])
    if got_numbers != expected_numbers:
        raise ValueError(f"blob numbers mismatch: {got_numbers}")
    return items


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python fix_blobs.py <chapter.json>")
    path = Path(sys.argv[1])
    doc = json.loads(path.read_text(encoding="utf-8"))
    chapter = doc["chapter"]
    blobs = chapter["blobs"]

    expected_numbers = [b["number"] for b in blobs]
    old_texts = {b["number"]: b["text"] for b in blobs}
    messages = build_messages(chapter)
    api_key = load_api_key()

    last_err = ""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            raw = call_model(api_key, messages)
            items = parse_reply(raw, expected_numbers)
            break
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:200]}"
        except (ValueError, json.JSONDecodeError) as e:
            last_err = f"invalid reply: {e}"
        except Exception as e:
            last_err = repr(e)
        print(f"Attempt {attempt} failed ({last_err})", file=sys.stderr)
        if attempt < MAX_ATTEMPTS:
            time.sleep(2 * attempt)
    else:
        sys.exit(f"All {MAX_ATTEMPTS} attempts failed; file left untouched. Last error: {last_err}")

    for it in items:
        for b in blobs:
            if b["number"] == it["number"]:
                b["text"] = it["text"]
                break

    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"{'blob':>4}  {'old':>5}  {'new':>5}  {'delta':>6}  status")
    changed = 0
    for b in blobs:
        old_wc = len(old_texts[b["number"]].split())
        new_wc = len(b["text"].split())
        same = old_texts[b["number"]] == b["text"]
        status = "same" if same else "edited"
        changed += 0 if same else 1
        print(f"{b['number']:>4}  {old_wc:>5}  {new_wc:>5}  {new_wc - old_wc:>+6}  {status}")
    print(f"\n{changed}/{len(blobs)} blobs edited; written to {path}")


if __name__ == "__main__":
    main()
