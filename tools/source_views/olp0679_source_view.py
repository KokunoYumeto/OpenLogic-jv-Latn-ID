"""Bounded comparison view for proof-search completeness notation repairs."""


def repaired_olp0679_source(s: str) -> str:
    repairs = (
        (r"for all~$! \in \Delta$", r"for all~$!A \in \Delta$"),
        ("Such a premise must obviously exist for\neach~$n$",
         "Such a premise must obviously exist for\neach~$n$ having a successor stage"),
        ("\\Pi_n\n\\Sequent \\Delta_n$", "\\Pi_n\n\\Sequent \\Lambda_n$"),
        ("If if the algorithm never terminates", "If the algorithm never terminates"),
        (r"f(t_1, \dots, t_n)$.", r"f(t_1, \dots, t_m)$."),
        (r"\Domain{M}^n}{R(t_1, \dots, t_n) \in \Theta}",
         r"\Domain{M}^m}{R(t_1, \dots, t_m) \in \Theta}"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
