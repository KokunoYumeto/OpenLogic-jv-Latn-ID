"""Bounded comparison view for OLP-0428's mismatched chapter file ID."""


def repaired_olp0428_source(s: str) -> str:
    old = r"\olfileid{nml}{axs}{int}"
    new = r"\olfileid{nml}{prf}{int}"
    assert s.count(old) == 1
    return s.replace(old, new, 1)
