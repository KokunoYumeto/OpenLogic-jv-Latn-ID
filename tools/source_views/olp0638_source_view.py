"""Bounded comparison view for Cantor's binary-interleaving argument."""


def repaired_olp0638_source(s: str) -> str:
    repairs = (
        ("Write them in binary notation, so that we\nhave infinite sequences",
         "Write them in binary notation, choosing for each number below one an expansion that is not eventually all ones, and choosing the all-ones expansion for one. Thus we\nhave infinite sequences"),
        ("Now $f$ is !!a{injection}, since if",
         "Every interleaved expansion is canonical: it has infinitely many zeros unless both inputs are one, in which case it is all ones. Now $f$ is !!a{injection}, since if"),
        (r"0.\dot{1}\dot{0}", r"0.00\dot{1}\dot{0}"),
        (r"0.1010101010\ldots", r"0.0010101010\ldots"),
        (r"0.\dot{1}\dot{1}", r"0.0\dot{1}"),
        (r"0.111111\ldots", r"0.011111\ldots"),
        ("= 1$. So, when we say", "= 0.1$. So, when we say"),
        (r"$1.000\ldots$", r"$0.1000\ldots$"),
        ("recurring decimal expansions", "recurring binary expansions"),
    )
    expected_counts = (1, 1, 3, 1, 2, 1, 1, 1, 1)
    for (wrong, right), expected in zip(repairs, expected_counts):
        assert s.count(wrong) == expected, (wrong, s.count(wrong), expected)
        s = s.replace(wrong, right)
    return s
