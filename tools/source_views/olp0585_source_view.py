"""Normalize source-only diaeresis in translated Naive Comprehension prose."""


def normalized_olp0585_source(s: str) -> str:
    wrong = r'Na\"ive Comprehension'
    assert s.count(wrong) == 3, s.count(wrong)
    return s.replace(wrong, "Komprehensi Naif")
