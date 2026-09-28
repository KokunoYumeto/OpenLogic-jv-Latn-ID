"""Bounded predicativity corrections plus source-language TeX typography."""


def repaired_olp0533_source(s: str) -> str:
    repairs = (
        ("all\nand only those sets which are not non-self-membered.",
         "all\nand only those sets which are non-self-membered."),
        (r"If we follow them in rejecting the \emph{vicious-circle principle},",
         r"If we follow them in accepting the \emph{vicious-circle principle},"),
        (r'Na\"{i}ve', 'Naif'),
        (r'(im)\-pre\-di\-ca\-tiv\-ity', '(im)predicativity'),
    )
    for old, new in repairs:
        assert s.count(old) == 1, (old, s.count(old))
        s = s.replace(old, new, 1)
    return s
