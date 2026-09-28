"""Bounded valuation-domain comparison view for filtration examples."""


def repaired_olp0454_source(s: str) -> str:
    old_even = "$V(p) = \\Setabs{2n}{n \\in\n    \\Nat}$"
    new_even = "$V(p) = \\Setabs{2n}{n \\in\n    \\PosInt}$"
    assert s.count(old_even) == 1
    s = s.replace(old_even, new_even, 1)

    old_tree = ("$V(p) = \\Setabs{\\sigma\n    0}{\\sigma \\in \\Bin^*}$ and "
                "$V(q) = \\Setabs{\\sigma 1}{\\sigma \\in\n"
                "    \\Bin^* \\setminus \\{1\\}}$")
    new_tree = ("$V(p) = \\Setabs{\\sigma\n    0}{\\sigma \\in \\Bin^*} \\cap W$ and "
                "$V(q) = \\Setabs{\\sigma 1}{\\sigma \\in\n"
                "    \\Bin^* \\setminus \\{1\\}} \\cap W$")
    assert s.count(old_tree) == 1
    return s.replace(old_tree, new_tree, 1)
