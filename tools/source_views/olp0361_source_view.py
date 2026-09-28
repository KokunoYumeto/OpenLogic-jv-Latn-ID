"""Bounded frozen-source view for the substitution definition and proofs.

The recorded repairs only supply the binder-identity case and correct
misstated variables, hypotheses, algebra and definedness. The source file
remains byte-for-byte frozen; QA compares the target against this view.
"""
from __future__ import annotations


def repaired_olp0361_source(text: str) -> str:
    def swap(old: str, new: str) -> None:
        nonlocal text
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)

    # OLPL-246: the prose example requires a matching-binder identity branch.
    swap(
        r"      if $x \neq y$ and $y \notin \FV{N}$, otherwise undefined." + "\n"
        r"      \ollabel{defn:substitution-4}" + "\n"
        r"  \end{enumerate}",
        r"      if $x \neq y$ and $y \notin \FV{N}$." + "\n"
        r"      \ollabel{defn:substitution-4}" + "\n"
        r"    \item $\Subst{(\lambd[x][P])}{N}{x} = \lambd[x][P]$." + "\n"
        r"  \end{enumerate}" + "\n"
        "  Otherwise undefined.",
    )
    # OLPL-247: the no-free-variable proof needs the matching-binder case;
    # in the other case, freeness belongs to P rather than nonexistent Q.
    swap(
        r"  \item $M$ is of the form $\lambd[y][P]$, and since" + "\n"
        r"    $\Subst{\lambd[y][P]}{N}{x}$ is defined, it has to be" + "\n"
        r"    $\lambd[y][\Subst{P}{N}{x}]$. Then $\Subst{P}{N}{x}$ has to be" + "\n"
        r"    defined; also, $x \neq y$ and $x \notin \FV{Q}$. Then:",
        r"  \item $M$ is of the form $\lambd[y][P]$. If $x=y$, the" + "\n"
        r"    abstraction stays unchanged. If $x \neq y$ and" + "\n"
        r"    $\Subst{\lambd[y][P]}{N}{x}$ is defined, it is" + "\n"
        r"    $\lambd[y][\Subst{P}{N}{x}]$. Then $\Subst{P}{N}{x}$ is" + "\n"
        r"    defined. From $x \notin \FV{M}$ and $x \neq y$ we also get" + "\n"
        r"    $x \notin \FV{P}$. Then:",
    )
    swap(
        r"      \FV{\Subst{\lambd[y][P]}{N}{x}} = \\",
        r"      \FV{\Subst{\lambd[y][P]}{N}{x}} \\",
    )
    # OLPL-248: repair the stray parenthesis, application variable,
    # abstraction premise, and set algebra in the free-variable theorem.
    swap(r"$x \in \FV{M})$", r"$x \in \FV{M}$")
    swap(r"$\Subst{(PQ)}{N}{y}$", r"$\Subst{(PQ)}{N}{x}$")
    swap(
        r"  \item $M$ is of the form $\lambd[y][P]$. Since" + "\n"
        r"    $\Subst{\lambd[y][P]}{N}{x}$ is defined, it has to be" + "\n"
        r"    $\lambd[y][\Subst{P}{N}{x}]$, with $\Subst{P}{N}{x}$" + "\n"
        r"    defined, $x \neq y$ and $y \notin \FV{N}$; also, since $y \in" + "\n"
        r"    \FV{\lambd[x][P]}$, we have $y \in \FV{P}$ too. Now:",
        r"  \item $M$ is of the form $\lambd[y][P]$. As $x \in \FV{M}$," + "\n"
        r"    we have $x \neq y$ and $x \in \FV{P}$. Since" + "\n"
        r"    $\Subst{\lambd[y][P]}{N}{x}$ is defined, it is" + "\n"
        r"    $\lambd[y][\Subst{P}{N}{x}]$; $\Subst{P}{N}{x}$ is defined" + "\n"
        r"    and $y \notin \FV{N}$. Now:",
    )
    swap(
        r"      \FV{\Subst{(\lambd[y][P])}{N}{x}} = \\",
        r"      \FV{\Subst{(\lambd[y][P])}{N}{x}} \\",
    )
    swap(
        r"      & = ((\FV{P} \setminus \{y\}) \cup (\FV{N} \setminus \{x\})" + "\n"
        r"       && \text{by inductive hypothesis} \\",
        r"      & = ((\FV{P} \setminus \{x\}) \cup \FV{N}) \setminus \{y\}" + "\n"
        r"       && \text{by inductive hypothesis} \\",
    )
    swap(r"       && x \notin \FV{N} \\", r"       && y \notin \FV{N} \\")
    # OLPL-249: inverse substitution requires the reverse to be defined.
    # For x=y it is identity; in the abstraction case both binders must
    # differ from x and y for the displayed recursive equalities.
    swap(
        r"  If $\Subst{M}{y}{x}$ is defined and $y \notin \FV{M}$, then" + "\n"
        r"  $\Subst{\Subst{M}{y}{x}}{x}{y} = M$.",
        r"  If $\Subst{M}{y}{x}$ and" + "\n"
        r"  $\Subst{\Subst{M}{y}{x}}{x}{y}$ are defined and" + "\n"
        r"  $y \notin \FV{M}$, then $\Subst{\Subst{M}{y}{x}}{x}{y} = M$.",
    )
    swap(
        r"  By induction on the formation of $M$." + "\n"
        r"  \begin{enumerate}" + "\n"
        r"  \item $M$ is a variable $z$: Exercise.",
        r"  If $x=y$, both substitutions are identities. Assume" + "\n"
        r"  $x \neq y$ and induct on the formation of $M$." + "\n"
        r"  \begin{enumerate}" + "\n"
        r"  \item $M$ is a variable $z$: Exercise.",
    )
    swap(
        r"  \item $M$ is of the form $\lambd[z][N]$. Because" + "\n"
        r"    $\Subst{\lambd[z][N]}{y}{x}$ is defined, we know" + "\n"
        r"    that $z \neq y$. So:",
        r"  \item $M$ is of the form $\lambd[z][N]$. Since" + "\n"
        r"    $\Subst{\lambd[z][N]}{y}{x}$ and its reverse are defined," + "\n"
        r"    $z \neq x$ and $z \neq y$. From $y \notin \FV{M}$ and" + "\n"
        r"    $z \neq y$, also $y \notin \FV{N}$. So:",
    )
    return text
