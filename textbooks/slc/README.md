# Himpunan, Logika, Komputasi

Pambuka metalogika ing basa Jawa aksara Latin. Richard Zach nyusun buku
iki saka *The Open Logic Text* anggitané Open Logic Project. Isiné teori
himpunan, logika tataran kapisan, kalkulus sekèn, dedhuksi alami, lan mesin
Turing. Lampirané ngrembug bukti, induksi, babad para ahli logika, lan
aksara Yunani.

Tèks Richard Zach lan Open Logic Project sarta terjemahan iki nganggo
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Terjemahan lan panyuntingan diprodhuksi AI OpenAI Codex, GPT-6.1 Sol
kanthi upaya nalar Ultra. Revisi sumber lan atribusi ana ing
[manifest](MANIFEST.json). [Buku sumber](https://github.com/rzach/sets-logic-computation/tree/6178f32f61645f3b62ef621b4c5a88f8e67778ad) ·
[Revisi Open Logic Text](https://github.com/OpenLogicProject/OpenLogic/tree/1e960beff9ed7835bf3e3f1335e21af3439cd107).

Ilustrasi anggitané Matthew Leadbeater nganggo
[CC BY-NC 4.0](assets/portraits/LICENSE.md). Foto dienggo miturut
[katemtuan repositori foto](assets/photos/README.md) lan atribusi saben
foto. Buku iki nyebut atribusi lengkap ing pérangan Atribusi Foto.

## Ngasilaké PDF

Gunakna PowerShell 7, Python 3.10 utawa luwih anyar, lan distribusi
LaTeX kanthi pdfLaTeX, BibTeX, MakeIndex lan pakèt sing dienggo
[kelas buku Open Logic Project](../../upstream/sty/open-logic-book.cls).
Saka oyod repositori, lakokna préntah ing ngisor iki.

~~~powershell
pwsh -NoProfile -File textbooks/slc/build.ps1
~~~

Asilé [slc-screen-jv.pdf](slc-screen-jv.pdf).

- [Arsip sumber lengkap lan pandhuan nyusun PDF](slc-source-jv.zip)
- [Sumber LaTeX kumulatif](slc-screen-jv.tex)
- [Checksum telung undhuhan](SHA256SUMS.txt)
- [Pandhuan ngasilaké PDF saka arsip sumber](BUILD.md)

Préntah iku nata
sumber ing .build, mriksa hash sumber OLP lan terjemahan, nyusun
locale/jv, lan nglakokaké pdfLaTeX, BibTeX lan MakeIndex.
Entri glosarium diurutaké nganggo kunci abjad Latin basa Jawa.
Skrip mriksa yèn 176 modul kang dienggo buku, 12 ringkesan, lan 79
entri glosarium kabèh mlebu ing PDF. Kanggo mriksa susunan bab lan
nlusuri tilas basa Inggris, gunakna Python kanthi pakèt pypdf lan
Poppler (pdftotext), sarta PDF basa Inggris saka manifest.

~~~powershell
python textbooks/slc/audit.py --reference path/to/slc-screen.pdf --report path/to/slc-audit.json
~~~

Teks kanggo sampul cetak ukuran 6×9 lan Lulu Royal ana ing
[cover-text.tex](book/include/cover-text.tex).

## Locale liya

Susunan buku lan pilihan tag SLC ana ing book/slc.tex lan
book/slc-config.jv.sty. Sumber basa target mlebu locale/<id>/content
lan nganggo tetenger basa ing olfileid, olchapterid, lan olpartid.
Katrangan rujukan lan istilah buku disetel ing locale basa target.
Pambuka, ringkesan, glosarium, teks sampul, lan atribusi foto nduwèni
sumber lokal dhewe. Gunakna kunci pangurutan kang cocog karo aksara
lan basa target.

Kanggo Telugu, gunakna LuaLaTeX, Babel mawa locale **telugu**, lan
font **Noto Serif Telugu** lumantar babelfont. Priksa wangun
aksara gandhèngan lan pegatan larik. [Pandhuan Babel kanggo Telugu](https://latex3.github.io/babel/guides/locale-telugu.html)

Kanggo Arab, gunakna LuaLaTeX, Babel mawa locale **arabic** lan
setelan **bidi=basic**, sarta font Arab OpenType kayata **FreeSerif**.
Priksa arah paragraf, arah formula lan angka ing prosa Arab, tandha
wacan, tabel, lan panah ing diagram. [Pandhuan Babel kanggo Arab](https://latex3.github.io/babel/guides/locale-arabic.html)

Kanggo loro-loroné, pisahna setelan font lan opsi pdfTeX ing kelas
buku saka setelan LuaLaTeX. Priksa manawa simbol lan tata letak
bukti tetep bener, font kabèh kacantum ing PDF, lan teks bisa
disalin. Priksa manèh setelan PDF/A. Yèn MakeIndex ora bisa
ngurutaké aksara manut paugeran basa target, gunakna nomer urut
kanthi dawa padha minangka kunci pangurutan glosarium.
