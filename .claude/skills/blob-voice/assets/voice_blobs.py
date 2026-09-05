#!/usr/bin/env python
"""Revise blob text fields into a chosen character voice using parallel OpenRouter calls.

Usage:
    python voice_blobs.py <path-to-chapter.json> <voice-type>

Supported voices:
    gneiss, necromancer, freeman, paladin, thorogood, rogue
"""
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

MODEL = "anthropic/claude-opus-5"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MAX_ATTEMPTS = 3
TIMEOUT = 300
MAX_TOKENS = 80000
TEMPERATURE = 0.5
BATCH_SIZE = 3
MAX_WORKERS = 6

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[3]
VOICE_SKILL_DIR = REPO_ROOT / ".claude" / "skills" / "voice-revision"


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


def format_sample(items: list, fmt: str) -> str:
    if fmt == "lines":
        return "\n\n".join(items)
    if fmt == "blockquote_lines":
        return "\n".join(f"> {x}" for x in items)
    if fmt == "blockquote_comma":
        return "> " + ", ".join(items)
    if fmt == "inline_comma":
        return ", ".join(items)
    raise ValueError(f"Unknown format: {fmt}")


def build_dynamic_voice(voice: str) -> str:
    assets_dir = VOICE_SKILL_DIR / "assets"
    vocab_path = assets_dir / f"{voice}_vocabulary.json"
    template_path = assets_dir / f"{voice}_template.json"
    if not vocab_path.exists() or not template_path.exists():
        ref_path = VOICE_SKILL_DIR / "references" / f"{voice}-voice.md"
        if ref_path.exists():
            return ref_path.read_text(encoding="utf-8")
        sys.exit(f"Cannot find generator templates or reference for voice '{voice}'")

    with vocab_path.open(encoding="utf-8") as f:
        vocab = json.load(f)
    with template_path.open(encoding="utf-8") as f:
        template = json.load(f)

    parts = []
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
    return "".join(parts)


def get_voice_instructions(voice: str) -> str:
    voice_key = voice.strip().lower()
    if voice_key in ("gneiss", "necromancer"):
        return build_dynamic_voice(voice_key)
    ref_path = VOICE_SKILL_DIR / "references" / f"{voice_key}-voice.md"
    if ref_path.exists():
        return ref_path.read_text(encoding="utf-8")
    sys.exit(f"Unknown voice '{voice}'. Check .claude/skills/voice-revision/references/")


def build_messages(batch_blobs, voice_instructions):
    items = [{"number": b["number"], "text": b.get("text", "")} for b in batch_blobs]
    system = (
        "Your task is to revise the provided fiction passages to embody the character voice "
        "defined in the Voice Guidelines below.\n\n"
        "**CONSTRAINTS:**\n"
        "1. ONLY CHANGE THE VOICE, cadence, syntax, and phrasing.\n"
        "2. DO NOT change the substance, events, actions, facts, or narrative beats of the story.\n"
        "3. DO NOT rewrite huge chunks or invent brand new plot elements.\n"
        "4. PRESERVE the delivery form: dialogue remains dialogue, action remains action, etc.\n"
        "5. PRESERVE approximate word length of each passage.\n"
        "6. Return ONLY a valid .json array of objects: [{\"number\": N, \"text\": \"...\"}].\n"
        "No markdown fences, no explanatory preamble, no commentary.\n\n"
        "**VOICE GUIDELINES:**\n"
        f"{voice_instructions}"
    )
    user = (
        "Revise the following passages into the specified voice. "
        "Return ONLY a .json array with the exact same numbers and updated text.\n\n"
        "**PASSAGES TO REVISE:**\n"
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
            "X-Title": "CorpLore blob-voice",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return (data["choices"][0]["message"].get("content") or "").strip()


def parse_reply(raw, expected_numbers):
    text = raw.strip()
    fence = re.match(r"^```(?:json)?\s*\n?(.*?)\n?```\s*$", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("no JSON array found in reply: " + text[:200])
    items = json.loads(text[start:end + 1])
    if not isinstance(items, list):
        raise ValueError("reply is not a JSON array")
    if len(items) != len(expected_numbers):
        raise ValueError(f"array length {len(items)} != expected {len(expected_numbers)}")
    got_numbers = []
    for it in items:
        if not isinstance(it, dict) or "number" not in it or "text" not in it:
            raise ValueError(f"item missing number/text keys: {it}")
        if not isinstance(it["text"], str) or not it["text"].strip():
            raise ValueError(f"blob {it.get('number')}: text is not non-empty string")
        got_numbers.append(it["number"])
    if got_numbers != expected_numbers:
        raise ValueError(f"numbers mismatch: got {got_numbers}, expected {expected_numbers}")
    return items


def process_batch(api_key, batch_blobs, voice):
    expected_numbers = [b["number"] for b in batch_blobs]
    last_err = ""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        voice_instructions = get_voice_instructions(voice)
        messages = build_messages(batch_blobs, voice_instructions)
        try:
            raw = call_model(api_key, messages)
            items = parse_reply(raw, expected_numbers)
            return items, "ok"
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:200]}"
        except (ValueError, json.JSONDecodeError) as e:
            last_err = f"invalid reply: {e}"
        except Exception as e:
            last_err = repr(e)
        time.sleep(2 * attempt)
    return None, f"FAILED: {last_err}"


def main():
    if len(sys.argv) < 3:
        sys.exit("Usage: python voice_blobs.py <path-to-chapter.json> <voice-type>")

    chapter_path = Path(sys.argv[1]).resolve()
    voice = sys.argv[2].strip()

    if not chapter_path.exists():
        sys.exit(f"File not found: {chapter_path}")

    doc = json.loads(chapter_path.read_text(encoding="utf-8"))
    chapter = doc.get("chapter", {})
    blobs = chapter.get("blobs", [])
    if not blobs:
        sys.exit("No blobs found in chapter JSON.")

    api_key = load_api_key()
    batches = [blobs[i:i + BATCH_SIZE] for i in range(0, len(blobs), BATCH_SIZE)]
    old_texts = {b["number"]: b.get("text", "") for b in blobs}

    print(f"Processing {len(blobs)} blobs in {len(batches)} batches using voice '{voice}'...")

    results = {}
    errors = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(process_batch, api_key, batch, voice)
            for batch in batches
        ]
        for f in futures:
            items, status = f.result()
            if status != "ok" or not items:
                errors.append(status)
            else:
                for it in items:
                    results[it["number"]] = it["text"]

    if errors or len(results) != len(blobs):
        sys.exit(f"Errors occurred during processing; file untouched. Errors: {errors}")

    for b in blobs:
        b["text"] = results[b["number"]]

    chapter_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"{'blob':>4}  {'old':>5}  {'new':>5}  {'delta':>6}  status")
    changed = 0
    for b in blobs:
        num = b["number"]
        old_wc = len(old_texts[num].split())
        new_wc = len(b["text"].split())
        same = old_texts[num] == b["text"]
        status = "same" if same else "voiced"
        changed += 0 if same else 1
        print(f"{num:>4}  {old_wc:>5}  {new_wc:>5}  {new_wc - old_wc:>+6}  {status}")

    print(f"\n{changed}/{len(blobs)} blobs voiced; written in-place to {chapter_path}")


if __name__ == "__main__":
    main()
