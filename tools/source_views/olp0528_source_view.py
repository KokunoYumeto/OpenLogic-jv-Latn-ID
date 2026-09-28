"""Bounded corrections to the contraposition countermodel's notation and inference."""


def repaired_olp0528_source(s: str) -> str:
    repairs = (
        (r"$\mModel{M_1} = \tuple{W, O, V}$", r"$\mModel{M} = \tuple{W, O, V}$"),
        (r"$O = \{\{w\}, \{w, w_1\}, \{w, w_1, w_2\}\}$",
         r"$O_w = \{\{w\}, \{w, w_1\}, \{w, w_1, w_2\}\}$"),
        (r"However, the $\lnot q$-admitting sphere",
         r"However, the only $\lnot q$-admitting sphere"),
        (r"$\mSat/{M}{\lnot q \lif \lnot p}[w_2]$." + "\n" + r"\end{ex}",
         r"$\mSat/{M}{\lnot q \lif \lnot p}[w_2]$. "
         r"Therefore the contrapositive counterfactual is false at $w$." + "\n" + r"\end{ex}"),
    )
    for old, new in repairs:
        assert s.count(old) == 1, old
        s = s.replace(old, new, 1)
    return s
