#!/usr/bin/env python
"""Fill each blob's text+model in a chapter JSON via parallel OpenRouter calls.

Usage:
    python write_blobs.py <path-to-chapter.json> [--only-empty]

Reads OPENROUTER_API_KEY from the environment or from assets/.env. Stdlib only.
"""
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Random model per blob, with replacement.
MODELS = [
    "nvidia/nemotron-3-ultra-550b-a55b",
    "anthropic/claude-sonnet-4.6",
    "openai/o3",
    "thinkingmachines/inkling",
]

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MAX_ATTEMPTS = 3
TIMEOUT = 180
MAX_TOKENS = 2000
TEMPERATURE = 1.0


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


def build_messages(blob, context):
    ctx = " ".join(context) if isinstance(context, list) else str(context)
    tags = ", ".join(blob.get("tags", []))
    system = (
        "You are writing one small, self-contained passage of continuous fiction "
        "that will slot into a larger chapter.\n"
        f"Story context: {ctx}\n"
        f"Write the passage in this form: {blob.get('mode', '')} - {blob.get('type', '')}.\n"
        f"Weave in these details and features: {tags}.\n"
        "Your piece MUST be under 200 words.\n"
        "Output ONLY the prose itself: no title, no framing, no preamble, no notes, "
        "no word count."
    )
    user = f"Write the following small piece of fiction: {blob.get('prompt', '')}"
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
            "X-Title": "CorpLore blob-writer",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return (data["choices"][0]["message"].get("content") or "").strip()


def write_one(api_key, index, blob, context):
    """Return (index, text, model, status). On persistent failure text/model are ''."""
    messages = build_messages(blob, context)
    last_err = ""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        model = random.choice(MODELS)
        try:
            text = call_model(api_key, model, messages)
            if text:
                return index, text, model, "ok"
            last_err = "empty content"
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}"
        except Exception as e:
            last_err = repr(e)
        time.sleep(1.5 * attempt)
    return index, "", "", f"FAILED ({last_err})"


def main():
    positional = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if not positional:
        sys.exit("Usage: python write_blobs.py <chapter.json> [--only-empty]")
    only_empty = "--only-empty" in flags

    path = Path(positional[0])
    doc = json.loads(path.read_text(encoding="utf-8"))
    chapter = doc["chapter"]
    context = chapter.get("context", [])
    blobs = chapter["blobs"]

    targets = [
        (i, b) for i, b in enumerate(blobs)
        if b.get("prompt", "").strip()
        and not (only_empty and b.get("text", "").strip())
    ]
    if not targets:
        sys.exit("No blobs to write (need non-empty prompts; --only-empty skips filled blobs).")

    api_key = load_api_key()
    results = []
    with ThreadPoolExecutor(max_workers=len(targets)) as pool:
        futures = [pool.submit(write_one, api_key, i, b, context) for i, b in targets]
        for f in futures:
            results.append(f.result())

    for index, text, model, status in results:
        if status == "ok":
            blobs[index]["text"] = text
            blobs[index]["model"] = model

    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Summary, in blob order.
    results.sort(key=lambda r: r[0])
    print(f"{'blob':>4}  {'words':>5}  {'status':<10}  model")
    failed = []
    for index, text, model, status in results:
        num = blobs[index].get("number", index + 1)
        wc = len(text.split())
        print(f"{num:>4}  {wc:>5}  {status:<10}  {model}")
        if status != "ok":
            failed.append(num)
    print(f"\nWrote {len(results) - len(failed)}/{len(results)} blobs to {path}")
    if failed:
        print(f"FAILED blobs: {failed}  -> re-run with --only-empty to retry just these.")


if __name__ == "__main__":
    main()
