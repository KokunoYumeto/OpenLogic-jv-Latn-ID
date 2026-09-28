"""Replace the invalid atomic quotient by finite subformula filtration."""


def repaired_olp0510_source(s: str) -> str:
    old = r"""\begin{proof}
  Assume $\mModel{M}=\tuple{W, R, V}$ is such that $\mSat/{M}{!A}$ and $P$ 
  is the set of !!{propositional variable}s occurring in~$!A$. Define
  $\mModel{M'}=\tuple{W', R', V'}$ by letting $W' = \Setabs{[w]}{w \in W}$ 
  where $[w] = \Setabs{p \in P}{w \in V(p)}$, $R'$ be the subset relation, 
  and $V'(p)=\Setabs{[w]}{p \in [w]}$. It should be clear that $W'$ is a 
  finite set and that $\mModel{M'}$ is !!a{relational model}.

  It can be shown, by induction on~$!A$, that 
  \[
    \mSat{M}{!A}[w] \text{ iff } \mSat{M'}{!A}[{[w]}]
  \]
  for all !!{formula}s $!A$ with only !!{propositional variable}s
  from~$P$. This is left as an exercise for the reader.
\end{proof}"""
    new = r"""\begin{proof}
  Assume $\mModel{M}=\tuple{W, R, V}$ satisfies $\mSat/{M}{!A}$ and $S$
  is the set of all !!{subformula}s of~$!A$, after expanding connective
  abbreviations. Define
  $\mModel{M'}=\tuple{W', R', V'}$ with $W' = \Setabs{[w]}{w \in W}$,
  where $[w] = \Setabs{!B \in S}{\mSat{M}{!B}[w]}$, $R'$ is the subset
  relation, and $V'(p)=\Setabs{[w]}{p \in [w]}$.
  We have $|W'| \le 2^{|S|}$. Subset inclusion is a partial order and
  atomic valuation is monotone along it. Thus $\mModel{M'}$ is a finite
  !!a{relational model}.

  By induction on formulas in the subformula set, we can show that
  \[
    \mSat{M}{!B}[w] \text{ yen lan mung yen } \mSat{M'}{!B}[{[w]}]
  \]
  for all !!{formula}s $!B \in S$. The atomic, falsity, conjunction and
  disjunction cases follow from definitions and the induction hypotheses.
  An implication true in the original model belongs to the current truth
  set and hence to every larger truth set. At each representative world,
  reflexivity and induction force the consequent whenever the antecedent
  is true. Conversely, an accessible counterworld in the original model
  has a larger truth set by persistence, and induction retains its true
  antecedent and false consequent in the finite model. Negation follows
  by the corresponding absence of an accessible world satisfying its
  operand. Details of the induction remain an exercise. The original
  formula is in this subformula set, so its counterworld yields a finite
  counterworld as required.
\end{proof}"""
    assert s.count(old) == 1
    s = s.replace(old, new, 1)
    old = r"""Finish the proof of \olref[int][sc][dec]{thm:decidability} by showing
that $\mSat{M,w}{!A}$ iff $\mSat{M',[w]}{!A}$ for all !!{formula}s~$!A$
with only propositional variables from~$P$. """
    new = r"""Complete the proof of \olref[int][sc][dec]{thm:decidability} by showing
that $\mSat{M}{!B}[w]$ iff $\mSat{M'}{!B}[{[w]}]$ for all
!!{formula}s~$!B \in S$."""
    assert s.count(old) == 1
    s = s.replace(old, new, 1)
    old = "From \\olref{thm:decidability} it follows that there is an algorithm to\ndecide whether~$\\Entails !A$."
    new = "From \\olref{thm:decidability}, an algorithm decides whether~$\\Entails !A$ by checking all partial orders and relevant monotone atomic valuations on models with at most $2^{|S|}$ worlds."
    assert s.count(old) == 1
    return s.replace(old, new, 1)
