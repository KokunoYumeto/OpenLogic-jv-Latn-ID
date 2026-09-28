"""Normalize the three source-language diaereses in the Frege appendix."""


def normalized_olp0536_source(s: str) -> str:
    repairs = ((r'Na\"{i}ve', 1), (r'Na\"ive', 2))
    for old, count in repairs:
        assert s.count(old) == count, (old, s.count(old))
        s = s.replace(old, 'Naif')
    return s
