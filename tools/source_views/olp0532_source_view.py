"""Normalize source-language diaeresis and prose control-space in OLP-0532.

This is a lexical TeX adaptation, not a change to the frozen argument.
"""


def normalized_olp0532_source(s: str) -> str:
    pairs = (
        (r'na\"{i}ve', 'naif', 2),
        (r'na\"ive', 'naif', 1),
        (r'Na\"{i}ve', 'Naif', 2),
        (r'\ ', ' ', 1),
    )
    for old, new, expected in pairs:
        assert s.count(old) == expected, (old, s.count(old))
        s = s.replace(old, new)
    return s
