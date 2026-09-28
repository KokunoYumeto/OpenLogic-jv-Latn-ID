"""Bounded comparison view for the K-tableau completeness argument."""


def repaired_olp0468_source(s: str) -> str:
    replacements = [
        ("the corresponding conclusion for every prefix occurring on\n"
         "      the branch in the case of modal rules that require a used\n"
         "      prefix.",
         "the corresponding conclusion for every relevant successor\n"
         "      prefix already used on the branch in the case of modal\n"
         "      rules that require a used prefix."),
        ("$\\sFmla{\\True}{!B\n  \\land !C}$.",
         "$\\sFmla{\\True}{!B\n  \\land !C}[\\sigma]$."),
        ("contains at least one of $\\sFmla{\\False}{!B}[\\sigma]$ and\n"
         "$\\sFmla{\\True}{!C}[\\sigma]$.",
         "contains at least one of $\\sFmla{\\True}{!B}[\\sigma]$ and\n"
         "$\\sFmla{\\True}{!C}[\\sigma]$."),
        ("If it contains \\iftag{prvBox}\n"
         "{$\\sFmla{\\False}{\\Box}[\\sigma]$} {$\\sFmla{\\True}{\\Diamond}[\\sigma]$}\n"
         "it also contains \\iftag{prvBox} {$\\sFmla{\\False}{\\Box}[\\sigma.n]$}\n"
         "{$\\sFmla{\\True}{\\Diamond}[\\sigma.n]$} for at least one~$n$.",
         "If it contains \\iftag{prvBox}\n"
         "{$\\sFmla{\\False}{\\Box !B}[\\sigma]$} {$\\sFmla{\\True}{\\Diamond !B}[\\sigma]$}\n"
         "it also contains \\iftag{prvBox} {$\\sFmla{\\False}{!B}[\\sigma.n]$}\n"
         "{$\\sFmla{\\True}{!B}[\\sigma.n]$} for at least one~$n$."),
        ("whenever it contains \\iftag{prvBox} {$\\sFmla{\\True}{\\Box}[\\sigma]$}\n"
         "{$\\sFmla{\\False}{\\Diamond}[\\sigma]$} it also contains \\iftag{prvBox}\n"
         "{$\\sFmla{\\True}{\\Box}[\\sigma.n]$}\n"
         "{$\\sFmla{\\False}{\\Diamond}[\\sigma.n]$} for every~$n$",
         "whenever it contains \\iftag{prvBox} {$\\sFmla{\\True}{\\Box !B}[\\sigma]$}\n"
         "{$\\sFmla{\\False}{\\Diamond !B}[\\sigma]$} it also contains \\iftag{prvBox}\n"
         "{$\\sFmla{\\True}{!B}[\\sigma.n]$}\n"
         "{$\\sFmla{\\False}{!B}[\\sigma.n]$} for every~$n$"),
        ("Every finite $\\Gamma$ has !!a{tableau} in which every branch is complete.",
         "Every finite $\\Gamma$ has !!a{tableau} in which every open branch is complete."),
        ("  repeat. But by construction, every branch is closed.",
         "  repeat. Fresh successor prefixes strictly lower modal depth; there\n"
         "  are only finitely many subformulas and each fresh-prefix\n"
         "  obligation is discharged once at a prefix. Hence this process\n"
         "  terminates, and by construction every open branch is complete."),
        ("By the proposition, $\\Gamma$ has !!a{tableau} in which every branch is\n"
         "complete. Since it has no closed !!{tableau}, it thas has !!a{tableau} in",
         "First suppose $\\Gamma$ is finite. By the proposition, $\\Gamma$ has\n"
         "!!a{tableau} in which every open branch is complete. Since it has\n"
         "no closed !!{tableau}, it has !!a{tableau} in"),
        ("$\\mSat/{M(\\Delta)}{!B}[\\sigma]$ or\n"
         "      $\\mSat/{M(\\Delta)}{!B}[\\sigma]$.",
         "$\\mSat/{M(\\Delta)}{!B}[\\sigma]$ or\n"
         "      $\\mSat/{M(\\Delta)}{!C}[\\sigma]$."),
        ("$\\mSat/{M(\\Delta)}{!B}[\\sigma]$ and\n"
         "      $\\mSat/{M(\\Delta)}{!B}[\\sigma]$.",
         "$\\mSat/{M(\\Delta)}{!B}[\\sigma]$ and\n"
         "      $\\mSat/{M(\\Delta)}{!C}[\\sigma]$."),
        ("$\\mSat{M(\\Delta)}{!B}[\\sigma]$ and\n"
         "      $\\mSat/{M(\\Delta)}{!B}[\\sigma]$.",
         "$\\mSat{M(\\Delta)}{!B}[\\sigma]$ and\n"
         "      $\\mSat/{M(\\Delta)}{!C}[\\sigma]$."),
        ("Since $\\Gamma \\subseteq \\Delta$, $\\mSat{M(\\Delta)}{\\Gamma}$.",
         "Since $\\Gamma \\subseteq \\Delta$, $\\mSat{M(\\Delta)}{\\Gamma}$.\n"
         "For arbitrary $\\Gamma$, every finite subset has no closed\n"
         "!!{tableau} and is satisfiable by the finite case. Modal\n"
         "compactness, obtained from first-order compactness by the\n"
         "standard translation, makes $\\Gamma$ satisfiable as well."),
    ]
    for old, new in replacements:
        assert s.count(old) == 1, old
        s = s.replace(old, new, 1)
    return s
