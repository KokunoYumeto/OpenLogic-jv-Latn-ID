"""Bounded limit-stage wording and English diaeresis normalization."""


def repaired_olp0539_source(s: str) -> str:
    repairs = (
        (r'Na\"{i}ve', 'Naif'),
        (r'Na\"ive', 'Naif'),
        ("at\nthe first stage immediately after all of its !!{element}s.",
         "at\na stage later than each of its !!{element}s."),
        ("would have to first occur immediately after the stage at which it\nfirst occurred, which is absurd.",
         "would have to first occur at a stage later than the stage at which it\nfirst occurred, which is absurd."),
    )
    for old, new in repairs:
        assert s.count(old) == 1, (old, s.count(old))
        s = s.replace(old, new, 1)
    return s
