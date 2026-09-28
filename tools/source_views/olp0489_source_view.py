"""Bounded comparison view for public-announcement language corrections."""


def repaired_olp0489_source(s: str) -> str:
    old_section = "% Section: language-epistemic-logic"
    new_section = "% Section: public-announcement-logic-lang"
    old_list = (r"  \iftag{prvIf}{\ycomma $\lif$ (!!{conditional})}{}%"
                "\n" r"  \item The knowledge operator")
    new_list = (r"  \iftag{prvIf}{\ycomma $\lif$ (!!{conditional})}{}%"
                "\n" r"  \iftag{prvIff}{\ycomma $\liff$ (!!{biconditional})}{}."
                "\n" r"  \item The knowledge operator")
    old_quote = "truthfully announced, $!B$~holds. It"
    new_quote = "truthfully announced, $!B$~holds.'' It"
    old_spelling = "changes in knowlege using"
    new_spelling = "changes in knowledge using"
    assert s.count(old_section) == s.count(old_list) == s.count(old_quote) == s.count(old_spelling) == 1
    return (s.replace(old_section, new_section, 1)
             .replace(old_list, new_list, 1)
             .replace(old_quote, new_quote, 1)
             .replace(old_spelling, new_spelling, 1))
