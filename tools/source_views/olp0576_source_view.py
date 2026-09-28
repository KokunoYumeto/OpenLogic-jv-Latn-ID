"""Bounded corrections to two ordinal-addition displayed equalities."""


def repaired_olp0576_source(s: str) -> str:
    repairs = (
        (
            r"\disjointsum (\{0\} \times \{1\})",
            r"\cup (\{0\} \times \{1\})",
        ),
        (
            r"\cup \{0\}, \rlexless}",
            r"\cup \emptyset, \rlexless}",
        ),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
