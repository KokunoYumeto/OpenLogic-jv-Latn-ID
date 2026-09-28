"""Bounded comparison view for the limit explanation, formula and plot."""


def repaired_olp0635_source(s: str) -> str:
    repairs = (
        ("value of $f'(c)$ ``tends without limit''",
         "approximations to $f'(c)$ ``tend without limit''"),
        (r"\emph{trend} of $f'(c)$ as $\beta$ approaches $0$",
         r"\emph{trend} of approximations to $f'(c)$ as $\beta$ approaches $0$"),
        (r"\left(|x - c| < \delta \lif", r"\left(0 < |x - c| < \delta \lif"),
        ("$|x -\nc| < \\delta$", "$0 < |x - c| < \\delta$"),
        ("{-2/-2, -1,1, 1/1, 2/2}", "{-2/-2, -1/-1, 1/1, 2/2}"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
