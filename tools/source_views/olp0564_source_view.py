"""Bounded rank-definition and proof repairs, plus axiom-name localization."""


def repaired_olp0564_source(s: str) -> str:
    old_intuition = (
        'the rank of $A$ is the first moment\n'
        'at which $A$ is formed.'
    )
    new_intuition = (
        'the rank of $A$ is the least stage whose elements suffice\n'
        'to form $A$.'
    )
    assert s.count(old_intuition) == 1, s.count(old_intuition)
    s = s.replace(old_intuition, new_intuition, 1)

    wrong = r'now a simple transfinite induction shows that $x \notin V_\alpha$.'
    right = r'now a simple transfinite induction shows that $\setrank{x} \in \alpha$.'
    assert s.count(wrong) == 1, s.count(wrong)
    s = s.replace(wrong, right, 1)

    axiom_names = {
        r'\emph{Regularity} \Rightarrow \emph{Foundation}':
            r'\emph{Regularitas} \Rightarrow \emph{Landhesan}',
        r'\text{Regularity}': r'\text{Regularitas}',
    }
    for english, javanese in axiom_names.items():
        expected = 2 if english == r'\text{Regularity}' else 1
        assert s.count(english) == expected, (english, s.count(english))
        s = s.replace(english, javanese)
    return s
