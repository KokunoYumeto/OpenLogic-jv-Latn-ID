"""Normalize the source-language diaeresis in the cumulative account."""


def normalized_olp0534_source(s: str) -> str:
    old = r'Na\"ive'
    assert s.count(old) == 1
    return s.replace(old, 'Naif', 1)
