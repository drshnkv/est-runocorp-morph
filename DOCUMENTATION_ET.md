# Eesti regilaulude korpuse morfoloogiline annotatsioon EstNLTK+dict meetodil

## Sissejuhatus

Käesolev töö kirjeldab  eesti regilaulude korpuse morfoloogilise annotatsiooni protsessi, kus töödeldud kogumahus 108 969 regilauluteksti ning 7,3 miljonit sõnavormi. Annotatsioon põhineb EstNLTK 1.7.4 tööriistikomplekti ja Vabamorf morfoloogikaanalüsaatori integratsioonil koos ulatusliku kirjakeele ja murdekeele sõnastike koondindeksiga.

## Algne töövoog: Google Colab paralleelprotsessor

Esmane töötlus toimus Google Colab keskkonnas, kasutades paralleelset partii-põhist töötlust. Süsteem jagas korpuse 1090 partiiks (batch), igaühes keskmiselt 100 luuleteksti, mis võimaldas kasutada mitme protsessori võimsust ja saavutada 2-4x kiirendus. Iga sõnavorm analüüsiti EstNLTK 1.7.4 abil, rakendades range valideerimisrežiimi (guess=False, propername=False, compound=False) ühemõttelise morfoloogilise analüüsi tagamiseks. 

## EstNLTK+dict hübriidmeetod

Põhimeetodina kasutati EstNLTK+dict (EstNLTK kontekstipõhine, ühestamisega analüüs) lähenemist, mis kombineerib morfoloogilist analüüsi sõnastikupõhise otsinguga (175 493 unikaalset sõnavormi erinevatest sõnastikest). Meetod toimib astmeliselt:

1. **EstNLTK+dict (33% korpusest)**: Morfoloogiline analüüs kinnitatud sõnastikukirjetega
2. **Manual_override (37% korpusest)**: Eksperdipoolsed käsitsi parandatud lemmad, kaitstud automaatse muutmise eest - pärinevad FILTER töörühma käsitsi annoteeritud regilaulukorpusest 
3. **EstNLTK (14% korpusest)**: Puhtal morfoloogilisel analüüsil põhinev lemma
4. **Dict (8% korpusest)**: Otsene sõnastikumatch ilma morfoloogilise kinnituseta
5. **Levenshtein (4% korpusest)**: Hägususe põhine lähimate sõnade otsing
6. **suffix_strip (2.91%)**  - Liidete eemaldamine (nt -de, -te, -d, -t) ja seejärel EstNLTK+dict analüüs
7.  **h_variation (0.10%)** - 7,665 sõna - H-lisamise/-ärajätmise käsitlemine (murdelised erinevused)
Jne.


Iga lemma saab usaldusväärsuse skoori (0-1), mis peegeldab meetodi ja analüüsi kvaliteeti. Korpuse keskmine usaldusväärsus on 0,92, mis ei pruugi peegeldada reaalsust. 

## Kolmeastmeline parandustesüsteem

Pärast esmast töötlust rakendati kolmeastmelist automaatset parandustsüklit, mis kasutab **hübriidskoorimist** (60% redigeerimiskaugus originaalvormist + 40% sagedusskoor Tartu Ülikooli ilukirjanduskorpuse põhjal) kombineerituna **EstNLTK/Vabamorf morfoloogilise valideerimisega**.

Tieride määramise kriteerium oli **Vabamorf'i valideerimise õnnestumine**:

**Tier 1 (kõrge usaldusväärsus)**: 588 046 parandust
- **Allikad**:
  - Sõnastikest pärinevad kandidaadid, mille Vabamorf valideeris (`valid_voro_candidate`)
  - EstNLTK analüüs normaliseeritud lemmadele, Vabamorf valideeris (`estnltk_normalized`)
  - Vabamorf'i checkpointist soovitused (`vabamorf_from_checkpoint`)


**Tier 2 (keskmine usaldusväärsus)**: 2 608 parandust
- **Allikad**: Sõnastikest pärinevad kandidaadid, mida Vabamorf **ei valideerinud** (`highest_voro_unvalidated`)
- **Rakendamine**: Ainult madala usaldusväärsusega algsetele lemmadele

**Tier 3 (madal usaldusväärsus)**: 38 533 parandust
- **Allikad**:
  - Sõnastikulemmad madalate sarnasuskooriridega (< 0.5) (`highest_voro_low_score`)
  - Alternatiivide puudumisel interpunktsioonita variant (`no_alternatives`)

Kokku teostati 629 187  parandust (automaatsed + osa kõige sagedasemaid vigaseid analüüse käsitsi) murdeliste vormide standardiseerimiseks. 

## Hübriidreitingusüsteem alternatiivide valikul

Mitme võimaliku lemma puhul rakendati hübriidreitingut: **60% redigeerimisetäpsus** (Levenshtein kaugus algvormist) + **40% sagedusreit** (Tartu Ülikooli ilukirjanduskorpuse põhjal). Süsteemi testiti 448 217 madala usaldusväärsusega sõnal, millest 119 184 (26,6%) said paranenud lemma. Enamik (94,9%) parandusi põhineb sagedusandmetel, mis tagab keeleliselt loomulikud valikud.

## Valideerimine ja kvaliteedikontroll

Kõik lemmad valideeriti EstNLTK/Vabamorf süsteemiga range režiimis:
- Kolme kategooria klassifikatsioon: valid_lemmas, invalid, not_lemmas
- Leitud sõnavormid, mis ei olnud lemmad (meesi→mees, jalge→jalg) parandati automaatselt

## Lõpptulemused

**Korpuse maht**: 7 302 185 sõna 
**Unikaalsed algvormid**: 452 161
**Unikaalsed lemmad**: 192 756  - millest 60 993 ehk 31,6% valideeritavad standardeesti morfoloogiaga; ülejäänud on arhailised või murdelemmad (kui sõnastikupõhine tuvastamine õnnestus) või sõnavormid
**Tundmatud sõnad**: 42 389 (0,58%)
**Keskmine usaldusväärsus**: 0,92

Korpus on kättesaadav SQLite andmebaasina (corpus_v3.db) ning sisaldab täielikku metainfot iga sõna kohta: lemma, POS-märgend, morfoloogiline kood, töötlusmeetod, usaldusväärsus, alternatiivid ning sagedusinfo. See võimaldab nii keeleteaduslikku analüüsi kui ka masinõppe rakendusi eesti murdeainese uurimisel.
