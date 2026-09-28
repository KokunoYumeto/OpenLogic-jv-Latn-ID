"""Bounded fixed-point recursion repairs and localized quote citations."""


def repaired_olp0591_source(s: str) -> str:
    repairs = (
        (r"\tau_0(A) & \defis \card{A}", r"\tau_0(A) & \defis \cardsucc{\card{A}}"),
        (r"W_0 &\defis 0", r"W_0 &\defis \tau(0)"),
        (r"\citep[p.~257]{Boolos2000}", r"\citep[kaca~257]{Boolos2000}"),
        (r"\citep[p.~268]{Boolos2000}", r"\citep[kaca~268]{Boolos2000}"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
