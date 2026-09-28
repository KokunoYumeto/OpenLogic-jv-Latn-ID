"""Bounded comparison view for three frozen-source defects in OLP-0421."""


def repaired_olp0421_source(s: str) -> str:
    old = "% Chapter: frame-correspondence"
    new = "% Chapter: frame-definability"
    assert s.count(old) == 1
    s = s.replace(old, new, 1)

    old = "let $W = \\{w\\}$ and\n$V(p) = \\emptyset$. Then $R$ is not reflexive"
    new = "let $W = \\{w\\}$, $R = \\emptyset$, and\n$V(p) = \\emptyset$. Then $R$ is not reflexive"
    assert s.count(old) == 1
    s = s.replace(old, new, 1)

    old = "where worlds $u$ and $v$ are related by $R$: i.e., both $Ruv$"
    new = "where worlds $u$ and $v$ are related by $R = \\{(u,v),(v,u)\\}$: i.e., both $Ruv$"
    assert s.count(old) == 1
    s = s.replace(old, new, 1)
    return s
