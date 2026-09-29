"""Bounded substitution and regularization corrections, without source edits."""
def repaired_olp0703_source(s: str) -> str:
    repairs = (
        ("by replacing every occurrence of~$c$ by~$t$ is a regular !!{proof}.",
         "by capture-avoiding replacement of every occurrence of~$c$ by~$t$ is a regular !!{proof}.\nBefore substitution, choose bound variables fresh for the replacement term."),
        (r"\Setabs{!A(t)}{!A(c) \in \Gamma}$." + "\n", r"\Setabs{!A(t)}{!A(c) \in \Gamma}$." + "\nThe displayed comprehension is a multiset comprehension: every original\noccurrence contributes one substituted occurrence.\n"),
        (r"\RightLabel{\RightR{\lforall}}" + "\n    " + r"\UnaryInf$\lforall[x][!A(x,c)], \Gamma(c) \fCenter \Delta'(c)$",
         r"\RightLabel{\LeftR{\lforall}}" + "\n    " + r"\UnaryInf$\lforall[x][!A(x,c)], \Gamma(c) \fCenter \Delta'(c)$"),
        (r"\RightLabel{\RightR{\lforall}}" + "\n    " + r"\UnaryInf$\lforall[x][!A(x,t)], \Gamma(t) \fCenter \Delta'(t)$",
         r"\RightLabel{\LeftR{\lforall}}" + "\n    " + r"\UnaryInf$\lforall[x][!A(x,t)], \Gamma(t) \fCenter \Delta'(t)$"),
        ("Moreover, the eigenvariables of $\\pi$\n  and Since $t$ was assumed not to contain an eigenvariable of~$\\pi$\n  and $\\Subst{\\pi}{t}{c}$ are the same, the new end-sequent does not",
         "Moreover, the eigenvariables of $\\pi$ are preserved: since $t$\n  contains no eigenvariables of~$\\pi$, the eigenvariables of\n  $\\Subst{\\pi}{t}{c}$ are the same. The new end-sequent does not"),
        ("show, by induction on~$n$", "show, by strong induction on~$n$"),
        ("Otherwise, pick a highest eigenvariable inference", "Otherwise, pick a highest dirty eigenvariable inference"),
        ("it contains no eigenvariable inferences at all", "all its eigenvariable inferences are clean and none uses the selected constant as its eigenvariable"),
        ("The resulting proof has $n-1$ dirty eigenvariable inferences", "The resulting proof has fewer than $n$ dirty eigenvariable inferences"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
