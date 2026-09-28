"""Bounded Methods/Proofs file-identity repair."""


def repaired_olp0605_source(s: str) -> str:
    wrong = r"\olfileid{mod}{prf}{def}"
    right = r"\olfileid{mth}{prf}{def}"
    assert s.count(wrong) == 1, s.count(wrong)
    return s.replace(wrong, right, 1)
