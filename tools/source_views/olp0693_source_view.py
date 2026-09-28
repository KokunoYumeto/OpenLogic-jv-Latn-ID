"""Give the tN3i typing-rule table its own cross-reference label."""
def repaired_olp0693_source(s: str) -> str:
    wrong = r"\ollabel{tab:tN2ip}"
    assert s.count(wrong) == 1
    return s.replace(wrong, r"\ollabel{tab:tN3ip}", 1)
