"""Three exact, auditable source views for OLP-0339 mathematical defects."""
from __future__ import annotations


def repaired_olp0339_source(text: str) -> str:
    source_inf = r'''\begin{multline*}
\lexists[u][(\lforall[x][\lforall[y][(\eq[u(x)][u(y)] \lif 
      \eq[x][y])]] \land {} \\\lexists[y][(X(y) \land \lforall[x][(X(x)
      \lif \eq/[y][u(x)])]])]
\end{multline*}'''
    target_inf = r'''\begin{multline*}
\lexists[u][(\lforall[x][(X(x) \lif X(u(x)))] \land {}
    \lforall[x][\lforall[y][(\eq[u(x)][u(y)] \lif
      \eq[x][y])]] \land {} \\
    \lexists[y][(X(y) \land \lforall[x][(X(x)
      \lif \eq/[y][u(x)])])])]
\end{multline*}'''
    source_count = r'''\begin{multline*}
\lexists[z][\lexists[u][(X(z) \land 
    \lforall[x][(X(x) \lif X(u(x)))] \land {} \\ \lforall[Y][((Y(z) \land
      \lforall[x][(Y(x) \lif Y(u(x)))]) \lif X = Y])]])
\end{multline*}'''
    target_count = r'''\begin{multline*}
\lnot\lexists[x][X(x)] \lor {} \\
\lexists[z][\lexists[u][(X(z) \land
    \lforall[x][(X(x) \lif X(u(x)))] \land {} \\
    \lforall[Y][((Y(z) \land
      \lforall[x][(Y(x) \lif Y(u(x)))]) \lif X \subseteq Y)])]]
\end{multline*}'''
    source_aleph_one = r'''$\fn{Aleph_1}(X) \ident \lforall[Y][(Y \subseteq X \lif
  (\lnot\fn{Inf}(Y) \lor \fn{Aleph}_0(Y)))] \land \lnot
\fn{Aleph}_0(X)$'''
    target_aleph_one = r'''$\fn{Aleph_1}(X) \ident \lnot \fn{Count}(X) \land
  \lforall[Y][((Y \subseteq X \land \lnot \fn{Count}(Y))
  \lif \cardeq{X}{Y})]$'''
    for old, new in (
        (source_inf, target_inf),
        (source_count, target_count),
        (source_aleph_one, target_aleph_one),
    ):
        assert text.count(old) == 1, (old[:50], text.count(old))
        text = text.replace(old, new)
    return text
