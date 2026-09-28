"""Bounded comparison view for alpha-conversion source notation and logic."""
from __future__ import annotations


def repaired_olp0362_source(text: str) -> str:
    def swap(old: str, new: str) -> None:
        nonlocal text
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)

    # OLPL-251: a change of bound-variable name requires distinct names.
    swap(
        r"  If a term $M$ contains an occurrence of $\lambd[x][N]$, $y \notin" + "\n"
        r"  \FV{N}$, and $\Subst{N}{y}{x}$ is defined, then replacing this occurrence",
        r"  If a term $M$ contains an occurrence of $\lambd[x][N]$," + "\n"
        r"  $x \neq y$, $y \notin \FV{N}$, and $\Subst{N}{y}{x}$ is defined," + "\n"
        r"  then replacing this occurrence",
    )
    # OLPL-254: both occurrences of FV(N) need the project macro.
    assert text.count("FV(N)") == 2
    text = text.replace("FV(N)", r"\FV{N}")
    swap(r"& = FV{\Subst{N}{y}{x}} \setminus \{y\} \\",
         r"& = \FV{\Subst{N}{y}{x}} \setminus \{y\} \\")
    swap(
        r"        & = \FV{N} \setminus \{x\}" + "\n"
        r"         && \text{by \olref[sub]{thm:notinfv}} \\",
        r"        & = \FV{N} \setminus \{y\}" + "\n"
        r"         && \text{by \olref[sub]{thm:notinfv}} \\" + "\n"
        r"        & = \FV{N} \setminus \{x\} \\",
    )
    # OLPL-255: the clear-variable theorem clears old x, not new y.
    swap(
        r"First, we have $y \notin" + "\n"
        r"    \FV{\Subst{N}{y}{x}}$ by \olref[sub]{thm:clr}. By",
        r"First, we have $x \notin" + "\n"
        r"    \FV{\Subst{N}{y}{x}}$ by \olref[sub]{thm:clr}, since" + "\n"
        r"    $x \neq y$. By",
    )
    swap(
        r"    \lambd[x][N]$." + "\n"
        r"  \end{enumerate}" + "\n"
        r"\end{proof}",
        r"    \lambd[x][N]$." + "\n"
        r"  \item The other compatibility cases follow by induction." + "\n"
        r"  \end{enumerate}" + "\n"
        r"\end{proof}",
    )
    # OLPL-256: use actual free-variable macros, preserve the source's
    # unproved inner-definedness step as an explicitly logged proof gap.
    swap(r"$z \notin FV(N')$", r"$z \notin \FV{N'}$")
    swap(r"$z \notin FV(R)$", r"$z \notin \FV{R}$")
    swap(
        r"      \Subst{(\lambd[z][\Subst{N''}{z}{x}])}{R''}{y} =\\",
        r"      \Subst{(\lambd[z][\Subst{N''}{z}{x}])}{R''}{y} \\",
    )
    swap(
        r"      &= \lambd[z][\Subst{\Subst{N''}{z}{x}}{R}{y}]",
        r"      &\aeq \lambd[z][\Subst{\Subst{N''}{z}{x}}{R}{y}]",
    )
    swap(
        r"      &=\lambd[z][\Subst{\Subst{N'}{z}{x}}{R}{y}]",
        r"      &\aeq\lambd[z][\Subst{\Subst{N'}{z}{x}}{R}{y}]",
    )
    # OLPL-257: the comparison pair needs its own definedness premise
    # and an alpha-equivalent replacement.
    swap(
        r"another pair $M'' \aeq M$ and $R''$",
        r"another pair $M'' \aeq M$ and $R'' \aeq R'$",
    )
    swap(
        r"  with $\Subst{M'}{R'}{y}$ defined, then",
        r"  with $\Subst{M''}{R''}{y}$ defined, then",
    )
    return text
