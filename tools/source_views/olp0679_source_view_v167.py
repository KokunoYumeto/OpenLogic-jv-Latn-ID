"""Post-seal bounded fairness view for the OLP-0679 truth lemma.

Builds on, but does not alter, the sealed initial OLP-0679 source view.
"""

from olp0679_source_view import repaired_olp0679_source


def repaired_olp0679_source_v167(s: str) -> str:
    s = repaired_olp0679_source(s)
    repairs = (
        ("unless $i$ is\nthe smallest index in $\\Pi_n \\Sequent \\Lambda_n$.",
         "unless $i$ is\nthe smallest non-atomic formula index in $\\Pi_n \\Sequent \\Lambda_n$."),
        ("Since the smallest\nindex increases in topmost sequents added at each stage,",
         "Since the smallest non-atomic formula\nindex increases in topmost sequents added at each stage,"),
        ("and $i$ is\nthe smallest index. At stage $n+1$",
         "and $i$ is\nthe smallest non-atomic formula index. At stage $n+1$"),
        ("!A^i$ and $i$ is the smallest index. And if $!A \\in \\Xi$",
         "!A^i$ and $i$ is the smallest non-atomic formula index. And if $!A \\in \\Xi$"),
        ("!A^i$ and $i$~is the smallest\nindex.",
         "!A^i$ and $i$~is the smallest non-atomic formula\nindex."),
        (r"$\Pi_{n+1} = \Pi_n', !B^k, !C^{k+1}$",
         r"$\Pi_{n+1} = \Pi_n', !B^{k+1}, !C^{k+2}$"),
        (r"$\Lambda_{n+1} = \Lambda_n', !B^k$",
         r"$\Lambda_{n+1} = \Lambda_n', !B^{k+1}$"),
        (r"$\Lambda_{n+1} = \Lambda_n',\n  !C^k$".replace(r"\n", "\n"),
         r"$\Lambda_{n+1} = \Lambda_n',\n  !C^{k+1}$".replace(r"\n", "\n")),
        (r"$\Pi_{n+1} = \Pi_n', !B(c)^k$",
         r"$\Pi_{n+1} = \Pi_n', !B(c)^{k+1}$"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
