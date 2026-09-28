"""Macro arity, injection annotations, capture avoidance and sequence correction."""
def repaired_olp0691_source(s: str) -> str:
    repairs = (
        (r"\pair{N_1, N_2}", r"\pair{N_1}{N_2}"),
        (r"\inj{i}{!A}{N}", r"\inj[!A]{i}{N}"),
        (r"\inj[!A_i]{i}{M}", r"\inj[!A_{3-i}]{i}{M}"),
        ("Here, $\\Subst{M}{N_i}{x}$ means replacing all free occurrences of the\nvariable~$x$ in $M$ by~$N_i$.", "Here, $\\Subst{N_i}{M}{x_i}$ means replacing all free occurrences of the\nvariable~$x_i$ in $N_i$ by~$M$, renaming bound variables first when\nnecessary to avoid capturing free variables."),
        (r"\redone M_2 \redone M_2 \redone \dots", r"\redone M_2 \redone \dots"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1
        s = s.replace(wrong, right, 1)
    return s
