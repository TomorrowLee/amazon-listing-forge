#!/usr/bin/env python3
"""Offline structural checks. This is not a compliance or claim verifier."""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


def inspect(data, title_limit=75, highlights_limit=125, search_terms_max_bytes=None):
    issues = []
    metrics = {}

    def issue(level, field, message):
        issues.append(dict(level=level, field=field, message=message))

    if not isinstance(data, dict):
        return {"metrics": {}, "issues": [dict(level="error", field="$", message="Expected a JSON object.")], "structural_pass": False}
    for field in ("title", "item_highlights", "description", "search_terms"):
        value = data.get(field, "")
        if not isinstance(value, str):
            issue("error", field, "Expected a string.")
            continue
        metrics[field] = {"characters": len(value), "utf8_bytes": len(value.encode("utf-8"))}
        if field == "title" and not value.strip():
            issue("error", field, "A non-empty title is required by this input format.")
        limit = {"title": title_limit, "item_highlights": highlights_limit}.get(field)
        if limit is not None and len(value) > limit:
            issue("error", field, f"{len(value)} characters exceeds the configured limit of {limit}.")
        if value != value.strip() or re.search(r"[\r\n\t]", value) and field in ("title", "item_highlights", "search_terms"):
            issue("warning", field, "Review leading/trailing whitespace or line breaks.")
        if field == "search_terms" and search_terms_max_bytes is not None and len(value.encode("utf-8")) > search_terms_max_bytes:
            issue("error", field, f"UTF-8 bytes exceed the configured limit of {search_terms_max_bytes}.")

    bullets = data.get("bullets", [])
    if not isinstance(bullets, list) or any(not isinstance(x, str) for x in bullets):
        issue("error", "bullets", "Expected a list of strings.")
        bullets = []
    metrics["bullets"] = [{"characters": len(x), "utf8_bytes": len(x.encode("utf-8"))} for x in bullets]
    seen = set()
    for i, bullet in enumerate(bullets, 1):
        field = f"bullets[{i}]"
        normalized = " ".join(bullet.lower().split())
        if not normalized:
            issue("error", field, "Empty bullet.")
        if normalized in seen:
            issue("warning", field, "Duplicate bullet; each point should answer a distinct question.")
        seen.add(normalized)
        if any(c in bullet for c in "™®©") or re.search("[\U0001F300-\U0001FAFF\u2600-\u27BF]", bullet):
            issue("warning", field, "Review trademark symbols, special characters or emoji against current rules.")
        if re.search(r"https?://|www\.|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", bullet):
            issue("warning", field, "Review external links or contact information.")
        words = sorted(set(re.findall(r"\b(?:warranty|guarantee|authentic|free|clean)\b", bullet, flags=re.I)))
        if words:
            issue("review", field, "Seller-reported risk terms, not universal bans: " + ", ".join(words) + ". Check context and current category policy.")
    title = data.get("title", "")
    if isinstance(title, str):
        stopwords = {"a", "an", "the", "and", "or", "of", "for", "to", "in", "on", "with", "by"}
        repeated = [word for word, count in Counter(re.findall(r"[a-z0-9]+", title.lower())).items() if count > 2 and word not in stopwords]
        if repeated:
            issue("warning", "title", "Review repeated tokens (heuristic): " + ", ".join(repeated))
    return {"metrics": metrics, "issues": issues, "structural_pass": not any(x["level"] == "error" for x in issues)}


def positive_int(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("Limit must be positive.")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--title-limit", type=positive_int, default=75)
    parser.add_argument("--highlights-limit", type=positive_int, default=125)
    parser.add_argument("--search-terms-max-bytes", type=positive_int, default=None)
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=True), file=sys.stderr)
        return 2
    result = inspect(data, args.title_limit, args.highlights_limit, args.search_terms_max_bytes)
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if result["structural_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
