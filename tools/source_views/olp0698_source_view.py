"""Four bounded corrections to sequent-rule admissibility exposition."""
def repaired_olp0698_source(s: str) -> str:
    repairs = (
        (r"\UnaryInf$!A \land !B \Gamma \fCenter \Delta$", r"\UnaryInf$!A \land !B, \Gamma \fCenter \Delta$"),
        (r"\RightLabel{\LeftR{\liff}}" + "\n" + r"\BinaryInf$\Gamma \fCenter \Delta, !A \liff !B$", r"\RightLabel{\LeftR{\liff}}" + "\n" + r"\BinaryInf$!A \liff !B, \Gamma \fCenter \Delta$"),
        ("Add the !!{formula}~$!A$ to the succedent of every sequent", "First rename the eigenparameters in their corresponding proof subtrees\nso that they are fresh for the added formula; this preserves the end-sequent\nand the height. Add the !!{formula}~$!A$ to the succedent of every sequent"),
        ("We prove this by induction on~$n$. If $n=0$,", "First choose the eigenparameters fresh for the added formula by the\n  subtree renaming just described. We prove this by induction on~$n$. If $n=0$,"),
        ("atomic $!C$ occurs in both $\\Gamma$ and~$\\Delta$), and so is $\\Gamma", "atomic $!C$ occurs in both $\\Gamma$ and~$\\Delta$, or falsity occurs in\n  the antecedent), and so is $\\Gamma"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, wrong
        s = s.replace(wrong, right, 1)
    return s
