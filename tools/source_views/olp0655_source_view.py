"""Bounded comparison view for three proof and cross-reference corrections."""


def repaired_olp0655_source(s: str) -> str:
    repairs = (
        (r"$\Delta = \Delta, !A$. In this case, $\pi_1$ ends",
         r"$\Delta = \Delta', !A$. In this case, $\pi_1$ ends"),
        ("in the proof of\n\\olref{lem:inv-G3c-cut}. That is",
         "in the proof of\n\\olref{lem:max-cut-red-G3c}. That is"),
        (r"\olref[top]{lem:cut-adm-G3c} establishes",
         r"\olref{lem:max-cut-red-G3c} establishes"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
