"""Localize the Potter page locator without changing the frozen source."""


def normalized_olp0598_source(s: str) -> str:
    wrong = r"\cite[pp.~242--3]{Potter2004}"
    right = r"\cite[kaca~242--3]{Potter2004}"
    assert s.count(wrong) == 1, s.count(wrong)
    return s.replace(wrong, right, 1)
