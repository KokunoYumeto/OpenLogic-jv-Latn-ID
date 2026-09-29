"""Three bounded repairs to rule interpretation, retaining frozen English."""
def repaired_olp0699_source(s: str) -> str:
    repairs = (
        (r"\RightLabel{\RightR{\oplus}}" + "\n" + r"\BinaryInf$!A \oplus !B, \Gamma \fCenter \Delta$",
         r"\RightLabel{\LeftR{\oplus}}" + "\n" + r"\BinaryInf$!A \oplus !B, \Gamma \fCenter \Delta$"),
        ("contains a false !!{formula} on\nthe right or a true !!{formula} on the left",
         "contains a false !!{formula} on\nthe left or a true !!{formula} on the right"),
        ("Why have structural rules at all? Contraction",
         "Why have structural rules at all? For distinct atomic schematic formulas, contraction"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, wrong
        s = s.replace(wrong, right, 1)
    return s
