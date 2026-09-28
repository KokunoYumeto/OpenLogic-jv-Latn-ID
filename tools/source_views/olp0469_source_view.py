"""Bounded comparison view for the countermodel examples; frozen source stays intact."""


def repaired_olp0469_source(s: str) -> str:
    replacements = [
        (r"constructing countermodels to~$!A$ if $\Entails/ A$.",
         r"constructing countermodels to~$!A$ if $\Entails/ !A$."),
        ("and end up with a ``complete''\n  !!{tableau},",
         "and end up with an open complete branch of a\n  !!{tableau},"),
        ("The construction of\n  the closed tableau says", "The construction of\n  the complete tableau says", 2),
        (r"$\sFmla{\True}{\Diamond(p \land q)}[1]$ on line~$3$.",
         r"$\sFmla{\False}{\Diamond(p \land q)}[1]$ on line~$3$."),
        (r"the $\TRule{\True}{\Diamond}$ rule for", 
         r"the $\TRule{\False}{\Diamond}$ rule for"),
        (r"\pFmla{\False}{\Diamond(p \land q) \lif (\Diamond p \land \Diamond q)}{1},",
         r"\pFmla{\False}{(\Diamond p \land \Diamond q) \lif \Diamond(p \land q)}{1},"),
        ("[\\pFmla{\\False}{\\Diamond(p \\land q)}{1},\n"
         "          just = {\\TRule{\\False}{\\lif}[1]}\n"
         "          [\\pFmla{\\True}{\\Diamond p}{1},",
         "[\\pFmla{\\False}{\\Diamond(p \\land q)}{1},\n"
         "          just = {\\TRule{\\False}{\\lif}[1]}, checked\n"
         "          [\\pFmla{\\True}{\\Diamond p}{1},", 2, "last"),
        ("$V(p) =\n  \\{1.2\\}$ (because line~11", 
         "$V(p) =\n  \\{1.2\\}$ (because line~12"),
        (r"$V(q) = \{1.1\}$ (because line~10", 
         r"$V(q) = \{1.1\}$ (because line~11"),
        ("$\\sFmla{\\True}{q}[1.1]$). The model is pictured in\n  \\olref{fig:counter-Diamond}",
         "$\\sFmla{\\True}{q}[1.2]$). The model is pictured in\n  \\olref{fig:counter-Diamond}"),
    ]
    for item in replacements:
        old, new = item[:2]
        count = item[2] if len(item) >= 3 else 1
        assert s.count(old) == count, (old, s.count(old), count)
        if len(item) == 4 and item[3] == "last":
            i = s.rfind(old)
            s = s[:i] + new + s[i + len(old):]
        else:
            s = s.replace(old, new, count)
    return s
