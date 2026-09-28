"""Bounded source comparison for primitive-recursion indexing and TeX notation."""
from __future__ import annotations


def repaired_olp0378_source(text: str) -> str:
    repairs = (
        (r"$F$, $G_0$, \dots, $G_k$", r"$F$, $G_0$, \dots, $G_{k-1}$"),
        ("Then $H$ is !!{lambda definable}.", "Then $h$ is !!{lambda definable}."),
        (
            r"h(x_1, \dots, x_n, y+1) & = h(x_1, \dots, x_n, y, h(x_1, \dots, x_n, y)).",
            r"h(x_1, \dots, x_n, y+1) & = g(x_1, \dots, x_n, y, h(x_1, \dots, x_n, y)).",
        ),
        ("application of the function $h$ $y$ times", "application of the function $g$ $y$ times"),
        (
            "    & \\redone\n"
            "    \\tuple{\\fn{Succ} (\\fn{Fst}\\, \\tuple{\\num{m}, \\num{h(n,m)}}),\\\\\n"
            "      & \\qquad (G \\, \\num{n} (\\fn{Fst}\\, \\tuple{\\num{m}, \\num{h(n,m)}}) (\\fn{Snd}\\, \\tuple{\\num{m}, \\num{h(n,m)}}))}\\\\",
            "    & \\redone \\tuple{\\fn{Succ} (\\fn{Fst}\\, \\tuple{\\num{m}, \\num{h(n,m)}}),\n"
            "      (G \\, \\num{n} (\\fn{Fst}\\, \\tuple{\\num{m}, \\num{h(n,m)}}) (\\fn{Snd}\\, \\tuple{\\num{m}, \\num{h(n,m)}}))}\\\\",
        ),
        (
            r"(\lambd[p].\tuple{\fn{Succ} (\fn{Fst}\, p), (G\, x\,",
            r"(\lambd[p][\tuple{\fn{Succ} (\fn{Fst}\, p), (G\, x\,",
        ),
        (
            r"(\fn{Fst}\, p)\, (\fn{Snd}\, p))}) \tuple{\num{0}, F x})]]",
            r"(\fn{Fst}\, p)\, (\fn{Snd}\, p))}]) \tuple{\num{0}, F x})]]",
        ),
        (
            r"(\lambd[p].\tuple{\fn{Succ} (\fn{Fst}\, p), (G \,\num n\,",
            r"(\lambd[p][\tuple{\fn{Succ} (\fn{Fst}\, p), (G \,\num n\,",
        ),
        (
            r"(\fn{Fst}\, p) (\fn{Snd}\, p))})}_{D_n}",
            r"(\fn{Fst}\, p) (\fn{Snd}\, p))}])}_{D_n}",
        ),
    )
    for old, new in repairs:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    return text
