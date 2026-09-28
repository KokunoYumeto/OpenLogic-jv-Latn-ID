"""Normalize English diaereses and a bounded C/c typo in the proof note."""


def repaired_olp0546_source(s: str) -> str:
    repairs = (
        (r'na\"ive', 'naive', 1),
        (r'Na\"ive', 'Naive', 2),
        (r'$x \in c$', r'$x \in C$', 1),
    )
    for old, new, expected in repairs:
        assert s.count(old) == expected, (old, s.count(old))
        s = s.replace(old, new)
    return s
