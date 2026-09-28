"""Normalize an English TeX accent command for Javanese orthography QA."""


def normalized_olp0568_source(s: str) -> str:
    old = r'Na\"ive Comprehension'
    new = 'Komprehensi Naif'
    assert s.count(old) == 1, s.count(old)
    return s.replace(old, new, 1)
