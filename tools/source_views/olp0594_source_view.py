"""Bounded Tarski--Scott naive-cardinality qualification and lexical repairs."""


def repaired_olp0594_source(s: str) -> str:
    repairs = (
        (r'na\"ive', "naive"),
        (
            "this definition fails. Any singleton set",
            "this definition fails for nonempty A. Any singleton set",
        ),
        (
            "singleton of the previous stage). So "
            + r"$\Setabs{x}{\cardeq{A}{x}}$"
            + " does\nnot exist, since it cannot have a rank.",
            "singleton of the previous stage). More generally, for any nonempty A, "
            "Cartesian products with singletons at unbounded ranks are equinumerous with A. "
            "So " + r"$\Setabs{x}{\cardeq{A}{x}}$"
            + " is not a set for nonempty A; the empty case is a set.",
        ),
        (r"\citet[chs.~9--12]{Potter2004}", r"\citet[bab~9--12]{Potter2004}"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
