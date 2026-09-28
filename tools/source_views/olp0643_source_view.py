"""Bounded comparison view for the provability proof appendix."""


def repaired_olp0643_source(s: str) -> str:
    repairs = (
        (r"\item We assume that $\Gamma_0 \cup\{\lnot !A\} \Proves \lfalse$.",
         r"\item We assume that $\Gamma_0 \cup\{!A\} \Proves \lfalse$."),
        (r"1. & $\Gamma_0 \cup\{\lnot !A\} \Proves \lfalse$ & hyp.",
         r"1. & $\Gamma_0 \cup\{!A\} \Proves \lfalse$ & hyp."),
        (r"2. & $\Gamma_0 \Proves \lnot !A \lif \lfalse$ & Deduction Theorem",
         r"2. & $\Gamma_0 \Proves !A \lif \lfalse$ & Deduction Theorem"),
        (r"3. & $\Gamma_0 \Proves (\lnot !A \lif \lfalse) \lif !A$ & Ax0",
         r"3. & $\Gamma_0 \Proves (!A \lif \lfalse) \lif \lnot !A$ & Ax0"),
        (r"4. & $\Gamma_0 \Proves !A$ & MP 2, 3",
         r"4. & $\Gamma_0 \Proves \lnot !A$ & MP 2, 3"),
        (r"\item We assume that $\Gamma \cup \{ !A \} \Proves \lfalse$ and that",
         r"\item We assume that $\Gamma_0 \cup \{ !A \} \Proves \lfalse$ and that"),
        (r"assume both that $\Gamma_0 \Proves !A$ and $\Gamma_0 \Proves !A \lif !B $.",
         r"assume both that $\Gamma_0 \Proves !A$ and $\Gamma_1 \Proves !A \lif !B $."),
        (r"2. & $\Gamma_0 \Proves !A \lif !B $ & hyp",
         r"2. & $\Gamma_1 \Proves !A \lif !B $ & hyp"),
        (r"3. & $\Gamma_0 \Proves !B$ & MP 1, 2",
         r"3. & $\Gamma_0 \cup \Gamma_1 \Proves !B$ & MP 1, 2"),
        (r"\item if $!A$ is an axiom, then so is",
         r"\item if $!A_i$ is an axiom, then so is"),
        (r"in $\Subst{!A}{y}{x}$, then",
         r"in $\Subst{!A}{y}{c}$, then"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    start = s.index("% prop:provability-land-left")
    end = s.index("% prop:provability-land-right", start)
    block = s[start:end]
    wrong = r"3. & $\Gamma_0 \Proves !A \lor !B$ & MP 1, 2"
    right = r"3. & $\Gamma_0 \Proves !A$ & MP 1, 2"
    assert block.count(wrong) == 1
    s = s[:start] + block.replace(wrong, right, 1) + s[end:]
    return s
