# Pamriksan Term, Formula lan Prinsip Induksi

Kabeh 43 blok Inggris lan Jawa OLP-0152 diwaca langsung, kalebu aturan kang kena tag lan rong koreksi sumber sadurunge OLPL-064/065. Terjemahan, koreksi, panyuntingan lan pamriksan panulis AI kang padha nggunakake OpenAI Codex — GPT-6 Sol, Ultra effort; ora ana pamriksan manungsa kang diklaim. Konsultasi kanon iki kelakon mengko. JV-P002 nyengkuyung gancaran ilmiah ngoko, JV-P006 ejaan lan serapan, JV-P026 andharan akademik; ora ana kang mbuktekake prinsip induksi utawa ngatestasi kabeh istilah FOL. JV-T035/076/077 nyebut panerus kanggo successor, mula penerus ing siji prosa iki dibenerake. Makna grammar dikontrol source Inggris lan tag/formula, dudu saksi Indonesia. Pakar Jawa bisa menehi koreksi sabanjure tanpa dadi syarat produksi.

## OLP-0152-P005

Judhul Term lan Formula njaga rong kelas ungkapan beda; token formula ing judhul tetep dikontrol sistem istilah reader.

Kanon kang diwaca: JV-P002, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P006

Basa L dadi parameter pambentukan ungkapan; term lan formula minangka asil utama, ora diasumsikake wis dadi ukara tertutup.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P007

Definisi induktif Trm[L] ngemot saben variabel, saben konstanta lan aplikasi fungsi n-argumen, banjur klausa wates. Term katutup ora ngemot variabel. Iki kontrol nyata kanggo koreksi OLPL-742/743/744 ing model term lan compactness, dudu makna anyar kang digawe saka kanon.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P008

Konstanta bisa dianggep fungsi aritas nol; yen mangkono klausa konstanta kapisah bisa dibusak. Aplikasi fungsi n=0 diwaca minangka simbol f dhewe, ora aplikasi kosong kang nambah obyek.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P009

Definisi Frm[L] diwiwiti saka formula atomik banjur aturan rekursif. Cabang falsum minangka formula atomik mung yen tag prvFalse aktif.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P010

Truth constant minangka formula atomik mung yen tag prvTrue aktif; beda saka simbol truth kang mung definisional ing setelan liyane.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P011

Predikat R n-panggonan lan n term saka L menehi formula atomik R(t1...tn). Variabel bisa ana ing term, mula formula atomik durung mesti ukara.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P012

Identitas rong term uga formula atomik; ora diwatesi term katutup ing grammar formula umum, beda saka model term kang dibangun mengko.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P013

Aturan prvNot mbangun not A saka A lan njaga tag opsional; ora nyelundupake negasi minangka primitif nalika mung definisional.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P014

Aturan konjungsi mbangun formula mawa kurung paling njaba saka A lan B. Kurung iki banjur bisa dilirwakake mung minangka konvensi panulisan ing P023.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P015

Aturan disjungsi mbangun (A or B) saka loro formula lan tag prvOr; ora ngowahi disjungsi dadi konjungsi.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P016

Aturan implikasi mbangun (A lif B) saka loro formula. A minangka antecedent lan B consequent tetep miturut urutan sumber.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P017

Aturan bikondisional mbangun (A iff B), beda saka definisi cekakan biconditional ing cabang defIff.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P018

Aturan universal saka A lan variabel x ngasilake forall x A; ora mbutuhake x bebas katon ing A.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P019

Aturan eksistensial saka A lan variabel x ngasilake exists x A; kalebu kuantifikasi vakum kang diijini.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P020

Klausa Nothing else nutup definisi formula induktif, dadi kurung utawa operator ekstra ora otomatis sah.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P021

Tahap awal ngemot formula atomik falsum/truth mung miturut tag, predikat lan identitas. Panganggone Ing dhasare ngganti Sacara pokok ing gancaran ilmiah; isi rekursif ora owah.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P022

Tahap kapindho/katelu nggunakake formula kang wis kawangun; saben formula muncul ing sawenehing tahap winates senajan jumlah tahap ora winates. Klausa ora ana liyane dijaga.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P023

Notasi identitas infiks, negated equality lan pembuangan kurung luar mung cekakan panulisan. Beda sintaksis resmi Atom eq lan eq infiks tetep dijlentrehake.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P024

Kuantifikasi vakum ora dilarang buku iki, senajan buku liya mbutuhake variabel x muncul ing A. Tag prvEx/prvAll lan tata basa singular/jamak tetep.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P025

Blok simbol definisional nerangake makna operator cekakan; materi iki mung katon yen paling ora siji tag def aktif.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P027

Truth definisional dadi not falsum yen falsum primitif, utawa A or not A kanggo atom A tetep ing cabang liya. Pilihan atom tetep perlu supaya cekakan ora ambig.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P028

Falsum definisional dadi not truth yen truth primitif, utawa A and not A kanggo atom A tetep ing cabang liya; ora mbalikke polarity truth/falsity.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P029

Negasi definisional A→falsum. Aturan tag defNot ora padha karo aturan prvNot kang mbangun grammar langsung.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P030

Disjungsi definisional nganggo De Morgan yen and primitif, utawa not A→B yen and ora primitif. Cabang tag lan kurung formula dijaga.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P031

Konjungsi definisional nganggo not(not A or not B) yen or primitif, utawa not(A→not B) ing cabang liya. A/B ora ditukar.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P032

Implikasi definisional nggunakake (not A or B) yen or primitif, utawa not(A and not B) ing cabang liya. OLPL-064 mbenerake kurung buka kang ilang ing sumber cabang pisanan; rumus target wis cocog lan ora dibaleni koreksine.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P033

Bikondisional definisional minangka konjungsi rong implikasi A→B lan B→A. Rong arah kasebut tetep lan beda saka aturan grammar prvIff.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P034

Kuantor universal definisional minangka not exists x not A, kanthi variable x lan scope negasi tetep.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P035

Kuantor eksistensial definisional minangka not forall x not A, dual saka klausa sadurunge.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P036

Notasi infiks <,+,membership lan postfix successor mung cekakan aplikasi simbol obyek resmi. OLPL-065 mbalekake tipografi Obj ing f1_0(t); fungsi successor diwastani panerus manut JV-T035/076/077, ora penerus.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P037

Identitas sintaktis ident ateges string padha dawane lan saben posisine, dudu identitas obyek ing model; formula A lan B bisa dibandhingake minangka string.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P038

Tuladha konkatenasi njlentrehake kurung buka, substring B ing posisi kapindho, operator or lan kurung tutup miturut urutan; ident ora nindakake entailment semantis.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P039

Klausa pangantar ngubungake definisi induktif term/formula marang prinsip induksi struktural kang sabanjure, ora nganggep bukti wis diwenehi.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P040

Induksi term duwe basis saben variabel lan konstanta, langkah fungsi n-argumen saka hipotesis t1...tn, banjur P kanggo kabeh Trm[L]. Iki ora mung term katutup, sing penting kanggo kontrol scope unit sadurunge.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P041

Gladhen njaluk bukti lemma induksi term karo label fol-syn-frm persis, dudu nyithak bukti anyar.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0152-P042

Induksi formula duwe basis kabeh atom lan langkah saben konektif/kuantor primitif kang dipilih dening tag. Kesimpulan P kabeh Frm[L] lan hipotesis A,B formula L tetep.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.
