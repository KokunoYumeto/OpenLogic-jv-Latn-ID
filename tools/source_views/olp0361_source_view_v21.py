"""Second bounded view: vacuous substitution makes alpha renaming reversible."""
from __future__ import annotations

from olp0361_source_view import repaired_olp0361_source


def repaired_olp0361_source_v21(text: str) -> str:
    text = repaired_olp0361_source(text)

    def swap(old: str, new: str) -> None:
        nonlocal text
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)

    # OLPL-250: no occurrence of x can be captured, so an abstraction
    # with no free x in its body must admit an identity substitution.
    swap(
        r"    \item $\Subst{(\lambd[x][P])}{N}{x} = \lambd[x][P]$." + "\n"
        r"  \end{enumerate}",
        r"    \item $\Subst{(\lambd[x][P])}{N}{x} = \lambd[x][P]$." + "\n"
        r"    \item If $x \notin \FV{P}$, then" + "\n"
        r"      $\Subst{(\lambd[y][P])}{N}{x} = \lambd[y][P]$." + "\n"
        r"  \end{enumerate}",
    )
    swap(
        r"    abstraction stays unchanged. If $x \neq y$ and",
        r"    abstraction stays unchanged. If $x \notin \FV{P}$, it also" + "\n"
        r"    stays unchanged. If $x \neq y$ and",
    )
    swap(
        r"  If $\Subst{M}{y}{x}$ and" + "\n"
        r"  $\Subst{\Subst{M}{y}{x}}{x}{y}$ are defined and" + "\n"
        r"  $y \notin \FV{M}$, then $\Subst{\Subst{M}{y}{x}}{x}{y} = M$.",
        r"  If $\Subst{M}{y}{x}$ is defined and $y \notin \FV{M}$," + "\n"
        r"  then $\Subst{\Subst{M}{y}{x}}{x}{y}$ is defined and" + "\n"
        r"  $\Subst{\Subst{M}{y}{x}}{x}{y} = M$.",
    )
    swap(
        r"  If $x=y$, both substitutions are identities. Assume" + "\n"
        r"  $x \neq y$ and induct on the formation of $M$.",
        r"  If $x=y$, both substitutions are identities. If" + "\n"
        r"  $x \notin \FV{M}$, neither substitution changes $M$." + "\n"
        r"  Assume $x \neq y$ and $x \in \FV{M}$ and induct on the" + "\n"
        r"  formation of $M$.",
    )
    swap(
        r"    $\Subst{\lambd[z][N]}{y}{x}$ and its reverse are defined," + "\n"
        r"    $z \neq x$ and $z \neq y$. From $y \notin \FV{M}$ and",
        r"    $\Subst{\lambd[z][N]}{y}{x}$ is defined and" + "\n"
        r"    $x \in \FV{M}$, $z \neq x$ and $z \neq y$. From" + "\n"
        r"    $y \notin \FV{M}$ and",
    )
    swap(
        r"    $z \neq y$, also $y \notin \FV{N}$. So:",
        r"    $z \neq y$, also $y \notin \FV{N}$. The reverse in $N$" + "\n"
        r"    is defined. So:",
    )
    return text
