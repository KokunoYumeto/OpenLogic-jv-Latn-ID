"""Bounded range-word repair and glossary-token plural normalization."""


def repaired_olp0551_source(s: str) -> str:
    old_plural = '!!{bijection}s'
    old_range = "as $f$'s domain\nis $B_{{b_2}}$."
    assert s.count(old_plural) == 1, s.count(old_plural)
    assert s.count(old_range) == 1, s.count(old_range)
    s = s.replace(old_plural, '!!{bijection}', 1)
    return s.replace(old_range, "as $f$'s range\nis $B_{{b_2}}$.", 1)
