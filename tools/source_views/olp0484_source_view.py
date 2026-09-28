"""Bounded comparison view for the modal-free definition's agent scope."""


def repaired_olp0484_source(s: str) -> str:
    old = r"does not contain $\Knows_a$, we say it"
    new = r"does not contain $\Knows_a$ for any agent, we say it"
    assert s.count(old) == 1
    return s.replace(old, new, 1)
