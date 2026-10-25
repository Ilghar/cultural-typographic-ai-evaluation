"""Deterministic Persian-script text linter (stdlib only). ilghar.studio

Rules are codepoint-level and do not judge language quality:
  PS001 Arabic yeh/alef-maksura (U+064A/U+0649) where Persian yeh U+06CC expected
  PS002 Arabic kaf U+0643 where Persian keheh U+06A9 expected
  PS003 ZWNJ misuse: doubled, at word edge, next to space, or after a non-joining letter
  PS004 Bidi control characters (embeddings/overrides/isolates, LRM/RLM) flagged
  PS005 Mixed digit sets in one field (ASCII / Arabic-Indic / Extended Arabic-Indic)
  PS006 Missing ZWNJ heuristic: "می"/"نمی" prefix joined directly to a verb stem
Usage: python -m cultural_typographic_ai_evaluation.script_lint FILE.json [--json] [--fields a,b]
Exit 0 = clean, 1 = findings, 2 = input error.
"""
import argparse, json, re, sys, unicodedata

ZWNJ = "\u200c"
BIDI = {"\u200e": "LRM", "\u200f": "RLM", "\u061c": "ALM", "\u202a": "LRE", "\u202b": "RLE",
        "\u202c": "PDF", "\u202d": "LRO", "\u202e": "RLO", "\u2066": "LRI", "\u2067": "RLI",
        "\u2068": "FSI", "\u2069": "PDI"}
# letters that never join to the following letter: ZWNJ after them is redundant
NON_JOINING = set("اآأإدذرزژوؤۀة")
DIGITS = {"ascii": "0123456789", "arabic_indic": "٠١٢٣٤٥٦٧٨٩", "persian": "۰۱۲۳۴۵۶۷۸۹"}
ARABIC_LETTER = re.compile(r"[\u0620-\u064a\u066e-\u06d3\u06fa-\u06ff]")
MI_JOINED = re.compile(r"(?<![\u0600-\u06ff\u200c])(ن?م[یي])(?=[\u0622-\u064a\u067e-\u06cc]{2,})")

def _f(rule, pos, msg):
    return {"rule": rule, "offset": pos, "message": msg}

def lint_text(text):
    out = []
    for i, ch in enumerate(text):
        if ch in "\u064a\u0649":
            out.append(_f("PS001", i, f"{unicodedata.name(ch)} U+{ord(ch):04X}; Persian uses U+06CC"))
        elif ch == "\u0643":
            out.append(_f("PS002", i, "ARABIC LETTER KAF U+0643; Persian uses U+06A9"))
        elif ch in BIDI:
            out.append(_f("PS004", i, f"bidi control {BIDI[ch]} U+{ord(ch):04X}"))
        elif ch == ZWNJ:
            prev = text[i - 1] if i else ""
            nxt = text[i + 1] if i + 1 < len(text) else ""
            if prev == ZWNJ:
                continue  # run already reported once at its first ZWNJ
            if nxt == ZWNJ:
                out.append(_f("PS003", i, "repeated ZWNJ"))
            elif not prev or not nxt or prev.isspace() or nxt.isspace():
                out.append(_f("PS003", i, "ZWNJ at word edge or beside whitespace"))
            elif prev in NON_JOINING:
                out.append(_f("PS003", i, f"redundant ZWNJ after non-joining {unicodedata.name(prev)}"))
            elif not ARABIC_LETTER.match(prev) or not ARABIC_LETTER.match(nxt):
                out.append(_f("PS003", i, "ZWNJ not between Arabic-script letters"))
    sets = sorted(k for k, ds in DIGITS.items() if any(d in text for d in ds))
    if len(sets) > 1:
        out.append(_f("PS005", 0, "mixed digit sets: " + ", ".join(sets)))
    for m in MI_JOINED.finditer(text):
        out.append(_f("PS006", m.start(), f"'{m.group(1)}' prefix joined without ZWNJ (heuristic; verify)"))
    return sorted(out, key=lambda f: (f["offset"], f["rule"]))

def _strings(obj, path=""):
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k in sorted(obj):
            yield from _strings(obj[k], f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for n, v in enumerate(obj):
            yield from _strings(v, f"{path}[{n}]")

def lint_document(doc, fields=None):
    findings = []
    for path, s in _strings(doc):
        leaf = re.sub(r"\[\d+\]", "", path).split(".")[-1]
        if fields and leaf not in fields:
            continue
        if not ARABIC_LETTER.search(s) and not any(c in BIDI for c in s):
            continue
        for f in lint_text(s):
            findings.append({"path": path, **f})
    counts = {}
    for f in findings:
        counts[f["rule"]] = counts.get(f["rule"], 0) + 1
    return {"findings": findings, "counts": dict(sorted(counts.items())), "clean": not findings}

def main(argv=None):
    ap = argparse.ArgumentParser(prog="script_lint", description=__doc__.splitlines()[0])
    ap.add_argument("file"); ap.add_argument("--json", action="store_true")
    ap.add_argument("--fields", help="comma-separated leaf keys to lint (default: all strings)")
    a = ap.parse_args(argv)
    try:
        with open(a.file, encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr); return 2
    r = lint_document(doc, set(a.fields.split(",")) if a.fields else None)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        for f in r["findings"]:
            print(f"{a.file}:{f['path']}@{f['offset']} {f['rule']} {f['message']}")
        print(f"{len(r['findings'])} finding(s)")
    return 0 if r["clean"] else 1

if __name__ == "__main__":
    sys.exit(main())
