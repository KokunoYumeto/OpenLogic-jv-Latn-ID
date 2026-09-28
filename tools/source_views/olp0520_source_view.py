"""Bounded strict-conditional repair and explicit intended S5 setting."""


def repaired_olp0520_source(s: str) -> str:
    repairs = (
        (r"\lnot(!A \lif !B) & \Entails/ !A \land \lnot !B",
         r"\lnot(!A \strictif !B) & \Entails/ !A \land \lnot !B"),
        ("We have:\n", "In S5, we have:\n"),
        ("antecedent or a necessarily true consequent is true. Moreover, any\n",
         "antecedent or a necessarily true consequent is true. Moreover, in S5 any\n"),
    )
    for old, new in repairs:
        assert s.count(old) == 1, old
        s = s.replace(old, new, 1)
    return s
