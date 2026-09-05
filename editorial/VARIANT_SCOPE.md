# Edition, script, register, and notation scope

The primary semantic edition is `openlogic-jv-Latn-ID`: Javanese in Latin
script, using formal written ngoko for university-level and independent study.
Its mathematical meaning comes directly from the frozen English OpenLogic
source. Indonesian material may clarify spelling or dictionary metalanguage,
but it is not an intermediate semantic source.

This register choice is an editorial inference from the academic prose
recorded as canon passage JV-P002. The official Latin spelling evidence in
JV-P005 supports the script and orthographic baseline. Neither source licenses
a claim that this is the only valid Javanese register, nor does the present
evidence justify separate regional semantic editions. Terminology remains
reviewable through the decision register rather than through an unpublished
review gate.

International mathematical notation, Arabic digits, and source-controlled
formula structure remain unchanged. The Latin edition is left-to-right and
does not need bidirectional layout. Localizing numerals or operators would
create a new notation profile and requires separate evidence and exact formula
QA; it is outside the current edition.

A future Javanese-script artifact can be valuable, but it must be represented
as a separately tested `script_projection` whose parent is
`openlogic-jv-Latn-ID`. It must not increase the semantic-translation unit
count. Acceptance requires deterministic Latin-to-Javanese-script mapping,
an explicit exception table for technical loans and symbols, font and shaping
tests, line-break and pagination review, searchable/copyable text checks, and
round-trip comparison against the accepted Latin semantic text. Mathematical
notation stays left-to-right inside that artifact. If those conditions are
met, the projection should have its own locale/catalogue identity and release
artifact even when both editions are produced by one configurable build.

Conversational, krama, pronunciation, regional, or Indonesian bridge versions
are optional companions. Each needs a stated audience, evidence for its
register or region, its own decision and QA surface, and a distinct coverage
claim. None interrupts or duplicates the 722-unit primary translation lane.
