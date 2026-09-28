"""Cover zero-indexed branches and specify the extension-length induction."""


def repaired_olp0507_source(s: str) -> str:
    repairs = (
        (r"Let $\tuple{!B_1, !C_1}$, $\tuple{!B_2, !C_2}$",
         r"Let $\tuple{!B_0, !C_0}$, $\tuple{!B_1, !C_1}$"),
        (r"on~$\sigma$.", r"on the length of the suffix appended to~$\sigma$."),
        (r"\text{if $\Delta(\sigma)", r"\text{yen $\Delta(\sigma)"),
        (r"\text{otherwise}", r"\text{yen ora}"),
    )
    for old, new in repairs:
        assert s.count(old) == 1
        s = s.replace(old, new, 1)
    return s
