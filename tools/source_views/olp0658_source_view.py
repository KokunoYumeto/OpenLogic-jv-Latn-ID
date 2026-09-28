"""Bounded comparison view for two Beth-proof notation corrections."""


def repaired_olp0658_source(s: str) -> str:
    repairs = (
        (r"$\Lang L(!A) = \Lang L_1 \cap" + "\n" +
         r"  \Lang L_2 = \Lang L(\Gamma) \setminus \{R\}$",
         r"$\Lang L(!A) \subseteq \Lang L_1 \cap" + "\n" +
         r"  \Lang L_2$"),
        (r"explicitly defines $!R$", r"explicitly defines $R$"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
