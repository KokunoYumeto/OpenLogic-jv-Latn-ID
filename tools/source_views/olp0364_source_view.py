"""Bounded source view for alpha-equivalence classes and malformed notation."""
from __future__ import annotations


def repaired_olp0364_source(text: str) -> str:
    def swap(old: str, new: str) -> None:
        nonlocal text
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)

    # OLPL-260: path and lam/syn/tr identifier locate this in syntax.
    swap("% Chapter: introduction", "% Chapter: syntax")
    # OLPL-261: split the malformed representative list into two math spans.
    swap(
        r"and $\rep{M}[0], \rep{M}[1], etc. $ if",
        r"and $\rep{M}[0]$, $\rep{M}[1]$, etc. if",
    )
    # OLPL-262: use the project's FV macro on equivalence classes.
    swap(r"$FV(M)$", r"$\FV{M}$")
    swap(r"$FV(\rep{M})$", r"$\FV{\rep{M}}$")
    swap(
        r"$FV(\rep{M}[0]) =" + "\n" + r"FV(\rep{M}[1])$",
        r"$\FV{\rep{M}[0]} =" + "\n" + r"\FV{\rep{M}[1]}$",
    )
    # OLPL-263: remove a duplicated equality at the start of the chain.
    swap(
        r"  \Subst{\lambd[x][x]}{y}{x} & =\ollabel{eq:1}\\",
        r"  \Subst{\lambd[x][x]}{y}{x} & \ollabel{eq:1}\\",
    )
    # OLPL-264: the class-level convention uses the FV macro.
    swap(r"$x \notin FV(R)$", r"$x \notin \FV{R}$")
    return text
