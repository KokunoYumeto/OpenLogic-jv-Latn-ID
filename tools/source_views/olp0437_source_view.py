"""Bounded comparison view for axiom/system macro confusions in OLP-0437."""


def repaired_olp0437_source(s: str) -> str:
    fixes = (
        ("\\Log{KT} \\Proves\n  \\Log{D}", "\\Log{KT} \\Proves\n  \\Ax{D}"),
        (r"\Log{KTB} \Proves/ \Log{4}", r"\Log{KTB} \Proves/ \Ax{4}"),
        (r"\Log{KTB} \Proves/ \Log{5}", r"\Log{KTB} \Proves/ \Ax{5}"),
    )
    for old, new in fixes:
        assert s.count(old) == 1
        s = s.replace(old, new, 1)
    return s
