"""Exact frozen-source views for three OLP-0340 formula/proof defects."""
from __future__ import annotations


def repaired_olp0340_source(text: str) -> str:
    source_pow = r'''\begin{multline*}
  \fn{Pow}(Y, R, X) \ident \\
  \lforall[Z][(Z \subseteq X \lif \lexists[x][(Y(x) \land
    \fn{Codes}(x, R, Z))])] \land {} \\ \lforall[x][(Y(x) \lif
  \lforall[Z][(\fn{Codes}(x, R, Z) \lif Z \subseteq X)]]
\end{multline*}'''
    target_pow = r'''\begin{multline*}
  \fn{Pow}(Y, R, X) \ident \\
  \lforall[Z][(Z \subseteq X \lif \lexists[x][(Y(x) \land
    \fn{Codes}(x, R, Z))])] \land {} \\
  \lforall[x][(Y(x) \lif
    \lforall[Z][(\fn{Codes}(x, R, Z) \lif Z \subseteq X)])]
\end{multline*}'''
    source_domain = r'''\begin{multline*}
  \Sat{M}{\lexists[X][\lexists[Y][\lexists[R][(\fn{Aleph}_0(X) \land \fn{Pow}(Y, R, X) \land \\
          \lexists[u][(\lforall[x][\lforall[y][(\eq[u(x)][u(y)] \lif \eq[x][y])]] \land {} \\\lforall[y][(Y(y) \lif \lexists[x][\eq[y][u(x)]])])])]]]}.
        \end{multline*}'''
    target_domain = r'''\begin{multline*}
  \Sat{M}{\lexists[Y][(\lforall[x][Y(x)] \land \fn{Cont}(Y))]}.
\end{multline*}'''
    source_proof = "and subsets of $s(Z)$ via"
    target_proof = "and subsets of $s(X)$ via"
    for old, new in (
        (source_pow, target_pow),
        (source_domain, target_domain),
        (source_proof, target_proof),
    ):
        assert text.count(old) == 1, (old[:60], text.count(old))
        text = text.replace(old, new)
    return text
