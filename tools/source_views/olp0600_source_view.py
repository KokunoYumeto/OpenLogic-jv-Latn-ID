"""Bounded Vitali rotation-group, index, and invariant-measure repairs."""


def repaired_olp0600_source(s: str) -> str:
    repairs = (
        (
            "by " + r"\emph{rational}" + "\nradian values between",
            "by angles that are " + r"\emph{rational}" +
            " multiples of a full turn, represented between",
        ),
        (
            "Every element has an inverse. Where",
            "Every element has an inverse. The identity is its own inverse. Where",
        ),
        (
            "rotations by rational radian\nvalues in",
            "rotations by rational multiples of a full turn in",
        ),
        (
            "by a rational-valued rotation about the origin",
            "by a rotation through a rational multiple of a full turn about the origin",
        ),
        (r"\emph{ iff }", r"\emph{ yèn lan mung yèn }"),
        (r"\rho \in R_1", r"\rho \in \rotationsgroup_1"),
        (
            "Details here\nare not essential, except that the function "
            + r"$\mu$" + " must obey the\nprinciple of countable additivity:",
            "We use a nonnegative measure on a rotation-invariant domain. "
            "Other details are not essential, except that the function "
            + r"$\mu$" + " must obey the\nprinciple of countable additivity:",
        ),
        (
            "To say that a set is ``unmeasurable'' is to\nsay that no measure can be suitably assigned.",
            "To say a set is ``unmeasurable'' is to say it is outside the domain of the measure under discussion.",
        ),
        (r"\citet[Theorem 5.2]{Wagon2016}", r"\citet[Téoréma 5.2]{Wagon2016}"),
        (r"\citet[p.~3]{Weston2003}", r"\citet[kaca~3]{Weston2003}"),
        (r"\citet[Theorem 2.1]{Wagon2016}", r"\citet[Téoréma 2.1]{Wagon2016}"),
        (r"\cite[p.~16]{Weston2003}", r"\cite[kaca~16]{Weston2003}"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    wrong = r"\rho \in C"
    right = r"\rho \in \rotationsgroup"
    assert s.count(wrong) == 1, s.count(wrong)
    s = s.replace(wrong, right, 1)
    wrong = r"\rho \in" + "\n" + "C"
    assert s.count(wrong) == 1, s.count(wrong)
    return s.replace(wrong, right, 1)
