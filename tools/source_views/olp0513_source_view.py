"""Bounded repairs for the prose describing the correct tableau rule table."""


def repaired_olp0513_source(s: str) -> str:
    start = s.index("For the conditional~")
    end = s.index("\n\nThe $\\TRule{\\lif}{\\False}$ rule", start)
    para = s[start:end]
    repairs = (
        (r"\TRule{\lif}{\True}", r"\TRule{\True}{\lif}"),
        (r"\sFmla{\True}{!A}[\sigma.{*}]", r"\sFmla{\False}{!A}[\sigma.{*}]"),
        (r"\sFmla{\False}{!B}[\sigma.{*}]", r"\sFmla{\True}{!B}[\sigma.{*}]"),
        (r"\sFmla{\True}{!A}[\sigma]", r"\sFmla{\False}{!A}[\sigma]"),
        (r"\sFmla{\False}{!B}[\sigma]", r"\sFmla{\True}{!B}[\sigma]"),
    )
    for old, new in repairs:
        assert para.count(old) == 1
        para = para.replace(old, new, 1)
    s = s[:start] + para + s[end:]
    assert s.count(r"\TRule{\lif}{\False}") == 1
    s = s.replace(r"\TRule{\lif}{\False}", r"\TRule{\False}{\lif}", 1)
    old = "(and not at any other world)"
    new = "(the rule introduces them at this prefix, without excluding truth at other worlds)"
    assert s.count(old) == 1
    s = s.replace(old, new, 1)
    for old, new in (
        (r"\text{and}", r"\text{lan}"),
        (r"\text{$\sigma.{*}$ is used}", r"\text{$\sigma.{*}$ wis digunakake}"),
        (r"\text{$\sigma.n$ is new}", r"\text{$\sigma.n$ anyar}"),
    ):
        assert s.count(old) == 2
        s = s.replace(old, new)
    return s
