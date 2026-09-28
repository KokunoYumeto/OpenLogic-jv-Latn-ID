"""Bounded comparison view for OLP-0433's missing final disjunction step."""


def repaired_olp0433_source(s: str) -> str:
    old = (r"7. & $\Log{K} \Proves \Diamond(!A\lor!B) \lif (\Diamond!B \lor \Diamond!A)$ & \PL, 6. \\" 
           + "\n  " + r"\end{derivation}")
    new = (r"7. & $\Log{K} \Proves \Diamond(!A\lor!B) \lif (\Diamond!B \lor \Diamond!A)$ & \PL, 6. \\" 
           + "\n    " + r"8. & $\Log{K} \Proves \Diamond(!A \lor!B) \lif (\Diamond!A \lor \Diamond!B)$ & \PL, 7"
           + "\n  " + r"\end{derivation}")
    assert s.count(old) == 1
    return s.replace(old, new, 1)
