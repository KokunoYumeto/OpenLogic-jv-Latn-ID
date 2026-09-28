"""Bounded decidability-argument comparison view for S5."""


def repaired_olp0457_source(s: str) -> str:
    old_scope = ("The finite model property gives us an easy way to show that systems of\n"
                 "modal logic given by schemas are \\emph{decidable}")
    new_scope = ("For effectively axiomatized systems whose relevant finite\n"
                 "countermodels can be effectively enumerated, the finite model\n"
                 "property can yield\n"
                 "\\emph{decidability}")
    assert s.count(old_scope) == 1
    s = s.replace(old_scope, new_scope, 1)
    old_models = "and all the models containing $1$, $2$, \\dots worlds"
    new_models = "and all the finite universal models containing $1$, $2$, \\dots worlds"
    assert s.count(old_models) == 1
    return s.replace(old_models, new_models, 1)
