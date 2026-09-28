"""Bounded repairs for four natural-deduction soundness proof findings."""


def repaired_olp0505_source(s: str) -> str:
    repairs = (
        (r"\Gamma \cup \Delta \Entails !A \land !B", r"\Gamma \cup \Delta \Entails !B \land !C"),
        ("Similarly, if the premise is~$!C$, we have that\n      $\\Gamma \\Entails !C$.",
         "Similarly, if the premise is~$!C$, we have that\n      $\\Gamma \\Entails !B \\lor !C$."),
        (r"$\mSat{M}{!B}$[w]", r"$\mSat{M}{!B}[w]$"),
        (r"\Delta_1 \cup !B \Entails !D", r"\Delta_1 \cup \{!B\} \Entails !D"),
        (r"\Delta_2 \cup !C \Entails !D", r"\Delta_2 \cup \{!C\} \Entails !D"),
    )
    for old, new in repairs:
        assert s.count(old) == 1
        s = s.replace(old, new, 1)
    return s
