"""Bounded variable repair and localized axiom names in math text."""


def repaired_olp0562_source(s: str) -> str:
    wrong = r'(\exists x \in b)'
    right = r'(\exists x \in B)'
    assert s.count(wrong) == 1, s.count(wrong)
    s = s.replace(wrong, right, 1)
    names = {
        r'\emph{Foundation}\Rightarrow\emph{Regularity}':
            r'\emph{Landhesan}\Rightarrow\emph{Regularitas}',
        r'\emph{Regularity}\Rightarrow\emph{Foundation}':
            r'\emph{Regularitas}\Rightarrow\emph{Landhesan}',
    }
    for english, javanese in names.items():
        assert s.count(english) == 1, (english, s.count(english))
        s = s.replace(english, javanese, 1)
    return s
