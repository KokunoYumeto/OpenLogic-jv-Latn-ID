"""Bounded comparison view for Euclidean tableau-soundness slips."""


def repaired_olp0466_source(s: str) -> str:
    replacements = [
        ("$\\mSat{M}{\\Box !B}[f(\\sigma).n]$",
         "$\\mSat{M}{\\Box !B}[f(\\sigma.n)]$"),
        ("$\\mSat/{M}{\\Diamond !B}[f(\\sigma).n]$",
         "$\\mSat/{M}{\\Diamond !B}[f(\\sigma.n)]$"),
        ("formula}~$\\sFmla{\\True}{\\Box!B}[\\sigma]$ on the branch. Suppose\n"
         "    $\\mSat{M}{\\Gamma}[f]$, in particular, $\\mSat/{M}{\\Diamond",
         "formula}~$\\sFmla{\\False}{\\Diamond!B}[\\sigma]$ on the branch. Suppose\n"
         "    $\\mSat{M}{\\Gamma}[f]$, in particular, $\\mSat/{M}{\\Diamond"),
    ]
    for old, new in replacements:
        assert s.count(old) == 1, old
        s = s.replace(old, new, 1)
    return s
