"""Bounded corrections and explicit proof-gap notes; frozen English is untouched."""

def repaired_olp0687_source(s: str) -> str:
    repairs = (
        (r"\len{p} &= 0\\", r"\len{p} &= 0\\" + "\n  " + r"\len{\lfalse} &= 0\\"),
        ("  \\len{!A} + \\len{!B} + 1\n\\end{align*}", "  \\len{!A_1} + \\len{!A_2} + 1\n\\end{align*}"),
        (r"\maxrank{M} = \max \{\cutrank{N} | N", r"\maxrank{M} = \max (\{0\} \cup \{\cutrank{N} | N"),
        ("    and is redex}\\}\n\\]", "    and is redex}\\})\n\\]"),
        (r"$\ore{i}{x_1}{P_1}{x_2}{P_2}$", r"$\ore{x}{x_1}{P_1}{x_2}{P_2}$"),
        (r"$\cutrank{\Subst{M}{N}{x}} = \len{!A})$", r"$\cutrank{\Subst{M}{N}{x}} = \len{!A}$"),
        ("Its cut rank is equal to\n        $\\cutrank{x}$, which is $\\len{!A}$.", "Its cut rank is equal to the length of the type of the substituted variable,\n        which is $\\len{!A}$."),
        ("rank, which is less than $\\cutrank{M}$ by assumption, or the cut", "rank, which is less than $\\cutrank{M}$ by assumption, or it is a redex copied\n    from the argument $Q$ and has smaller cut rank by the same assumption, or the cut"),
        ("equal cut rank, which is less than $\\cutrank{M}$ by assumption; or", "equal cut rank, which is less than $\\cutrank{M}$ by assumption; or it is a redex\n    copied from the injected term $N$ and has smaller cut rank by the same assumption; or"),
        ("\\end{enumerate}\n\\end{proof}\n\nThe fact that typed", "\\end{enumerate}\n\\footnote{Editorial note (OLPL-655): This source argument only bounds redexes inside the contracted subterm. It does not control new redexes exposed in the enclosing context, particularly when a disjunction elimination has an arbitrary result type. Nor does the stated rank assign a measure to permutation conversions. The argument as printed therefore remains incomplete for the full calculus; this note does not supply the missing proof.}\n\\end{proof}\n\nThe fact that typed"),
        ("and so cannot overlap. This means that", "and so cannot partially overlap. This means that"),
        ("this reduces also to~$O_2$.", "this reduces also to~$O_1'$. If the inner redex instead occurs in the\n  discarded component, both orders still yield the first component.\\footnote{Editorial note (OLPL-657): This is a sketch of the principal-contraction cases. The remaining nested cases and the permutation-conversion interactions are not established here.}"),
        ("N & = N_1' \\redone N_2'", "N & = N_0' \\redone N_1' \\redone N_2'"),
        ("N & = N_1'' \\redone N_2''", "N & = N_0'' \\redone N_1'' \\redone N_2''"),
        ("some $N'''$ such that $N_1' \\red N'''$ and $N_1'' \\red N'''$. Since", "a common reduct. By strong normalization this reduct has a normal form\n  $N'''$, so $N_1' \\red N'''$ and $N_1'' \\red N'''$. Since"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
