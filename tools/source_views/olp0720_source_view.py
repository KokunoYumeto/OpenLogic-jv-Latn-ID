"""Comparison-only normalization of an English word's accent macro for native spelling.

This is translation typography, not a mathematical defect or frozen-source edit.
"""
def repaired_olp0720_source(s: str) -> str:
    wrong = r'Na\"ive'
    assert s.count(wrong) == 1
    return s.replace(wrong, "Naive", 1)
