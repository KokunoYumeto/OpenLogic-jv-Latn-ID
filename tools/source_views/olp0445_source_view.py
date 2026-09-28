"""Bounded modal accessibility and lemma notation comparison view."""


def repaired_olp0445_source(s: str) -> str:
    old_val = r"$V^\Sigma)$"
    new_val = r"$V^\Sigma$)"
    assert s.count(old_val) == 1
    s = s.replace(old_val, new_val, 1)
    old_rel = ("If we stipulate that\n  $R^\\Sigma\\Delta\\Delta'$ holds whenever "
               "$\\Diamond!A \\in \\Delta$ for\n  all $!A \\in \\Delta'$, "
               "then this holds.")
    new_rel = ("If we stipulate that\n  $R^\\Sigma\\Delta\\Delta'$ holds if and only if "
               "$\\Diamond!A \\in \\Delta$ for\n  all $!A \\in \\Delta'$, "
               "then this holds.")
    assert s.count(old_rel) == 1
    s = s.replace(old_rel, new_rel, 1)
    assert s.count(r"!B_n") == 2
    s = s.replace(r"!B_n", r"!B_k")
    old_proves = r"\Box\Box^{-1}\Gamma \Proves \Box!A"
    new_proves = r"\Box\Box^{-1}\Gamma \Proves[\Sigma] \Box!A"
    assert s.count(old_proves) == 1
    return s.replace(old_proves, new_proves, 1)
