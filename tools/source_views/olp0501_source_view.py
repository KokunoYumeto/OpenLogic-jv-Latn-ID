"""Repair the local entailment proof and localize prose inside an equation."""


def repaired_olp0501_source(s: str) -> str:
    old = r"""  \item Suppose $\mSat{M}{\Gamma}$. Since $\Gamma \Entails !A$, we
    know that if $\mSat{M}{\Gamma}[w]$, then $\mSat{M}{!A}[w]$. Since
    $\mSat{M}{\Gamma}[u]$ for all every $u \in W$,
    $\mSat{M}{\Gamma}[w]$. Hence $\mSat{M}{!A}[w]$."""
    new = r"""  \item Suppose $\mSat{M}{\Gamma}[w]$. Since $\Gamma \Entails !A$,
    by the definition of entailment, from $\mSat{M}{\Gamma}[w]$ we
    obtain $\mSat{M}{!A}[w]$."""
    assert s.count(old) == 1
    s = s.replace(old, new, 1)
    assert s.count(r"\text{ and}") == 1
    return s.replace(r"\text{ and}", r"\text{ lan}", 1)
