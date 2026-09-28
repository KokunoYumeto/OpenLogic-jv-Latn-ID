"""Bounded repairs to aleph enumeration and the conditional GCH bound."""


def repaired_olp0590_source(s: str) -> str:
    repairs = (
        (
            r"definition of $\cardfont{a}$ is provided",
            r"definition of the $\aleph$ and $\beth$ sequences is provided",
        ),
        (
            "By transfinite induction on cardinals. For induction, suppose that if\n"
            + r"$\cardfont{b} < \cardfont{a}$",
            "By transfinite induction on infinite cardinals. The base case is "
            + r"$\cardfont{a}=\omega=\aleph_0$"
            + ". For induction, suppose that if\n"
            + r"$\omega \leq \cardfont{b} < \cardfont{a}$",
        ),
        (
            "show that when " + r"$\cardfont{b} < \cardfont{a}$" + ", the value of",
            "show that when " + r"$\cardfont{a}$" + " is infinite and "
            + r"$0<\cardfont{b}<\cardfont{a}$" + ", the value of",
        ),
        (
            r"\gamma_\cardfont{b}$. " + "\n\\end{proof}",
            r"\gamma_\cardfont{b}$. "
            + "The index is unique because " + r"$\aleph$" + " is strictly increasing.\n\\end{proof}",
        ),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    wrong = r"\bigcup_{\cardfont{b} < \cardfont{a}}"
    right = r"\bigcup_{\omega \leq \cardfont{b} < \cardfont{a}}"
    assert s.count(wrong) == 3, s.count(wrong)
    return s.replace(wrong, right)
