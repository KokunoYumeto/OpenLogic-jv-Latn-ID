"""Bounded comparison view for consistency's model scope and proof citation."""


def repaired_olp0440_source(s: str) -> str:
    old_scope = ("If a set is\ninconsistent, its !!{formula}s cannot all be true in a model at a\n"
                 "world. For the completeness theorem we prove the converse: every\n"
                 "consistent set is true at a world in a model, namely in the ``canonical\n"
                 "model.''")
    new_scope = ("If a set is\ninconsistent relative to a system, its !!{formula}s cannot all be true\n"
                 "at a world in a model of that system. For the completeness theorem we\n"
                 "prove the converse: every set consistent relative to the system is true\n"
                 "at a world in a model of that system, namely in the ``canonical\n"
                 "model.''")
    assert s.count(old_scope) == 1
    s = s.replace(old_scope, new_scope, 1)
    old_citation = "Then by\n  \\olref{prop:consistencyfacts-b}, both"
    new_citation = "Then by\n  the definition of consistency, both"
    assert s.count(old_citation) == 1
    return s.replace(old_citation, new_citation, 1)
