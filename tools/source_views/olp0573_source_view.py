"""Bounded Montague/Potter proof repairs; frozen source remains unchanged."""


def repaired_olp0573_source(s: str) -> str:
    repairs = (
        (
            r"\theta^X \land X\text{ is transitive} \land (\forall Y \in X)(Y\text{ is transitive}\lif \lnot \theta^{Y})",
            r"\theta^X \land X\text{ transitif lan poten} \land (\forall Y \in X)(Y\text{ transitif lan poten}\lif \lnot \theta^{Y})",
            1,
        ),
        (
            r"((N\text{ is transitive})^N \land (\theta^N)^M)",
            r"((N\text{ transitif lan poten})^M \land (\theta^N)^M)",
            1,
        ),
        (
            r"(N\text{ is transitive} \land \theta^N)",
            r"(N\text{ transitif lan poten} \land \theta^N)",
            1,
        ),
        (
            r"X\text{ is transitive} \lif \sigma^X",
            r"X\text{ transitif lan poten} \lif \sigma^X",
            2,
        ),
    )
    for wrong, right, count in repairs:
        assert s.count(wrong) == count, (wrong, s.count(wrong))
        s = s.replace(wrong, right, count)
    return s
