"""Bounded repairs to induction notation, arithmetic and finite-arity definitions."""
def repaired_olp0718_source(s: str) -> str:
    repairs = (
        (r"\documentclass[../../include/open-logic-section]{subfiles}", r"\documentclass[../../../include/open-logic-section]{subfiles}"),
        ("The sum of the first $n$ natural numbers", "The sum of the integers from 1 through $n$"),
        ("The sum of the first 0 natural numbers", "The empty sum for n equal to 0"),
        (r"\frac{2k + k + 2k +2}{2}", r"\frac{k^2 + k + 2k +2}{2}"),
        ("Each operator can be seen as\ncorresponding to a function of !!{formula}s that returns a new\n!!{formula} joining these two together with the operator in\nquestion.", "Each operator can be seen as\ncorresponding to a function of the appropriate number of !!{formula}s\nthat returns a new !!{formula} by applying that operator."),
        (r"\tag{Assumption}", r"\tag{Anggepan}"),
        (r"\tag{Add $k+1$ to both sides}", r"\tag{Tambah $k+1$ ing loro sisih}"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, wrong
        s = s.replace(wrong, right, 1)
    assert s.count("!!^a") == 16
    s = s.replace("!!^a", "!A")
    closure = "S$, then $f(x) \\in S$.\n\\end{defn}"
    assert s.count(closure) == 1
    s = s.replace(closure, "S$, then $f(x) \\in S$.\n" +
        r"For a function with $n \ge 1$ inputs, closure means" + "\n" +
        r"$f(x_1,\ldots,x_n) \in S$ whenever $x_1,\ldots,x_n \in S$." + "\n\\end{defn}", 1)
    preservation = "$P(a)$ implies\n$P(f(a))$ (if $a$ has property $P$, then so does $f(a)$).\n\\end{defn}"
    assert s.count(preservation) == 1
    s = s.replace(preservation, "$P(a)$ implies\n$P(f(a))$ (if $a$ has property $P$, then so does $f(a)$).\n" +
        r"For a function with $n \ge 1$ inputs, preservation means that" + "\n" +
        r"$P(a_1),\ldots,P(a_n)$ imply $P(f(a_1,\ldots,a_n))$." + "\n\\end{defn}", 1)
    return s
