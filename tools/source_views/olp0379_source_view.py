"""Bounded comparison view for the factorial example and Church fixed point."""
from __future__ import annotations


def repaired_olp0379_source(text: str) -> str:
    old_unfold = r"""\begin{align*}
  \fn{Fac} & \ident \lambd[n][\fn{IsZero}\, n\, \num{1}] \\
    & \qquad (\fn{Mult}\, n
  ((\lambd[n][\fn{IsZero} \, n \, \num 1\, (\fn{Mult}\, n\, (\fn{Fac}
    (\fn{Pred}\, n)))]) (\fn{Pred}\, n)))
\end{align*}"""
    new_unfold = r"""\begin{align*}
  \fn{Fac} & \ident \lambd[n][\fn{IsZero}\, n\, \num{1}\,
    (\fn{Mult}\, n\,
      ((\lambd[n][\fn{IsZero}\, n\, \num{1}\,
        (\fn{Mult}\, n\, (\fn{Fac}(\fn{Pred}\, n)))])
       (\fn{Pred}\, n)))]
\end{align*}"""
    repairs = (
        (
            r"\fn{Mult} \ident \lambd[ab][a (\fn{Add}\, a) 0]",
            r"\fn{Mult} \ident \lambd[ab][a (\fn{Add}\, b) \num{0}]",
        ),
        (old_unfold, new_unfold),
        (
            "$Yg\n\\equal[\\beta] g(Yg)$ but not $Yg \\bred g(Yg)$",
            r"$Y_Cg \equal[\beta] g(Y_Cg)$ but not $Y_Cg \bred g(Y_Cg)$",
        ),
    )
    for old, new in repairs:
        assert text.count(old) == 1, (old[:80], text.count(old))
        text = text.replace(old, new)
    return text
