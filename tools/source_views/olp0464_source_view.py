"""Bounded logical comparison view for modal-tableau soundness."""


def repaired_olp0464_source(s: str) -> str:
    replacements = [
        ("but\n  $\\mSat{M}{!A}[w]$", "but\n  $\\mSat/{M}{!A}[w]$"),
        ("$\\sFmla{\\False}{!B \\lor !C} \\in \\Gamma$",
         "$\\sFmla{\\False}{!B \\lor !C}[\\sigma] \\in \\Gamma$"),
        ("$\\sFmla{\\False}{!A}[\\sigma.n]$",
         "$\\sFmla{\\False}{!B}[\\sigma.n]$"),
        ("$\\sFmla{\\True}{!A}[\\sigma.n]$",
         "$\\sFmla{\\True}{!B}[\\sigma.n]$"),
        ("possible inferences with only one premise",
         "possible non-branching inferences"),
        ("possible inferences with two premises",
         "possible branching inferences"),
        ("So we must have $\\Gamma \\Proves !A$ after all.",
         "So we must have $\\Gamma \\Entails !A$ after all."),
    ]
    for old, new in replacements:
        assert s.count(old) == 1, old
        s = s.replace(old, new, 1)
    return s
