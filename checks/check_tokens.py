"""The design system's rules, checked rather than trusted.

1. Every colour token exists in both themes.
2. Every text colour meets 4.5:1 on each background it is used on, in both
   themes (WCAG AA for normal text). The pairs are listed below; tones and
   stages are paired by name, so a new one is checked without being listed.
3. Components use tokens only: no raw colour outside the two token blocks.

Standard library only. Run: python3 checks/check_tokens.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

CSS = Path(__file__).resolve().parent.parent / "styles.css"
MINIMUM = 4.5
COLOUR_PREFIXES = ("--color-", "--tone-", "--stage-")

# Text on a background, as the components use them. Add a line when a
# component puts a text colour on a background not already here.
PAIRS = [
    ("--color-text", "--color-bg"),
    ("--color-text", "--color-surface"),
    ("--color-text", "--color-surface-raised"),
    ("--color-text-dim", "--color-bg"),
    ("--color-text-dim", "--color-surface"),
    ("--color-text-dim", "--color-surface-raised"),
    ("--color-link", "--color-bg"),
    ("--color-link", "--color-surface"),
    ("--color-accent-hover", "--color-bg"),
    ("--color-accent-hover", "--color-surface"),
    ("--color-on-accent", "--color-accent"),
    ("--color-on-accent", "--color-accent-hover"),
    ("--color-feature-text", "--color-feature-bg"),
    ("--color-feature-dim", "--color-feature-bg"),
    ("--color-feature-accent", "--color-feature-bg"),
]


def block(css: str, selector: str) -> dict[str, str]:
    match = re.search(re.escape(selector) + r"\s*\{(.*?)\n\}", css, re.S)
    if not match:
        sys.exit(f"styles.css has no {selector} block")
    body = re.sub(r"/\*.*?\*/", "", match.group(1), flags=re.S)
    return dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", body))


def luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    channels = [int(h[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(a: str, b: str) -> float:
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def pairs(tokens: dict[str, str]) -> list[tuple[str, str]]:
    found = list(PAIRS)
    for name in tokens:
        if m := re.fullmatch(r"--tone-([\w]+)-bg", name):
            found.append((f"--tone-{m.group(1)}-text", name))
        if re.fullmatch(r"--stage-\d+", name):
            found.append((f"{name}-text", name))
    return found


def main() -> int:
    css = CSS.read_text()
    light = block(css, ":root")
    dark = block(css, '[data-theme="dark"]')
    failures: list[str] = []

    colours = {n for n in light if n.startswith(COLOUR_PREFIXES)}
    for name in sorted(colours ^ {n for n in dark if n.startswith(COLOUR_PREFIXES)}):
        failures.append(f"{name} is defined in one theme only")

    checked = 0
    for theme, overrides in (("light", {}), ("dark", dark)):
        tokens = {**light, **overrides}
        for text, back in pairs(tokens):
            if text not in tokens or back not in tokens:
                failures.append(f"{theme}: {text} on {back}: a token is missing")
                continue
            ratio = contrast(tokens[text], tokens[back])
            checked += 1
            if ratio < MINIMUM:
                failures.append(
                    f"{theme}: {text} {tokens[text]} on {back} {tokens[back]} is {ratio:.2f}:1, needs {MINIMUM}:1"
                )

    dark_block = re.search(r'^\[data-theme="dark"\]\s*\{.*?\n\}', css, re.S | re.M)
    components = css[dark_block.end() :]
    for raw in sorted(set(re.findall(r"#[0-9A-Fa-f]{3,8}\b|rgba?\(|hsla?\(", components))):
        failures.append(f"a raw colour ({raw}) is used outside the token blocks; use a token")

    for line in failures:
        print(f"FAIL  {line}")
    print(f"{checked} text pairs checked across both themes; {len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
