"""Apply SLC's Javanese vocabulary to the reused textbook sections."""

import re


VOCABULARY = {
    "input": "masukan", "output": "asil", "blank": "simbol kosong",
    "domain": "ranah", "valid": "sah", "lemma": "lema",
    "soundness": "kesahihan", "term": "terma", "subterm": "subterma",
    "tuple": "tupel",
    "enumerable": "bisa dietung", "validitas": "kesahan",
    "term-term": "terma-terma", "input-output": "saka masukan menyang asil",
}
WORDS = re.compile(
    r"(?<![\\\w:-])"
    r"(input-output|term-term|input|output|blank|domain|validitas|valid|lemma|"
    r"soundness|term|subterm|tuple|enumerable|natural)"
    r"(ne|né|e|é)?(?=$|---|:(?:[}\s]|$)|[^\w:-])",
    re.I,
)
# IDs, paths, token keys, URLs and references are part of OLP's source interface.
MARKUP = re.compile(
    r"!!(?:\^)?(?:a)?\{[^{}\n]*\}"
    r"|\\usetoken\{[^{}\n]*\}\{[^{}\n]*\}"
    r"|\\(?:olimport|olref|Olref|ollabel|label|cref|Cref|ref|index|gls|glspl|href|url|cite[a-z]*)"
    r"\*?(?:\[[^\]\n]*\])*\{[^{}\n]*\}"
    r"|\\(?:if|iftag|tagtrue|tagfalse)\{[^{}\n]*\}"
)


def localize(text, path):
    count = 0
    number_term = "asli" if path.startswith("content/sets-functions-relations/") else "alami"

    def translate(match):
        nonlocal count
        stem, suffix = match.groups()
        key = stem.casefold()
        value = number_term if key == "natural" else VOCABULARY[key]
        if key == "blank" and re.search(r"\b(?:kothak|simbol)\s+$", match.string[:match.start()], re.I):
            value = "kosong"
        if suffix:
            value += "né" if value[-1] in "aeiou" else "é"
        if stem.isupper():
            value = value.upper()
        elif stem[0].isupper():
            value = value[0].upper() + value[1:]
        count += 1
        return value

    def localize_code(code):
        parts = []
        start = 0
        for match in MARKUP.finditer(code):
            parts.append(WORDS.sub(translate, code[start:match.start()]))
            parts.append(match[0])
            start = match.end()
        parts.append(WORDS.sub(translate, code[start:]))
        return "".join(parts)

    result = []
    for line in text.splitlines(keepends=True):
        comment = re.search(r"(?<!\\)%", line)
        split = comment.start() if comment else len(line)
        result.append(localize_code(line[:split]) + line[split:])
    return "".join(result), count
