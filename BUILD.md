# Build the complete Javanese reader

The main file is `edition/jv-complete.tex`. It loads the complete Javanese
text in `edition/jv-complete-body.tex` and the front matter in
`edition/jv-complete-about.tex`. The source archive also contains the 722
translated modules under `translation/content/`, the original English source,
and the OpenLogic styles, figures and bibliography inputs used by the
reader.

Keep the archive's directory layout when extracting it. Use a TeX distribution
with pdfLaTeX, BibTeX, memoir, mathpazo, microtype, TikZ and the other packages
loaded by OpenLogic. Run the commands from the extracted archive's root.

## macOS and Linux

```sh
(
set -e
cd edition
export BSTINPUTS="../upstream/bib:"
pdflatex -no-shell-escape -halt-on-error -interaction=nonstopmode jv-complete.tex
bibtex jv-complete
pdflatex -no-shell-escape -halt-on-error -interaction=nonstopmode jv-complete.tex
bibtex jv-complete
for pass in 1 2 3 4 5 6; do
  pdflatex -no-shell-escape -halt-on-error -interaction=nonstopmode jv-complete.tex
done
)
```

## Windows PowerShell 7

From the source tree root, one command builds the reader with a 5 GiB
process-tree cap. A fresh output folder is required.

~~~powershell
pwsh -NoProfile -File tools/build-complete-reader.ps1 -Edition edition -Output .build/reader
~~~

The PDF is in .build/reader. To reproduce the direct cumulative TeX
download, put it in edition/ and pass its basename as -JobName to
the same command, using a fresh output folder.

### Manual commands

```powershell
Set-Location edition
$env:BSTINPUTS = '..\upstream\bib;'
pdflatex -no-shell-escape -halt-on-error -interaction=nonstopmode jv-complete.tex
if ($LASTEXITCODE -ne 0) { throw 'pdfLaTeX failed' }
bibtex jv-complete
if ($LASTEXITCODE -ne 0) { throw 'BibTeX failed' }
pdflatex -no-shell-escape -halt-on-error -interaction=nonstopmode jv-complete.tex
if ($LASTEXITCODE -ne 0) { throw 'pdfLaTeX failed' }
bibtex jv-complete
if ($LASTEXITCODE -ne 0) { throw 'BibTeX failed' }
1..6 | ForEach-Object {
    pdflatex -no-shell-escape -halt-on-error -interaction=nonstopmode jv-complete.tex
    if ($LASTEXITCODE -ne 0) { throw 'pdfLaTeX failed' }
}
```

The result is `edition/jv-complete.pdf`. The second BibTeX pass picks up
citations introduced by bibliography notes. The final pdfLaTeX passes settle
references, page numbers and the table of contents. Check the final log for
unresolved references or citations before using the PDF.

The reader credits the Open Logic Project and the authors of its original
components. See [the source and licence information](README.md) for the pinned
English revision and applicable notices.
