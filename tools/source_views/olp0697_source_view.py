"""Context consistency, partial typing, injection/binders and unique table reference."""
def repaired_olp0697_source(s: str) -> str:
    repairs = (
        ("context~$\\Gamma$, the proof \\emph{is} uniquely determined.", "context~$\\Gamma$ and the term is well-typed, the corresponding typing proof\n\\emph{is} uniquely determined."),
        ("is a set $\\Gamma$ such that for\nevery free variable of~$N$", "is a set $\\Gamma$ assigning at most one formula to each variable, such that for\nevery free variable of~$N$"),
        ("(relative to~$\\Gamma$) is inductively defined as follows:", "(relative to~$\\Gamma$) is inductively defined as follows. Bound variables\n  are first renamed fresh for the context:"),
        (r"\inj[!B]{i}{!M}", r"\inj[!B]{i}{N}"),
        ("to $x:!A, \\Gamma$ and $N_2$ has type~$!C$ relative to $y:!B,", "to $x_1:!A, \\Gamma$ and $N_2$ has type~$!C$ relative to $x_2:!B,"),
        ("Every proof term~$N$ has exactly one type relative to a\ncontext~$\\Gamma$ for~$N$.", "Every proof term~$N$ has at most one type relative to a\ncontext~$\\Gamma$ for~$N$. Every well-typed term has exactly one type."),
        (r"\olref{tab:tN2ip}", r"\olref{tab:tN3ip}"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, wrong
        s = s.replace(wrong, right, 1)
    return s
