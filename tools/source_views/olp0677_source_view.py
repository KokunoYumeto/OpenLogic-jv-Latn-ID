"""Bounded comparison view for normalization segment-definition repairs."""


def repaired_olp0677_source(s: str) -> str:
    repairs = (
        ("$A_{i+1}$ is the conclusion of\n  that inference.",
         "$!A_{i+1}$ is the conclusion of\n  that inference."),
        ("length~$1$ does have to be the conclusions of !!{introduction} rules\n"
         "to count as a cut.",
         "length~$1$ does have to be the conclusion of an !!{introduction} rule\n"
         "or of~\\FalseInt to count as a cut."),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
