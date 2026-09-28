"""Bounded comparison view for the Euclidean-filtration source defects."""


def repaired_olp0459_source(s: str) -> str:
    old = "and then also between $w_2$ and~$w_5$."
    assert s.count(old) == 1
    s = s.replace(old, "and then also between $[w_2]$ and~$[w_5]$.", 1)

    arrow = "    \\draw[->] (w1) to (w2);\n"
    assert s.count(arrow) == 2
    s = s.replace(arrow, arrow + "    \\draw[reflexive above] (w2) to (w2);\n")

    proof_open = "\\begin{proof}\n\\begin{enumerate}\n"
    proof_close = "\\end{enumerate}\n\\end{proof}"
    assert s.count(proof_open) == s.count(proof_close) == 1
    start = s.index(proof_open) + len(proof_open)
    end = s.index(proof_close, start)
    original = s[start:end]
    euclidean = ("  \\item Exercise. Use the fact that both \\Ax{5} and $\\Ax{5_\\Diamond}$\n"
                 "    are valid in all euclidean models.\n")
    symmetric = ("  \\item Exercise. Use the fact that \\Ax{B} and $\\Ax{B_\\Diamond}$ are\n"
                 "    valid in all symmetric models.\n")
    assert original.endswith(euclidean + symmetric)
    transitive = original[:-len(euclidean + symmetric)]
    assert transitive.startswith("  \\item If $\\mModel{M^*}$ is a coarsest filtration")
    old_box = "\\iftag{prvBox}{Suppose $\\mSat{M}{\\Box !A}[u]$; then"
    new_box = "\\iftag{prvBox}{Suppose $\\Box!A \\in \\Gamma$ and $\\mSat{M}{\\Box !A}[u]$; then"
    assert transitive.count(old_box) == 1
    transitive = transitive.replace(old_box, new_box, 1)
    old_diamond = "\\iftag{prvDiamond}{Suppose\n      $\\mSat{M}{!A}[w]$; then"
    new_diamond = "\\iftag{prvDiamond}{Suppose\n      $\\Diamond!A \\in \\Gamma$ and $\\mSat{M}{!A}[w]$; then"
    assert transitive.count(old_diamond) == 1
    transitive = transitive.replace(old_diamond, new_diamond, 1)
    s = s[:start] + symmetric + transitive + euclidean + s[end:]
    return s
