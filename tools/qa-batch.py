import pathlib,hashlib,json,re,datetime,collections
R=pathlib.Path(__file__).resolve().parent.parent
S=R/'evidence'
def sha(data): return hashlib.sha256(data).hexdigest()
units=[json.loads(x) for x in (S/'SOURCE_MANIFEST.jsonl').read_text(encoding='utf-8-sig').splitlines()]
passages={x['passage_id']:x for x in map(json.loads,(S/'CANON_PASSAGES.jsonl').read_text(encoding='utf-8').splitlines())}
def chunks(txt):
    return [m for m in re.finditer(r'\S[\s\S]*?(?=\n[ \t]*\n|\Z)',txt) if m.group().strip()]
def math(txt):
    pattern=r'\$(?:\\.|[^$])*\$|\\\[[\s\S]*?\\\]|\\begin\{(?:align|multline|equation|gather)\*?\}[\s\S]*?\\end\{(?:align|multline|equation|gather)\*?\}'
    vals=[]
    for m in re.finditer(pattern,txt):
        t=m[0]
        pos=0
        while True:
            found=re.search(r'\\(text|intertext)\{',t[pos:])
            if not found:break
            start=pos+found.start()
            command=found[1]
            prefix='\\'+command+'{'
            content_start=start+len(prefix)
            end=content_start;depth=1
            while end<len(t) and depth:
                if t[end]=='{' and t[end-1]!='\\':depth+=1
                elif t[end]=='}' and t[end-1]!='\\':depth-=1
                end+=1
            assert depth==0
            contents=t[content_start:end-1]
            preserved=''.join(re.findall(r'!![\^a]*\{[^}]+\}s?|\$(?:\\.|[^$])*\$',contents))
            replacement=prefix+preserved+'}'
            t=t[:start]+replacement+t[end:];pos=start+len(replacement)
        vals.append(re.sub(r'\s+','',t))
    return vals
def protected(txt):
    pat=r'\\(?:olfileid|ollabel|olref|olimport|olasset|oliflabeldef|cite\w*|href|url|documentclass)(?:\[[^\]]*\])*(?:\{[^{}]*\})+'
    vals=re.findall(pat,txt)
    return [re.sub(r'(\\href\{[^}]*\})\{[\s\S]*\}',r'\1',x) for x in vals]
def tokens(txt):return re.findall(r'!![\^a]*\{[^}]+\}s?',txt)
rows=[];align=[];failures=[]
for u in units:
    dest=R/'translation'/u['source_path']
    if not dest.exists():continue
    src=R/'upstream'/u['source_path'];b=src.read_bytes();tb=dest.read_bytes()
    assert sha(b)==u['source_sha256']
    # Raw file hashes remain authoritative. Paragraph analysis and segment
    # hashes normalize line endings, because frozen OLP-0037 uses CRLF.
    a=b.decode().replace('\r\n','\n').replace('\r','\n')
    t=tb.decode().replace('\r\n','\n').replace('\r','\n')
    protected_source=a
    if u['unit_id']=='OLP-0037':
        assert protected_source.count(r'\citet[pp.~165--6]{Potter2004}')==1
        protected_source=protected_source.replace(r'\citet[pp.~165--6]{Potter2004}',r'\citet[kaca~165--6]{Potter2004}')
    ac=chunks(a);tc=chunks(t)
    math_source=a
    # OLFUN-003: the frozen prose switches from input n to x. The target
    # consistently uses x; formulas and every other mathematical span stay exact.
    if u['unit_id']=='OLP-0021':
        defect='Given a natural number~$n$, $g$ will output'
        assert math_source.count(defect)==1
        math_source=math_source.replace(defect,'Given a natural number~$x$, $g$ will output')
    # OLSIZ-001 through OLSIZ-010: normalize only the ten confirmed
    # Size-of-Sets defects adopted in the translated body. The exact frozen
    # English bytes and manifest hashes remain unchanged.
    if u['unit_id']=='OLP-0029':
        omitted_value=r'0 & 1 & -1 & 2 & -2 & 3 & \dots'
        assert math_source.count(omitted_value)==1
        math_source=math_source.replace(omitted_value,r'0 & 1 & -1 & 2 & -2 & 3 & -3 & \dots')
    if u['unit_id']=='OLP-0032':
        duplicated_pair=r'$\tuple{2,m}$, $\tuple{2,m}$'
        assert math_source.count(duplicated_pair)==1
        math_source=math_source.replace(duplicated_pair,r'$\tuple{2,m}$, $\tuple{3,m}$')
    if u['unit_id']=='OLP-0034':
        assert math_source.count(r'$s_{k}$')==1
        assert math_source.count(r'$s_{k}(n) = 1$')==1
        assert math_source.count(r'$s_k(n) = 0$')==1
        math_source=math_source.replace(r'$s_{k}$',r'$s$')
        math_source=math_source.replace(r'$s_{k}(n) = 1$',r'$s(n) = 1$')
        math_source=math_source.replace(r'$s_k(n) = 0$',r'$s(n) = 0$')
        finite_string=r"h(n) = \underbrace{000\dots0}_{\text{$n$ $0$'s}}"
        assert math_source.count(finite_string)==1
        math_source=math_source.replace(finite_string,r"h(n) = \underbrace{00\dots0}_{\text{$n$ $0$'s}}111\dots")
    if u['unit_id']=='OLP-0035':
        assert math_source.count(r'$g(x) = y$')==2
        math_source=math_source.replace(r'$g(x) = y$',r'$f(x) = y$')
    if u['unit_id']=='OLP-0036':
        wrong_domain='$x \\in\n  \\overline{A}$'
        assert math_source.count(wrong_domain)==1
        math_source=math_source.replace(wrong_domain,'$x \\in\n  A$')
    # OLP-0039: the notation/array require s_n(m) to mean the mth digit
    # of the nth string and require flipping 0 to 1. Normalize only these
    # two confirmed source prose defects for source-target math comparison.
    if u['unit_id']=='OLP-0039':
        index_defect='Let $s_n(m)$ be the $n$th digit of\nthe $m$th string in this list.'
        flip_defect='changing every $1$ to a $0$ and\nevery $1$ to a~$0$.'
        assert math_source.count(index_defect)==1
        assert math_source.count(flip_defect)==1
        math_source=math_source.replace(index_defect,'Let $s_n(m)$ be the $m$th digit of\nthe $n$th string in this list.')
        math_source=math_source.replace(flip_defect,'changing every $1$ to a $0$ and\nevery $0$ to a~$1$.')
    if u['unit_id']=='OLP-0040':
        assert math_source.count(r'$s_{k}$')==1
        assert math_source.count(r'$s_{k}(n) = 1$')==1
        assert math_source.count(r'$s_k(n) = 0$')==1
        math_source=math_source.replace(r'$s_{k}$',r'$s$')
        math_source=math_source.replace(r'$s_{k}(n) = 1$',r'$s(n) = 1$')
        math_source=math_source.replace(r'$s_k(n) = 0$',r'$s(n) = 0$')
    # OLP-0043: the surrounding sentence and displayed definition both require
    # s-r to be nonnegative; one intervening source phrase reverses it to r-s.
    if u['unit_id']=='OLP-0043':
        assert math_source.count('$r - s$')==1
        math_source=math_source.replace('$r - s$','$s - r$')
    # OLP-0047 places six linguistic axiom labels inside align environments.
    # Translate those labels while preserving every formula and alignment token.
    if u['unit_id']=='OLP-0047':
        label_translations={
            r'\emph{Associativity}':(r'\emph{Asosiativitas}',2),
            r'\emph{Commutativity}':(r'\emph{Komutativitas}',1),
            r'\emph{Identities}':(r'\emph{Identitas}',1),
            r'\emph{Additive Inverse}':(r'\emph{Invers Aditif}',2),
            r'\emph{Distributivity}':(r'\emph{Distributivitas}',2),
            r'\emph{Multiplicative Inverse}':(r'\emph{Invers Multiplikatif}',1),
        }
        for english,(javanese,expected) in label_translations.items():
            assert math_source.count(english)==expected
            math_source=math_source.replace(english,javanese)
    # OLP-0048 defines positivity for a real equivalence class but compares
    # it with rational zero. The next sentence and the quotient type require real zero.
    if u['unit_id']=='OLP-0048':
        zero_type_defect=r'\equivrep{f}{}\neq 0_\Rat'
        assert math_source.count(zero_type_defect)==1
        math_source=math_source.replace(zero_type_defect,r'\equivrep{f}{}\neq 0_\Real')
    checks={'paragraph_count':len(ac)==len(tc),'protected_commands':protected(protected_source)==protected(t),'math_sequence':math(math_source)==math(t),'token_sequence':tokens(a)==tokens(t),'environment_sequence':re.findall(r'\\(?:begin|end)\{[^}]+\}',a)==re.findall(r'\\(?:begin|end)\{[^}]+\}',t),'unicode_clean':'\ufffd' not in t and not re.search(r'[\uA980-\uA9DF]',t),'no_placeholder':not re.search(r'\b(?:TODO|TBD|TRANSLATE_ME)\b',t)}
    command_source=a
    if u['unit_id']=='OLP-0034':
        finite_string=r"h(n) = \underbrace{000\dots0}_{\text{$n$ $0$'s}}"
        assert command_source.count(finite_string)==1
        command_source=command_source.replace(finite_string,r"h(n) = \underbrace{00\dots0}_{\text{$n$ $0$'s}}111\dots")
    if u['unit_id']=='OLP-0036':
        wrong_domain='$x \\in\n  \\overline{A}$'
        assert command_source.count(wrong_domain)==1
        command_source=command_source.replace(wrong_domain,'$x \\in\n  A$')
    # Source English lexical typography disappears when those words are translated:
    # naive's diaeresis and anti-symmetric's discretionary hyphenation are not
    # mathematical commands. These exact source strings were directly checked.
    if u['unit_id'] in ['OLP-0003','OLP-0010']:
        expected=1 if u['unit_id']=='OLP-0003' else 2
        assert command_source.lower().count('na\\"iv')==expected
        command_source=command_source.replace('Na\\"iv','Naiv').replace('na\\"iv','naiv')
    if u['unit_id']=='OLP-0014':
        assert command_source.count(r'anti-sym\-met\-ric')==1
        command_source=command_source.replace(r'anti-sym\-met\-ric','anti-symmetric')
    if u['unit_id']=='OLP-0042':
        assert command_source.count(r'na\"{i}ve')==2
        command_source=command_source.replace(r'na\"{i}ve','naive')
    if u['unit_id']=='OLP-0043':
        assert command_source.count(r'na\"{i}ve')==1
        assert command_source.count(r'na\"ive')==1
        command_source=command_source.replace(r'na\"{i}ve','naive').replace(r'na\"ive','naive')
    if u['unit_id']=='OLP-0046':
        assert command_source.count(r'na\"ive')==1
        command_source=command_source.replace(r'na\"ive','naive')
    if u['unit_id']=='OLP-0048':
        assert command_source.count(r'na\"{i}ve')==1
        command_source=command_source.replace(r'na\"{i}ve','naive')
        # Apply the same bounded real-zero source correction used by the
        # mathematical-span comparison above. A broad 0_\Rat replacement can
        # hide an unrelated future command change.
        zero_type_defect=r'\equivrep{f}{}\neq 0_\Rat'
        assert command_source.count(zero_type_defect)==1
        command_source=command_source.replace(zero_type_defect,r'\equivrep{f}{}\neq 0_\Real')
    if u['unit_id']=='OLP-0041':
        assert command_source.count(r'na\"ive')==1
        command_source=command_source.replace(r'na\"ive','naive')
    checks['all_command_sequence']=re.findall(r'\\[A-Za-z@]+|\\[^A-Za-z@]',command_source)==re.findall(r'\\[A-Za-z@]+|\\[^A-Za-z@]',t)
    row={'unit_id':u['unit_id'],'source_path':u['source_path'],'source_sha256':sha(b),'translation_sha256':sha(tb),'translation_bytes':len(tb),'checks':checks,'source_paragraphs':len(ac),'target_paragraphs':len(tc),'source_math_count':len(math(a)),'target_math_count':len(math(t)),'status':'structural_pass' if all(checks.values()) else 'defect'}
    rows.append(row)
    if not all(checks.values()):
        failures.append(row)
        print(json.dumps(row))
        for key,fn in [('math_sequence',math),('protected_commands',protected),('token_sequence',tokens)]:
            if not checks[key]:
                aa=fn(math_source if key=='math_sequence' else a);tt=fn(t)
                print(key,[(i,x,tt[i] if i<len(tt) else None) for i,x in enumerate(aa) if i>=len(tt) or x!=tt[i]][:4])
    if len(ac)!=len(tc):continue
    for i,(am,tm) in enumerate(zip(ac,tc),1):
        same=am[0].strip()==tm[0].strip()
        consulted=[] if same else ['JV-P002','JV-P005']
        # These passage sets reflect actual consultation while authoring this batch.
        if not same and (u['unit_id']=='OLP-0001' or 'logika' in tm[0].lower()):consulted+=['JV-P001','JV-P004','JV-P006']
        if not same and re.search(r'!![\^a]*\{element\}',am[0]):consulted+=['JV-P007']
        if not same and any(x in tm[0].lower() for x in ['himpunan','ekstensionalitas','wilangan','rerangken','gabungan','irisan','paradoks','pasangan']):consulted+=['JV-P006']
        if not same and any(x in tm[0].lower() for x in ['buktekna','bukti']):consulted+=['JV-P008']
        if not same and any(x in tm[0].lower() for x in ['relasi','refleksif','simetris','transitif','koneks']):consulted+=['JV-P011','JV-P006']
        if not same and 'fungsi' in tm[0].lower():consulted+=['JV-P012','JV-P006']
        if not same and any(x in tm[0].lower() for x in ['invers','komposisi','parsial','serial','injektif','surjektif','bijektif','citra','!!{injective}','!!{surjective}','!!{bijective}']):consulted+=['JV-P006']
        # Fresh recovered-canon revision of OLP-0021; do not retroactively claim
        # the laptop entries were consulted when earlier units were authored.
        if not same and u['unit_id']=='OLP-0021':
            if 'wilangan' in tm[0].lower():consulted+=['JV-P013']
            if 'ping-pingan' in tm[0].lower():consulted+=['JV-P015']
        if not same and u['unit_id'] in ['OLP-0027','OLP-0028','OLP-0029','OLP-0030','OLP-0031','OLP-0032','OLP-0033','OLP-0034','OLP-0035','OLP-0036','OLP-0037','OLP-0038','OLP-0039','OLP-0040','OLP-0041','OLP-0042','OLP-0043','OLP-0044','OLP-0045','OLP-0046','OLP-0047','OLP-0048']:
            if 'wilangan' in tm[0].lower():consulted+=['JV-P013']
            if any(x in tm[0].lower() for x in ['enumer','didhaptar','dietung','cacah']):consulted+=['JV-P014','JV-P006']
            if 'rambang' in tm[0].lower():consulted+=['JV-P018']
            if 'gunggung' in tm[0].lower():consulted+=['JV-P017']
        if not same and u['unit_id'] in ['OLP-0045','OLP-0046','OLP-0047','OLP-0048'] and 'potongan' in tm[0].lower():consulted+=['JV-P021','JV-P006']
        consulted=list(dict.fromkeys(consulted))
        seg={'segment_id':u['unit_id']+f'-P{i:03d}','unit_id':u['unit_id'],'source_path':u['source_path'],'source_line_start':a.count('\n',0,am.start())+1,'source_line_end':a.count('\n',0,am.end())+1,'translation_line_start':t.count('\n',0,tm.start())+1,'translation_line_end':t.count('\n',0,tm.end())+1,'source_segment_sha256':sha(am[0].encode()),'translation_segment_sha256':sha(tm[0].encode()),'classification':'unchanged_structural_or_formal' if same else 'translated','passage_ids':consulted,'passage_hashes':{p:passages[p]['excerpt_sha256'] for p in consulted},'consultation_note':'Source identifiers, imports, environments or nonlinguistic structure; no translated prose.' if same else 'Consulted during English-to-Javanese authorship for register, spelling and listed lexical decisions; canon is not mathematical authority.','semantic_review':'pending'}
        seg['segment_hash_representation']='UTF-8 with LF-normalized line endings; whole-file source and translation hashes remain raw-byte hashes'
        align.append(seg)
review_file=S/'SEMANTIC_REVIEW.json'
review=json.loads(review_file.read_text(encoding='utf-8')) if review_file.exists() else {}
by_id={r['unit_id']:r for r in rows}
reviewed={r['unit_id'] for r in review.get('unit_reviews',[]) if r['status']=='pass' and r['unit_id'] in by_id and r.get('translation_sha256')==by_id[r['unit_id']]['translation_sha256'] and r.get('source_sha256')==by_id[r['unit_id']]['source_sha256']}
for seg in align:
    if seg['unit_id'] in reviewed:
        seg['semantic_review']='same_author_source_comparison_pass' if seg['classification']=='translated' else 'structural_exception_verified'
        seg['review_file']='SEMANTIC_REVIEW.json'
        seg['review_sha256']=sha(review_file.read_bytes())
(S/'SEGMENT_CANON_USE.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in align),encoding='utf-8')
report={'schema':'jv-batch-qa/1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checked_units':len(rows),'structural_pass_units':sum(x['status']=='structural_pass' for x in rows),'total_units':722,'segments':len(align),'translated_segments':sum(x['classification']=='translated' for x in align),'units':rows,'failures':len(failures),'semantic_reviewed_units':len(reviewed),'build':'see BUILD_SETS.json','release_ready':False}
(S/'BATCH_QA.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='units'}))
