"""Bounded countable-choice finite-union and Feferman--Levy corrections."""


def repaired_olp0597_source(s: str) -> str:
    repairs = (
        (r"\card{\bigcup_{i < n}A_n}", r"\card{\bigcup_{i < n}A_i}"),
        (
            "a countable union of countable sets has\n" + r"cardinality~$\beth_1$",
            "the uncountable set of reals " + r"$\Real$" +
            " can be a countable union of countable sets",
        ),
        (r"\citet[p.~138]{Cohen1966}", r"\citet[kaca~138]{Cohen1966}"),
        (r"\citep[p.~126]{Russell1919}", r"\citep[kaca~126]{Russell1919}"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
