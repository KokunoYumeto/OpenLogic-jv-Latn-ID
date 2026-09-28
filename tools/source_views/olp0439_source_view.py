"""Bounded comparison view for the commented-out Rule T opening."""


def repaired_olp0439_source(s: str) -> str:
    old = r"\item \ollabel{prop:derivabilityfacts-ruleT}% \emph{Rule T}: If"
    new = r"\item \ollabel{prop:derivabilityfacts-ruleT} \emph{Rule T}: If"
    assert s.count(old) == 1
    return s.replace(old, new, 1)
