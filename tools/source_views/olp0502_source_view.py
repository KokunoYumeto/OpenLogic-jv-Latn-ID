"""Clarify topology inclusions, model quantification and interior notation."""


def repaired_olp0502_source(s: str) -> str:
    assert s.count(r"\subset \Prop{X}{!B}") == 2
    s = s.replace(r"\subset \Prop{X}{!B}", r"\subseteq \Prop{X}{!B}")
    old = r"!B$ iff $\Prop{X}{!A} \subseteq \Prop{X}{!B}$? We require"
    new = r"!B$ iff $\Prop{X}{!A} \subseteq \Prop{X}{!B}$ for every topological model? We require"
    assert s.count(old) == 1
    s = s.replace(old, new, 1)
    old = r"""  Here, $\Interior{V}$ is the function that maps a set $V \subseteq X$
  to its \emph{interior}, that is, the union of all open sets it
  contains. In other words,"""
    new = r"""  Here, $\Interior{V}$ denotes the result for a set $V \subseteq X$,
  its \emph{interior}, that is, the union of all open sets it
  contains. In other words,"""
    assert s.count(old) == 1
    s = s.replace(old, new, 1)
    assert s.count(r"\text{ and }") == 1
    return s.replace(r"\text{ and }", r"\text{ lan }", 1)
