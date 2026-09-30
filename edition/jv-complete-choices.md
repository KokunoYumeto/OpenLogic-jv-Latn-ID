# Cathetan Pilihan lan Pamriksan Wacan

Wacan iki ngemot materi saka 722 berkas isi OpenLogic ing revisi `9620cc73f9c8e0ad003c514a5d3748f29611c4c0`. Terjemahan, koreksi, panyuntingan, lan pamriksan dening panulis AI sing padha ditindakake nganggo OpenAI Codex — GPT-5.6 Sol lan GPT-6 Sol, Ultra effort. Ora ana pamriksan manungsa kang diklaim. Cathetan iki lan wacan kumulatif isih draf kanggo pambangunan lan pamriksan; durung ana rilis wacan jangkep kang wis diverifikasi.

Bab sistem bukti kang digunakake bebarengan ing logika proposisional lan logika sepisanan kapacak sapisan, kanthi materi kuantor tetep ana. Cathetan pangendhali proposisional asli tetep nuduhake carane ngasilake versi proposisional kapisah. Pangendhali alternatif kanggo himpunan lan sintaksis/semantik tetep diakoni, nanging ora njalari bab kang padha dicithak kaping pindho. Materi kang ora diimpor pangendhali baku dilebokake ing bab kang gegayutan, kalebu teori bukti lan panelusuran bukti.

Perangan alternatif OLP-0643 nggunakake identitas rujukan edhisi `prv-alt`; perangan OLP-0121 tetep nganggo `prv`. Identitas ing berkas modular ora diowahi. Tabel aturan kang ora nduweni identitas berkas dhewe tetep nganggo konteks perangan induke. Fragmen `intuitionistic.tex` kapacak minangka fragmen draf: diagram kang ana ing kono nggunakake `G3c` lan konteks suksedhen jamak, mula jeneng berkas kasebut ora dianggep bukti kanggo kalkulus intuisionistik.

Rujukan proposisional menyang bab sistem bukti kang dienggo bebarengan tetep kasedhiya liwat alias `pl` menyang label `fol` ing bab `prf`, `seq`, `ntd`, `tab`, `axd`, lan `com`. Alias mung nuduhake panggonan kang padha ing wacan; ora ngowahi hipotesis utawa rumus. Lapisan rujukan iki kudu dipriksa ing log pambangunan supaya ora ana rujukan kang ilang utawa label kang tumpang tindih.

Kanon kang diwaca mbedakake bukti panganggone basa saka teges matématis. JV-P002 menehi tuladha andharan akademis ngoko, kalebu *yaiku*, *kang*, *nggunakake*, lan jlentrehan rinci. JV-P006 menehi paugeran ejaan serapan; sufiks manca diserap minangka perangan tembung wutuh. JV-P025 menehi tuladha definisi impersonal ing tulisan akademis. JV-P014 nyengkuyung teges *cacah* minangka jumlah, kanthi homonim nyincang disisihake. Perangan kasebut ora menehi atestasi istilah logika utawa kardinalitas kang ora ana ing teks kanon.

Pilihan teknis kang durung nduweni atestasi basa Jawa kang cukup tetep sauntara lan bisa dibenerake. Definisi, rumus, hipotesis, lan arah implikasi manut sumber Inggris. Glosarium utawa tembung serapan wae ora dianggep bukti konsultasi. Pemetaan kanon otomatis kang wis ditarik tetep ora digunakake minangka bukti konsultasi nyata.

| Token sumber | Wujud ing wacan | Teges lan watesan |
| --- | --- | --- |
| `enumerable` | bisa didhaptar | Manut OLP-0029, saben anggota katon ing posisi winates; himpunan winates lan kosong uga kalebu. Ora ditambahake syarat komputabilitas. |
| `denumerable` | bisa dietung lan tanpa wates | Kardinalitas tanpa wates kang bisa dietung: ana bijeksi karo `Nat`; OLP-0193 lan OLP-0339 menehi kontrol teges iki. Kabeh 39 panganggone wis dibandhingake karo paragraf sumber. |
| `at most denumerable` | ukurane ora ngluwihi himpunan kang bisa dietung lan tanpa wates | Wates ukuran iki uga ngidini domain winates. Rong klausa ing OLP-0137 dijlentrehake supaya ora kelangan kasus winates. |
| `computably enumerable`, `c.e.` | bisa didhaptar kanthi komputasi; `c.e.` | Syarat komputabilitas beda saka enumerabilitas umum. Singkatan sumber tetep ana lan ora diklaim minangka istilah asli basa Jawa. |
| `height`, `hp` | dhuwur; `hp` | Dhuwur bukti diukur nganggo langkah inferensi. Ing rong definisi OLP-0698/0701, `hp` ateges njaga dhuwur. |
| `depth` | jerone | Kompleksitas rekursif formula ing induksi formula; beda saka dhuwur wit bukti. |
| `function`, `constant`, `predicate` | simbol fungsi, simbol konstanta, simbol predikat | Token iki manut konfigurasi sumber kanggo tandha basa formal; fungsi utawa unsur domain kang napsirake tandha kasebut ora dipadhakake karo tandhane. |
| `proof`, `derivation` | bukti; derivasi | Sistem sumber netepake objek formal kasebut. Pilihan tembung ora ngowahi aturan, konteks premis, utawa kesimpulan. |
| `derive` kanthi sufiks `d` | diderivasi | Wangun pasif asli diwaca nganggo wangun pasif basa Jawa, kanthi sufiks Inggris diserep dening lapisan token. |
| `prove` kanthi sufiks `d` | dibuktekake, utawa mbuktekake sawise *wis* | Klausa pasif dibedakake saka rong klausa aktif kanthi subjek *kita* utawa *sampeyan*. Kabeh 16 konteks sufiks wis diwaca; rumus lan identitas token tetep ana. |
| `lambda define`, `lambda defined`, `lambda definable` | netepake nganggo lambda; ditetepake nganggo lambda; bisa ditetepake nganggo lambda | Tumindak aktif, asil pasif, lan anane wakil suku lambda dibedakake. Simbol lambda ing wacan tetep simbol sumber. |
| `colorC`, `colorD`, `colorE` | abang, biru, ijo | Manut palet diagram sumber: `a81c21`, `1973ba`, `4d6f39`; warna lan teges geometris ora diowahi. |

Lapisan wacan saiki nduweni definisi kanggo kabeh 67 kulawarga token kang dinormalake lan pemetaan kanggo 6.752 panganggone. Angka iki nuduhake cakupan mekanis. Kajaba panganggone kang kanthi cetha wis dicathet minangka dipriksa, angka kasebut ora ateges kabeh konteks wis divalidasi semantike. Pamriksan konteks liyane isih diterusake. Cathetan pilihan nyimpen paragraf sumber lan target, lokasi, hash, peran bukti kanon, lan bab kang durung mesthi supaya koreksi bisa ditlusuri.

Watesan bukti normalisasi lan konfluensi ing OLP-0687 (OLPL-655 lan OLPL-657) tetep ana. Cakupan berkas jangkep ora minangka sertifikat kabeneran kabeh bukti sumber utawa kabeh pilihan basa. Pamriksan manungsa bisa menehi koreksi tambahan, nanging ora minangka syarat kanggo nerusake produksi lan rilis kang wis lolos pamriksan deterministik.

Kanggo pamriksan tambahan, pilih identitas unit lan paragraf kang cetha, bandhingake rumus lan teges karo sumber Inggris, banjur cathet usul wujud basa Jawa lan bukti panganggone. Mbedakake kaluputan terjemahan saka kaluputan utawa celah ing sumber. Aja nggunakake rasio dawa teks minangka bukti kabeneran semantik.

Pamriksan OLP-0119 lan OLP-0120 nyakup kabeh 23 paragraf kang diterjemahake. OLPL-736 njlentrehake cakupan bukti pisanan lan panggonan kasus kuantor sabanjure; kasus eksistensial tetep gladhen sumber. Alesan basa Jawa lan bukti kanon persis ana ing `translation-decisions/CANON_REVALIDATION_0119_0120.md` lan ledger pilihan.

Pamriksan PDF draf kapisan (931 kaca) nemokake rujukan lawas, rong koma ing dhaptar rujukan tag, label pitakon kang mbaleni, lan sawetara ambane tata letak. Pemetaan rujukan njaga pratelan sumber kang padha: jeneng `prv` lawas tumuju asil konektif ing `ppr`; `phi` tumuju proposisi inkonsistensi loro perluasan; rujukan provabilitas alternatif tumuju `prv-alt`. Label pitakon Nat menyang Nat kang kapindho nganggo `-alt`, dene rujukan baku tetep marang pitakon pisanan. `TAss` diwaca Asumsi lan `Hyp` diwaca Hip; iki katrangan aturan, dudu owah-owahan simbol matématis. Ambane kolom tabel, indentasi, lan larik formula diatur tanpa ngganti formula utawa teks sumber. Pamriksan visual lan kompilasi sabanjure isih kudu rampung.

Kompilasi draf sabanjure ngasilake 932 kaca tanpa rujukan kang ora ditemokake, label kang mbaleni, utawa aksara kang ilang. Rong tabel isih luwih amba rong pt amarga sela antarane garis vertikal rangkep; sela iki saiki diitung ing ambane kolom. Whitespace jejer hbox lan rong paragraf kang meh muat diatur kanthi owah-owahan tata letak. Rumus lan teks basa ora dibusak; pamriksan visual sabanjure tetep dibutuhake.
