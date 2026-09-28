"""Bounded comparison view for the filtrations introduction."""


def repaired_olp0451_source(s: str) -> str:
    old_count = "number of subsets of $W \\times W$, i.e., $2^{n^2}$."
    new_count = "number of subsets of $W \\times W$, i.e., $2^{n^2}$)."
    assert s.count(old_count) == 1
    s = s.replace(old_count, new_count, 1)

    old_parts = ("in such a way that each partition contains infinitely many worlds, but\n"
                 "there are only finitely many partitions.")
    new_parts = ("in such a way that each partition may contain infinitely many worlds, but\n"
                 "there are only finitely many partitions.")
    assert s.count(old_parts) == 1
    s = s.replace(old_parts, new_parts, 1)

    old_box = ("To see how this would go, first imagine we have no accessibility\n"
               "relation. $\\mSat{M}{\\Box !B}[w]$ iff for some $v \\in W$,\n"
               "$\\mSat{M}{\\Box !B}[v]$,")
    new_box = ("To see how this would go, first imagine we have a universal accessibility\n"
               "relation. $\\mSat{M}{\\Box !B}[w]$ iff for every $v \\in W$,\n"
               "$\\mSat{M}{!B}[v]$,")
    assert s.count(old_box) == 1
    s = s.replace(old_box, new_box, 1)

    old_val = r"$[w] \in V^*$ by definition"
    new_val = r"$[w] \in V^*(p)$ by definition"
    assert s.count(old_val) == 1
    return s.replace(old_val, new_val, 1)
