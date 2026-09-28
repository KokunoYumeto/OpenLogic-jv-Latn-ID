"""Bounded comparison view for nonstandard arithmetic model and block claims."""


def repaired_olp0653_source(s: str) -> str:
    repairs = (
        ("interpret the non-logical constants of\n$\\Lang{L}$ as",
         "interpret the non-logical symbols of\n$\\Lang{L_N}$ as"),
        (r"\Assign{<}{M} \subseteq M^2$",
         r"\Assign{<}{M} \subseteq \Domain{M}^2$"),
        ("impossible because it implies $x \\approx y$, so $x \\prec\n  y$.",
         "impossible because it implies $x \\approx y$, so $x^* \\prec\n  y$."),
        ("each block $[x]$ forms a doubly infinite chain",
         "each non-standard block $[x]$ forms a doubly infinite chain"),
        ("if $x \\prec y$\n  then the block of $x$ is less than the block of $y$.",
         "if $x \\prec y$ and the blocks are distinct, then the block of $x$ is less than the block of $y$."),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
