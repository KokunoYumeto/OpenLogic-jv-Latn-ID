# Ngasilaké PDF Himpunan, Logika, Komputasi

Gunakna Windows, PowerShell 7, Python 3.10 utawa luwih anyar, lan
distribusi TeX kang nyedhiyakaké pdfLaTeX, BibTeX, MakeIndex, memoir,
Babel, glossaries, pdfx lan pakèt Open Logic. Ekstrak kabèh isi arsip
kanthi susunan direktori kang padha. Préntah iki dilakokaké saka oyod
arsip kang wis diekstrak.

~~~powershell
pwsh -NoProfile -File build.ps1 -PreparedTree .
~~~

Kanggo ngasilaké PDF saka siji berkas LaTeX kumulatif, gunakna
préntah iki. Sumber kumulatif wis ana ing direktori buku ing arsip.
Yèn nganggo undhuhan LaTeX kapisah, salinna menyang
`olp/locale/jv/courses/sets-logic-computation/slc-screen-jv.tex`.

~~~powershell
pwsh -NoProfile -File build.ps1 -PreparedTree . -Cumulative
~~~

PDF asil ana ing oyod arsip. Arsip ngemot sumber lan gambar sing
dibutuhaké. Daftar checksum isi ana ing `SOURCE-SHA256SUMS.txt`.

Richard Zach nyusun buku saka karya Open Logic Project. Tèks lan
terjemahan nganggo CC BY 4.0. Terjemahan diprodhuksi AI OpenAI
Codex, GPT-6.1 Sol kanthi upaya nalar Ultra. Delengen
`LICENSE-SLC.md`, `olp/LICENSE.md`, lisènsi ilustrasi lan cathetan
atribusi foto kanggo hak saben komponen.
