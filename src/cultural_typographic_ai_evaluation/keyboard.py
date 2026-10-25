"""Persian keycap check: "if you are going to use the Persian alphabet on the keys of the typewriter,
at least have the decency to do it right, or don't do it at all."

Given the glyphs a design (or a generator's native-text output) puts on keys, report:
duplicate letters, Arabic look-alikes used instead of Persian letters, non-letters, and which of
the 32 Persian letters are missing. Works on declared text only; no OCR of images.
"""
import unicodedata
PERSIAN_32 = list("ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی")
CONFUSABLES = {"\u0643": "\u06a9", "\u064a": "\u06cc", "\u0649": "\u06cc", "\u0647\u0654": "\u06c0"}

def check_keys(keys, require_full_alphabet=True):
    """keys: {key_id: glyph}. Returns verdict + itemised findings."""
    if not isinstance(keys, dict): return {"verdict": "fail", "findings": [{"kind": "invalid", "evidence": "keys must be an object"}]}
    f, seen = [], {}
    for k, g in keys.items():
        if not isinstance(g, str) or len(g) == 0:
            f.append({"kind": "empty", "key": k, "evidence": f"{g!r}"}); continue
        g = unicodedata.normalize("NFC", g)
        if g in CONFUSABLES:
            f.append({"kind": "arabic_lookalike", "key": k, "evidence": f"{unicodedata.name(g[0])} used; Persian needs {unicodedata.name(CONFUSABLES[g][0])}"})
        elif g not in PERSIAN_32:
            f.append({"kind": "not_a_persian_letter", "key": k, "evidence": " ".join(f"U+{ord(ch):04X}" for ch in g)})
        seen.setdefault(g, []).append(k)
    for g, ks in seen.items():
        if len(ks) > 1: f.append({"kind": "duplicate", "key": ",".join(map(str, ks)), "evidence": f"U+{ord(g[0]):04X} appears on {len(ks)} keys"})
    missing = [ch for ch in PERSIAN_32 if ch not in seen]
    if require_full_alphabet and missing: f.append({"kind": "missing", "key": None, "evidence": " ".join(f"U+{ord(ch):04X}" for ch in missing)})
    return {"verdict": "fail" if f else "pass", "n_keys": len(keys), "n_missing": len(missing), "findings": f}
