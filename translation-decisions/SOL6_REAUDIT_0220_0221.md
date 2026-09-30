# Pamriksan Maneh Karya Sol 6: OLP-0220, OLP-0221

Pamriksan sumber lan kanon iki ditindakake dening OpenAI Codex — GPT-6.1 Sol, Ultra. Iki bukti anyar saka pamriksan retrospektif. Ora ana pamriksan manungsa kang diklaim. Cathetan lawas dijaga minangka riwayat.

## OLP-0220

Kabeh 25 blok lan rong konstruksi concat dipriksa. Nilai wiwitan concat dibenerake supaya alias kosong siji dadi nol kanonik. OLPL128 lan130 dibuktekake maneh; OLPL129 mung varian wates aman, dudu salah sumber kang wis nduweni counterexample. Cakupan kode sah lan subseq total dilabeli cathetan panyunting.

## OLP-0221

Kabeh sepuluh blok lan bukti subwit dipriksa. OLPL131 rekursi kumulatif lan OLPL132 suku tambahan kosong diwaca maneh; andharan anyar saka kode mudhun kanggo wates dhuwur wit dilabeli cathetan panyunting.

### OLP-0220-P004

Judhul rerangken lan identitas perangan tetep.

Alternatif kang ditimbang: rerangken ing kene winates.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0220-P005

Saben pangkat ditambah siji supaya unsur nol ing pucuk ora ilang. Kode kosong utama nol; siji mung wakil alternatif, dudu kode kanonik kang kapindho.

Alternatif kang ditimbang: ora kabeh wilangan asli dadi kode sah rerangken.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0220-P006

Faktorisasi prima unik menehi injektivitas kode kanonik, dene eksponen nol bisa nuduhake wilangan kang ora dadi kode sah. Pangodean kosong kanonik dipilih nol.

Alternatif kang ditimbang: kode siji kanggo kosong ora ngrusak injektivitas nalika kode utama dipilih nol.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0220-P007

Patang operasi dawa, unsur, append lan concat tetep dibedakake.

Alternatif kang ditimbang: ngitung kode ora padha karo ngitung cacah unsur.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0220-P008

Dawa rerangken diwaca mung kanggo kode sah; rumus isih menehi fungsi total kanggo wilangan liyane.

Alternatif kang ditimbang: ora ngaku hasil dawa kanggo kode kang ora sah duwe makna rerangken.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0220-P009

R nemokake prima pungkasan ing dhaptar faktor prima kang runtut kanggo kode sah. Indeks luwih cilik tinimbang kode amarga saben prima paling ora loro; kasus kosong nol/siji dipriksa kapisah.

Alternatif kang ditimbang: prima kang ilang ing tengah mung kedadeyan kanggo kode ora sah.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0220-P010

Pratelan append menehi kode unsur anyar ing pucuk.

Alternatif kang ditimbang: ora nambah unsur ing wiwitan.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0220-P011

Kasus kosong menehi loro pangkat a tambah siji; kasus ora kosong nggunakake prima anyar kanthi indeks dawa.

Alternatif kang ditimbang: unsur nol tetep nduweni pangkat siji.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0220-P012

Unsur wiwitan nganggo indeks nol; indeks ing njaban dawa diwenehi nilai nol kanthi konvensi.

Alternatif kang ditimbang: nilai nol ora otomatis ateges unsur ana.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0220-P013

Minimisasi golek a paling cilik kang prima pangkat a tambah loro ora mbagi kode. Iki menehi eksponen dikurangi siji nalika indeks sah. Tembung ing mbox diterjemahake kanthi math njero padha.

Alternatif kang ditimbang: ora mbutuhake tes pangkat sadurunge ing saben calon a amarga minimalitas.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0220-P014

Notasi tuple saka append lan indeks nol nganti k kurang siji nalika dawa k dipriksa.

Alternatif kang ditimbang: tuple kang nduweni unsur a0 nganti ak dawane k tambah siji.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0220-P015

Concat minangka fungsi numerik kudu konsisten ing rong konstruksi, kalebu wakil alternatif kode kosong.

Alternatif kang ditimbang: SOL6-F038 mbenerake nilai wiwitan kang durung kanonik.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0220-P016

Rekursi hconcat nambah unsur t kaping n; nilai wiwitan saiki ngganti wakil kosong siji dadi nol. Iki nggawe concat saka kode kosong alternatif padha numerike karo minimisasi.

Alternatif kang ditimbang: tanpa normalisasi, concat saka siji lan nol menehi siji ing rekursi nanging nol ing minimisasi.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0220-P017

Notasi concat infiks tetep nglambangake fungsi kang padha.

Alternatif kang ditimbang: ora ngowahi urutan rerangken.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0220-P018

OLPL128 kasus dawa nol dipriksa maneh; p kanthi indeks minus siji ora ana, mula wates siji ditetepake kapisah. Kanggo dawa positif, saben faktor lan pangkat diwatesi kaya sumber.

Alternatif kang ditimbang: wates iki kanggo kode utama nol lan kode kosong alternatif siji.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0220-P019

OLPL130 rong kuantor sejajar dipriksa maneh nganggo s kosong lan t singleton. Varian wates kalebu endpoint saka OLPL129 aman, nanging wates ketat sumber wis cukup kanggo input kode sah ora kosong amarga s tambah t ngluwihi saben unsur.

Alternatif kang ditimbang: ora mbaleni klaim yen wis ana counterexample marang bound s+t kang dipasang ing sumber.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0220-P020

Gladhen sconcat bisa dibangun kanthi nglumpukake concat liwat saben unsur saka kode rerangken njaba.

Alternatif kang ditimbang: kode njaba lan kode subrerangken dibedakake.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0220-P021

Tail mbusak unsur kapisan lan menehi kode nol kanggo kosong; singleton uga menehi kosong.

Alternatif kang ditimbang: ora njaga unsur kapisan ing asil.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0220-P022

Cakupan subseq dibenerake: kanggo interval sah asil subrerangken asli; supaya fungsi total dawane n, interval liwat pucuk diisi unsur nol saka konvensi element.

Alternatif kang ditimbang: ora ngaku ana subrerangken asli dawane n yen unsur kang kasedhiya kurang.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0220-P023

Source gladhen tetep diterjemahake minangka gladhen.

Alternatif kang ditimbang: ora ngaku sumber ngemot bukti subseq.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0220-P024

Rujukan prop:subseq lan syarat gladhen padha. Konstruksi kanthi append unsur i nganti i+n kurang siji njaga rekursi primitif.

Alternatif kang ditimbang: rumus extension input ora sah kudu kasebut yen fungsi total dibutuhake.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0221-P004

Judhul wit lan identitas tetep; iki wit kanthi oyod kang winates.

Alternatif kang ditimbang: ora wit tanpa wates utawa grafik kang nduweni siklus.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0221-P005

Oyod lan subwit langsung dibedakake; label simpul bisa ana utawa ora.

Alternatif kang ditimbang: subwit ing kene kalebu wit kang diwiwiti ing oyod dhewe.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0221-P006

Kode nyimpen cacah subwit dhisik banjur kode subwit lan label. Kabeh tuladha nested tuple dipriksa.

Alternatif kang ditimbang: label ora diitung minangka subwit.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0221-P007

Pratelan SubtreeSeq ngasilake rerangken kode kabeh subwit kanthi ulangan diidinake.

Alternatif kang ditimbang: dudu dhaptar tanpa ulangan kaya gladhen sabanjure.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0221-P008

OLPL131 rekursi kumulatif dipriksa maneh; OLPL132 siji input tambahan menehi f0 kosong ing helper tartamtu iki. Saben kode subwit langsung luwih cilik tinimbang kode induke amarga katon minangka eksponen; iki menehi wates dhuwur t.

Alternatif kang ditimbang: f0 kosong ora bener kanggo sembarang fungsi f, mung ISubtrees kang digunakake.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.

### OLP-0221-P009

Gladhen njaluk nyingkirake kode ulangan, ora nyamarake simpul beda kanthi label padha minangka simpul kang padha.

Alternatif kang ditimbang: dhaptar kode unik bisa nyawijikake subwit kang kode lengkap padha.
Kanon kang digunakake: JV-P002, JV-P005, JV-P006. Bukti ragam lan ejaan diwatesi; makna logis manut sumber beku.
