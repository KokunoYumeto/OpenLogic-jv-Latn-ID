"""Bounded comparison view for fresh-index and right-existential repairs."""


def repaired_olp0683_source(s: str) -> str:
    repairs = (
        (r"\Axiom$!B^k, !C^{k+1}, \Pi \fCenter \Lambda$",
         r"\Axiom$!B^{k+1}, !C^{k+2}, \Pi \fCenter \Lambda$"),
        (r"\Axiom$\Pi \fCenter \Lambda, !B^k$",
         r"\Axiom$\Pi \fCenter \Lambda, !B^{k+1}$"),
        (r"\Axiom$\Pi \fCenter \Lambda, !C^k$",
         r"\Axiom$\Pi \fCenter \Lambda, !C^{k+1}$"),
        (r"\Axiom$!B(c)^k, \Pi \fCenter \Lambda$",
         r"\Axiom$!B(c)^{k+1}, \Pi \fCenter \Lambda$"),
        (r"above $\Pi \Sequent \Lambda, \lexists[x][!B(x)]$:",
         r"above $\Pi \Sequent \Lambda, \lexists[x][!B(x)]^i$:"),
        (r"\Axiom$\Pi \fCenter \Lambda, \lexists[x][!B(x)]^k, !B(t)^{k+1}$",
         r"\Axiom$\Pi \fCenter \Lambda, \lexists[x][!B(x)]^{k+1}, !B(t)^{k+2}$"),
        (r"\RightLabel{\LeftR{\lexists}}" + "\n" +
         r"  \UnaryInf$\Pi \fCenter \Lambda, \lexists[x][!B(x)]^i$",
         r"\RightLabel{\RightR{\lexists}}" + "\n" +
         r"  \UnaryInf$\Pi \fCenter \Lambda, \lexists[x][!B(x)]^i$"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
