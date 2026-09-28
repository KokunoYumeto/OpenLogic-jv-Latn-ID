"""Bounded corrections to cardinal-exponentiation proof notation and citations."""


def repaired_olp0589_source(s: str) -> str:
    repairs = (
        (
            r"(f_{\cardfont{b}} \times f_\cardfont{c})",
            r"\tuple{f_{\cardfont{b}}, f_\cardfont{c}}",
        ),
        (
            r"\funfromto{\cardfont{b} \cardtimes \cardfont{c}}{\cardfont{a}}",
            r"\funfromto{\cardfont{b} \times \cardfont{c}}{\cardfont{a}}",
        ),
        (
            r"\olref[opps]{lem:SizePowerset2Exp}",
            r"\olref[opps]{cantorcor}",
        ),
        (
            r"\olref[card-arithmetic][opps]{lem:SizePowerset2Exp}",
            r"\olref[card-arithmetic][opps]{cantorcor}",
        ),
        (r"$n \in \omega$", r"$0<n \in \omega$"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
