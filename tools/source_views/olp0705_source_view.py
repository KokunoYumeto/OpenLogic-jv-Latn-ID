"""Distinct G1i table identity and the exact minimal-logic axiom difference."""
def repaired_olp0705_source(s: str) -> str:
    repairs = (
        (r"\ollabel{tab:G1c}", r"\ollabel{tab:G1i}"),
        ("without axioms $\\lfalse,\n\\Gamma \\Sequent \\Delta$", "without the axiom $\\lfalse \\Sequent \\quad$"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, wrong
        s = s.replace(wrong, right, 1)
    return s
