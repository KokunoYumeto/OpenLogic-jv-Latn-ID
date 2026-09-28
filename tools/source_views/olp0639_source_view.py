"""Bounded comparison view for the Hilbert-curve appendix."""


def repaired_olp0639_source(s: str) -> str:
    repairs = (
        (r"for each $x \in \unitsquare$:",
         r"for each $x \in \unitline$:"),
        ("So the maximum distance of any\npoint from $h$ is given by:",
         "This informal picture suggests that the maximum distance of any\npoint from $h$ should be bounded by:"),
        ("In\nother words, every point of $\\unitsquare$ lies \\emph{on} the curve. So $h$\nfills space!{}",
         "Heuristically, every point of $\\unitsquare$ lies \\emph{on} the curve, so $h$\nfills space!{} A full proof still requires control of the limiting image."),
        ("onto the plane $\\Real^2$", "into the plane $\\Real^2$"),
        ("In the\nvernacular, we want to establish the following:",
         "The following describes how the image approaches each target point; it is not the epsilon/delta criterion for continuity at each domain point:"),
        ("increasingly stretched-out, wiggly fashion.",
         "increasingly stretched-out, wiggly fashion. This informal account does not by itself establish continuity at every point of the domain."),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
