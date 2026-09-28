"""Bounded comparison view for the auxiliary implication-cut derivation."""


def repaired_olp0660_source(s: str) -> str:
    repairs = (
        (r"\Deduce$B!, \Gamma \fCenter \Delta, !C$",
         r"\Deduce$!B, \Gamma \fCenter \Delta, !C$", 1),
        (r"$!B, \Gamma, \Pi, \Pi \fCenter \Delta, \Lambda," + "\n" + r"\Lambda$",
         r"$!B, \Gamma, \Pi \fCenter \Delta, \Lambda$", 2),
        (r"\Deduce$!B, \Gamma, \Pi \fCenter \Delta, \Lambda$" + "\n" +
         r"\RightLabel{\Cut}" + "\n" +
         r"\BinaryInf$!B, \Gamma, \Pi \fCenter \Delta, \Lambda$",
         r"\Deduce$!B, \Gamma, \Pi \fCenter \Delta, \Lambda$" + "\n" +
         r"\RightLabel{\Cut}" + "\n" +
         r"\BinaryInf$\Gamma, \Gamma, \Pi, \Pi \fCenter \Delta, \Delta, \Lambda, \Lambda$", 1),
        (r"$\Gamma," + "\n" + r"\Gamma, \Pi, \Pi, \Pi \fCenter \Delta, \Lambda, \Lambda, \Lambda$",
         r"$\Gamma, \Gamma, \Pi, \Pi \fCenter \Delta, \Delta, \Lambda, \Lambda$", 1),
    )
    for wrong, right, count in repairs:
        assert s.count(wrong) == count, (wrong, s.count(wrong))
        s = s.replace(wrong, right)
    return s
