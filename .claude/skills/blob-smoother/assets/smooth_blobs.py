#!/usr/bin/env python
"""Smooth a chapter JSON's blobs into a coherent narrative, editing in place.

Walks the blobs in order. Blob 1 is the untouched anchor. For every later blob it
makes ONE synchronous OpenRouter call whose input is the chapter outline plus a
sliding window of consecutive passages (the previous up-to-two, already-edited,
plus the target). The call edits ONLY the last passage so it flows from and stays
consistent with the ones before it, preferring cuts over additions and never
growing the passage. The revised text is written back into the blob in place.

Usage:
    python smooth_blobs.py <path-to-chapter.json>

Reads OPENROUTER_API_KEY from the environment or this folder's .env. Stdlib only.
"""
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# Random model per call, with replacement.
MODELS = [
    "nvidia/nemotron-3-ultra-550b-a55b",
    "anthropic/claude-sonnet-4.6",
    "openai/o3",
    "thinkingmachines/inkling",
]

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MAX_ATTEMPTS = 4
TIMEOUT = 180
MAX_TOKENS = 2000
TEMPERATURE = 0.35  # Cold: careful reconciliation.
WINDOW = 3          # Target passage plus up to two preceding.
BACKOFF_BASE = 5    # Exponential retry base seconds.
BACKOFF_MAX = 60    # Retry sleep ceiling seconds.


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


def words(text):
    return len(text.split())


def build_messages(target, window, outline, context, orig_wc):
    """window: list of (number, text, is_target) in order; only the last is the target."""
    ctx = " ".join(context) if isinstance(context, list) else str(context)
    tags = ", ".join(target.get("tags", []))
    system = (
        "You are an editor smoothing one passage of continuous first-person fiction so a "
        "sequence of separately-written passages reads as one coherent narrative.\n"
        f"Chapter outline (the plot spine, for reference only; do not copy from it): {outline}\n"
        f"Story context: {ctx}\n"
        "You are given an ordered set of consecutive passages. Every passage EXCEPT THE LAST "
        "is already finalized and FIXED: treat it as read-only reference for continuity. "
        "Edit ONLY the last passage so it flows from and stays consistent with the one(s) before it.\n"
        "Rules:\n"
        "- Reconcile only real conflicts with what precedes it: contradictory names, locations, "
        "physical descriptions, or established facts; jarring stylistic jumps; and vocabulary "
        "repeated from the previous passage.\n"
        "- Strongly PREFER cutting or changing text over adding. Add a word or a line only as a "
        "last resort, and NEVER introduce new details, characters, objects, or events.\n"
        "- Do NOT erase unique or idiosyncratic details. Fix only serious conflicts that cannot "
        "be reconciled; leave everything else alone.\n"
        f"- Preserve the last passage's form: its mode is '{target.get('mode', '')}' and its type "
        f"is '{target.get('type', '')}'. Do not, for example, turn dialogue into narration or an "
        "action beat into description.\n"
        f"- LENGTH LIMIT (STRICT): the last passage is {orig_wc} words. Your revision MUST be "
        f"{orig_wc} words or fewer, and under 200 words in every case. Exceeding this is a hard "
        "failure and the result is discarded. When unsure, cut. Do not pad, restate, or explain.\n"
        "- Keep it first-person and in the same archaic voice.\n"
        "CRITICAL OUTPUT FORMAT: return ONLY the revised last passage itself, beginning "
        "immediately with its first word. No preamble, no 'Here is', no title, no labels, no "
        "surrounding quotation marks, no commentary, no notes, no word count. Nothing whatsoever "
        "before or after the prose."
    )
    lines = ["Here are the consecutive passages, in order. Edit ONLY the final one.\n"]
    for number, text, is_target in window:
        label = "EDIT THIS - the last passage" if is_target else "FIXED - reference only"
        lines.append(f"----- Passage {number} ({label}) -----\n{text}\n")
    lines.append(
        f"\nThe passage to edit has mode '{target.get('mode', '')}', type "
        f"'{target.get('type', '')}', and tags: {tags}. Preserve that mode and type. "
        "Return only the revised final passage, prose only."
    )
    user = "\n".join(lines)
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def call_model(api_key, model, messages):
    body = json.dumps({
        "model": model,
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
            "X-Title": "CorpLore blob-smoother",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return (data["choices"][0]["message"].get("content") or "").strip()


def smooth_one(api_key, target, window, outline, context):
    """Return (new_text, model, status). On failure new_text is None (keep original)."""
    orig_wc = words(target.get("text", ""))
    messages = build_messages(target, window, outline, context, orig_wc)
    last_err = ""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        model = random.choice(MODELS)
        retry_after = None
        try:
            text = call_model(api_key, model, messages)
            if not text:
                last_err = "empty content"
            elif words(text) > orig_wc:
                last_err = f"over length ({words(text)}>{orig_wc}w)"
            else:
                return text, model, "ok"
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}"
            if e.headers:
                retry_after = e.headers.get("Retry-After")
        except Exception as e:
            last_err = repr(e)
        if attempt < MAX_ATTEMPTS:
            # Honor Retry-After, else exponential backoff.
            if retry_after and str(retry_after).isdigit():
                wait = float(retry_after)
            else:
                wait = BACKOFF_BASE * (2 ** (attempt - 1))
            time.sleep(min(wait, BACKOFF_MAX))
    return None, "", f"KEPT ({last_err})"


def main():
    positional = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not positional:
        sys.exit("Usage: python smooth_blobs.py <chapter.json>")

    path = Path(positional[0])
    doc = json.loads(path.read_text(encoding="utf-8"))
    chapter = doc["chapter"]
    outline = chapter.get("outline", "")
    context = chapter.get("context", [])
    blobs = chapter["blobs"]

    if len(blobs) < 2:
        sys.exit("Need at least 2 blobs with text to smooth.")

    api_key = load_api_key()
    print(f"{'blob':>4}  {'orig':>4}  {'new':>4}  {'status':<22}  model")

    results = []
    # Blob 0 is the untouched anchor.
    for i in range(1, len(blobs)):
        target = blobs[i]
        num = target.get("number", i + 1)
        orig_wc = words(target.get("text", ""))
        if not target.get("text", "").strip():
            print(f"{num:>4}  {orig_wc:>4}  {'-':>4}  {'SKIP (empty text)':<22}")
            results.append((num, "skip"))
            continue

        start = max(0, i - (WINDOW - 1))
        window = [
            (blobs[j].get("number", j + 1), blobs[j].get("text", ""), j == i)
            for j in range(start, i + 1)
        ]
        new_text, model, status = smooth_one(api_key, target, window, outline, context)
        if new_text is not None:
            blobs[i]["text"] = new_text  # feeds forward into the next window
            # Flush after each edit so a crash is resumable.
            path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        new_wc = words(blobs[i].get("text", ""))
        print(f"{num:>4}  {orig_wc:>4}  {new_wc:>4}  {status:<22}  {model}")
        results.append((num, status))

    kept = [n for n, s in results if s.startswith("KEPT")]
    ok = sum(1 for _, s in results if s == "ok")
    print(f"\nSmoothed {ok}/{len(results)} editable blobs in {path}")
    if kept:
        print(f"KEPT original (no change) for blobs: {kept}  -> re-run to retry just these.")


if __name__ == "__main__":
    main()
