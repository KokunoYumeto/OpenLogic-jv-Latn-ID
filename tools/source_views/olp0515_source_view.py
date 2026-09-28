"""Bounded audited repairs for intuitionistic tableau soundness."""


def repaired_olp0515_source(s: str) -> str:
    repairs = (
        (r"$\mSat{M}{!A}[w]$, then no", r"$\mSat/{M}{!A}[w]$, then no"),
        ("in the modal case", "in the intuitionistic case"),
        (r"if, whenever $\sigma$ and $\sigma.n$ are both" + "\n  "
         + r"in~$P$, then $Rf(\sigma)f(\sigma.n)$.",
         r"if, whenever $\sigma$ and any extension $\sigma.{*}$ are both" + "\n  "
         + r"in~$P$, then $Rf(\sigma)f(\sigma.{*})$."),
        (r"contains $\sFmla{\True}{\lfalse}$ is unsatisfiable.",
         r"contains $\sFmla{\True}{\lfalse}[\sigma]$ is unsatisfiable."),
        (r"$P(\Gamma)$ such that both If $\mSat{M}{!A}[f(\sigma)]$, then by" + "\n  "
         + r"\olref[sem][rel]{prop:true-monotonic}, since" + "\n  "
         + r"$Rf(\sigma)(\sigma.{*})$, $\mSat{M}{!A}[f(\sigma)]$. So we cannot",
         r"$P(\Gamma)$. If $\mSat{M}{!A}[f(\sigma)]$, then by" + "\n  "
         + r"\olref[sem][rel]{prop:true-monotonic}, since" + "\n  "
         + r"$Rf(\sigma)f(\sigma.{*})$, $\mSat{M}{!A}[f(\sigma.{*})]$. So we cannot"),
        (r"$\sFmla{\False}{!B \lor !C} \in \Gamma$",
         r"$\sFmla{\False}{!B \lor !C}[\sigma] \in \Gamma$"),
        ("Now let's consider the possible inferences with two premises.",
         "Now let's consider the possible branching inferences."),
        (r"contradiction. So we must have $\Gamma \Proves !A$ after all.",
         r"contradiction. So we must have $\Gamma \Entails !A$ after all."),
    )
    for old, new in repairs:
        assert s.count(old) == 1, old
        s = s.replace(old, new, 1)
    old = r"\Gamma \cup \{\sFmla{\False}{!B \lif !C}[\sigma.n]\}"
    new = r"\Gamma \cup \{\sFmla{\True}{!B}[\sigma.n], \sFmla{\False}{!C}[\sigma.n]\}"
    assert s.count(old) == 2
    s = s.replace(old, new)
    old = "and closed branches are unsatisfiable."
    new = (old + " Legal tableaux begin at the root and introduce only immediate "
           "children of used prefixes; therefore their branch prefix sets contain "
           "every nonempty initial segment of each used prefix.")
    assert s.count(old) == 1
    s = s.replace(old, new, 1)
    old = r"Let $f'$ be like $f$, except that $f'(\sigma.n)"
    new = r"Let $f'$ extend $f$ with $f'(\sigma.n)"
    assert s.count(old) == 1
    s = s.replace(old, new, 1)
    old = r"$Rf'(\sigma)f'(\sigma.n)$, so $f'$ is an interpretation of"
    new = (r"$Rf'(\sigma)f'(\sigma.n)$. Transitivity gives accessibility "
           "from all old ancestors to the new world. No old descendant of the "
           "fresh prefix exists, by the initial-segment property of legal "
           r"branches. Hence $f'$ is an interpretation of")
    assert s.count(old) == 1
    s = s.replace(old, new, 1)
    return s
