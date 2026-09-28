"""Bounded type and implication repairs in order-type representation."""


def repaired_olp0556_source(s: str) -> str:
    wrong_map = r'$f \colon \beta \to \tuple {B, \lessdot}$'
    right_map = r'$f \colon \beta \to B$'
    assert s.count(wrong_map) == 1, s.count(wrong_map)
    s = s.replace(wrong_map, right_map, 1)

    marker = "\\begin{align*}\n\t\\alpha \\in \\beta&\\text{ iff }"
    assert s.count(marker) == 1, s.count(marker)
    start = s.index(marker)
    end = s.index("\\end{align*}", start) + len("\\end{align*}")
    block = s[start:end]
    assert block.count(r'\text{ iff }') == 3
    assert block.count(r'\funrestrictionto{f}{\alpha}') == 1
    s = s[:start] + block.replace(r'\text{ iff }', r'\Longrightarrow') + s[end:]

    old_end = r'\olref[basic]{ordissetofsmallerord}.'
    new_end = (
        r'\olref[basic]{ordissetofsmallerord}. Conversely, if the first '
        'well-order is isomorphic to a proper initial segment of the second, '
        'pull that segment\'s endpoint back through the isomorphism. The '
        'segment is isomorphic to the corresponding member of the source '
        'ordinal. By '
        r'\olref[basic]{ordisoidentity}, the first order type equals that '
        'member and hence belongs to the source ordinal.'
    )
    assert s.count(old_end) == 1, s.count(old_end)
    return s.replace(old_end, new_end, 1)
