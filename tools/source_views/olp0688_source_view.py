"""Three constructor-argument corrections in the proof-term definition."""
def repaired_olp0688_source(s: str) -> str:
    for wrong, right in (
        (r"c^\land(N, m)", r"c^\land(N, M)"),
        (r"c^{\lor{!B}}_1:!A \lor !B", r"c^{\lor{!B}}_1(N):!A \lor !B"),
        (r"\inj[!A]{i}{!M}", r"\inj[!A]{i}{N}"),
    ):
        assert s.count(wrong) == 1
        s = s.replace(wrong, right, 1)
    return s
