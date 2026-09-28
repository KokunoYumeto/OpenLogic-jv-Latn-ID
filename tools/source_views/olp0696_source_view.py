"""Clarify the reduction scope and capture-safe proof substitution."""
def repaired_olp0696_source(s: str) -> str:
    repairs = (
        ("$\\beta$-reduction rules for $\\lambd$-terms exactly mirror", "reduction rules for $\\lambd$-terms exactly mirror"),
        ("remains the same after $\\beta$-conversion.", "remains the same after a reduction or permutation conversion."),
        ("left. Of course one would have to carefuly verify (by induction on\n  the height of~$\\delta_2$) that if we replace all axioms of the form\n  $\\Gamma' \\Sequent x:!B_1$ in~$\\delta_2$ by the !!{proof}~$\\delta_3$\n  of $\\Gamma \\Sequent M:!B_1$ actually results in !!a{proof}\n  $\\Subst{\\delta_2}{\\delta_3}{x:!B_1}$ of $\\Gamma \\Sequent\n  \\Subst{N}{M}{x} : !B_2$.", "left. First rename bound variables so that the discharged variable is fresh\n  for the outer context and internal binders are fresh for the substituting term.\n  Induction on the height of~$\\delta_2$ verifies that each axiom\n  $\\Gamma' \\Sequent x:!B_1$ in~$\\delta_2$ is replaced by the !!{proof}~$\\delta_3$\n  of $\\Gamma \\Sequent M:!B_1$, weakened to the remaining local context\n  after removing the discharged variable. The other variable axioms persist,\n  and each introduction or elimination rule preserves its result type; freshness\n  prevents capture in abstraction and case branches. This yields !!a{proof}\n  $\\Subst{\\delta_2}{\\delta_3}{x:!B_1}$ of $\\Gamma \\Sequent\n  \\Subst{N}{M}{x} : !B_2$."),
        ("Hence every $\\lambd$-term not in normal form $\\beta$-reduces\nto another.", "Hence every well-typed $\\lambd$-term not in normal form reduces\nto another by a reduction or permutation conversion."),
        ("ensure that $\\beta$-reduction", "ensure that reduction"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1
        s = s.replace(wrong, right, 1)
    return s
