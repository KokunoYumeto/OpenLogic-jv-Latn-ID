# Pamriksan Substitusi lan Bebas Kanggo

Kabeh 27 blok Inggris lan Jawa OLP-0158 diwaca langsung. Terjemahan, koreksi lan pamriksan panulis AI kang padha nggunakake OpenAI Codex — GPT-6 Sol, Ultra effort; ora ana pamriksan manungsa kang diklaim. JV-P002/JV-P026 mung kanggo ragam akademik lan cara andharan, JV-P006 kanggo ejaan/serapan. Definisi free-for, substitusi rekursif, cabang kuantor lan variable capture dikontrol sumber Inggris, rumus lan indeks. Telung kemunculan ing prosa diganti muncule konsisten karo OLP-0157. Istilah logika teknis tetep provisional, tanpa klaim atestasi kanon kang ora ana.

## OLP-0158-P005

Judhul Substitusi konsisten karo notasi Subst lan definisi prosedural unit iki.

Kanon kang diwaca: JV-P002, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0158-P006

Substitusi term t kanggo saben occurrence x ing s ditetepake rekursif; kasus konstanta c tetep s.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0158-P007

Yen s variabel y kang ora identik x, asil substitusi tetep s; syarat y variabel lan nonidentitas dijaga.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0158-P008

Yen s persis x, asil substitusi t; iki kasus penggantos pokok.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0158-P009

Ing term f(t1...tn), substitusi ditindakake ing saben argumen term tanpa ngowahi simbol fungsi utawa urutan argumen.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0158-P010

Free for mbutuhake saben occurrence bebas x ing A ana ing njaba cakupan kuantor kang bakal ngiket variabel ing t; iki syarat nyegah capture.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0158-P011

Tuladha v8 bebas kanggo v1 ing exists v3 A2(v3,v1) amarga kuantor v3 ora ngiket variabel ing term v8.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0158-P012

Tuladha f2(v1,v2) ora bebas kanggo v0 ing forall v2 A2(v0,v2) amarga v2 term bakal ketangkep; negasi emfatise dijaga.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0158-P013

Substitusi formula mung diijini yen t free for x ing A lan ngganti kabeh occurrence bebas x; kasus falsum tetep falsum.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0158-P014

Kasus truth tetep truth; tag prvTrue lan beda saka falsum dijaga.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0158-P015

Ing atom predikat P(t1...tn), substitusi lumaku ing saben term argumen lan ora ngowahi P utawa aritas.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0158-P016

Ing identitas t1=t2, substitusi lumaku ing loro sisih identitas, ora ngganti tandha identitas.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0158-P017

Negasi primitif ngleksanani substitusi ing B lan tetep not ing njaba; tag prvNot.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0158-P018

Konjungsi primitif substitusi ing B lan C, njaga kurung lan operator and.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0158-P019

Disjungsi primitif substitusi ing B lan C, njaga operator or lan urutane.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0158-P020

Implikasi primitif substitusi ing antecedent B lan consequent C, ora mbalik arah lif.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0158-P021

Bikondisional primitif substitusi ing B lan C, operator liff ora diowahi.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0158-P022

Ing forall y B, yen y beda x substitusi nerusake ing B; yen y=x, kuantor wis ngiket x mula formula tetep. Syarat free-for njaga y saka t ora ketangkep.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0158-P023

Ing exists y B, cabang y beda x lan y=x paralel universal; tag prvEx lan identitas string formula dijaga.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0158-P024

Substitusi bisa vacuous yen x ora muncul ing A babar pisan; asil A tanpa owah.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0158-P025

Counterexample capture: exists y (x<y) kanthi t=y bakal dadi exists y (y<y), salah ing bilangan asli sanajan forall x exists y x<y bener. Free-for nyegah langkah ora sah iki.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.

## OLP-0158-P026

A(x) mung notasi yen x bisa bebas; A(t) cekakan Subst A t x yen t free for x. Instance universal dimaksud sacara sintaktis, ora ngakoni saben term sah tanpa syarat.

Kanon kang diwaca: JV-P026, JV-P006. Rentang byte persis ana ing ledger pilihan.
