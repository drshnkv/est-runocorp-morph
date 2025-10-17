# Eesti regilaulude korpuse morfoloogiline annotatsioon EstNLTK+dict meetodil – versioon 1\.

## Sissejuhatus

Käesolev töö kirjeldab  eesti regilaulude korpuse morfoloogilise annotatsiooni protsessi, kus töödeldud kogumahus 108 969 regilauluteksti ning 7,3 miljonit sõnavormi. Annotatsioon põhineb EstNLTK 1.7.4 tööriistikomplekti ja Vabamorf morfoloogikaanalüsaatori integratsioonil koos ulatusliku kirjakeele ja murdekeele sõnastike koondindeksiga.

## Algne töövoog: Google Colab paralleelprotsessor

Esmane töötlus toimus Google Colab keskkonnas, kasutades paralleelset partii-põhist töötlust. Süsteem jagas korpuse 1090 partiiks (batch), igaühes 100 regilauluteksti, mis võimaldas kasutada mitme protsessori võimsust ja saavutada 2-4x kiirendus. Iga sõnavorm analüüsiti EstNLTK 1.7.4 abil, rakendades range valideerimisrežiimi (guess=False, propername=False, compound=False) ühemõttelise morfoloogilise analüüsi tagamiseks.

## EstNLTK+dict hübriidmeetod

Põhimeetodina kasutati EstNLTK+dict (EstNLTK kontekstipõhine, ühestamisega analüüs) lähenemist, mis kombineerib morfoloogilist analüüsi sõnastikupõhise otsinguga (175 493 unikaalset sõnavormi erinevatest sõnastikest). Meetod toimib astmeliselt:

1. **EstNLTK+dict (33% korpusest)**: Morfoloogiline analüüs kinnitatud sõnastikukirjetega  
2. **Manual\_override (37% korpusest)**: Eksperdipoolsed käsitsi parandatud lemmad, kaitstud automaatse muutmise eest \- pärinevad FILTER töörühma käsitsi annoteeritud regilaulukorpusest  
3. **EstNLTK (14% korpusest)**: Puhtal morfoloogilisel analüüsil põhinev lemma  
4. **Dict (8% korpusest)**: Otsene sõnastikumatch ilma morfoloogilise kinnituseta  
5. **Levenshtein (4% korpusest)**: Hägususe põhine lähimate sõnade otsing  
6. **suffix\_strip (2.91%)**  \- Liidete eemaldamine (nt \-de, \-te, \-d, \-t) ja seejärel EstNLTK+dict analüüs  
7. **h\_variation (0.10%)** \- 7,665 sõna \- H-lisamise/-ärajätmise käsitlemine (murdelised erinevused)   
8. Jne.

Iga lemma sai usaldusväärsuse skoori (0-1), mis peegeldab esialgset hinnangut meetodi ja analüüsi kvaliteedile. Korpuse keskmine usaldusväärsuse skoor on 0,92, kuid tõenäoliselt (varasem eksperiment näitas) on õigeid lemmasid umbes 60-70%.

## Kolmeastmeline parandustesüsteem

Pärast esmast töötlust rakendati kolmeastmelist automaatset parandustsüklit, mis kasutab **hübriidskoori** (60% redigeerimiskaugus originaalvormist \+ 40% sagedusskoor Tartu Ülikooli ilukirjanduskorpuse põhjal) kombineerituna **EstNLTK/Vabamorf morfoloogilise valideerimisega**, et valida sõnastikeindeksist suurima tõenäosusega õigem lemmakandidaat.

Tieride määramise kriteerium oli **Vabamorfi abil valideerimise õnnestumine**:

**Tier 1 (kõrge usaldusväärsus)**: 588 046 parandust

**Allikad**:

- Sõnastikest pärinevad kandidaadid, mille Vabamorf valideeris (`valid_voro_candidate`)  
- EstNLTK analüüs normaliseeritud lemmadele, Vabamorf valideeris (`estnltk_normalized`)  
- Vabamorf'i checkpointist soovitused (`vabamorf_from_checkpoint`)

**Tier 2 (keskmine usaldusväärsus)**: 2 608 parandust

- **Allikad**: Sõnastikest pärinevad kandidaadid, mida Vabamorf **ei valideerinud** (`highest_voro_unvalidated`)  
- **Rakendamine**: Ainult madala usaldusväärsusega algsetele lemmadele

**Tier 3 (madal usaldusväärsus)**: 38 533 parandust

**Allikad**:

- Sõnastikulemmad madalate sarnasuskooridega (\< 0.5) (`highest_voro_low_score`)  
- Alternatiivide puudumisel interpunktsioonita variant (`no_alternatives`)

Kokku teostati 629 187  parandust (automaatsed \+ osa kõige sagedasemaid vigaseid analüüse käsitsi) murdeliste vormide standardiseerimiseks.

## Hübriidreitingusüsteem alternatiivide valikul

Mitme võimaliku lemma puhul rakendati hübriidreitingut: **60% redigeerimisetäpsus** (Levenshteini kaugus algvormist) \+ **40% sagedusreiting** (Tartu Ülikooli ilukirjanduskorpuse põhjal). Süsteemi testiti 448 217 madala usaldusväärsusega sõnal, millest 119 184 (26,6%) said paranenud lemma. Enamik (94,9%) parandusi põhineb sagedusandmetel, mis aitavad valida suurema tõenäosusega õigemad lemmad paljude variantide seast (kuna ilukirjanduses rohkem esinevaid sõnu kasutatakse ka regilauludes rohkem).

## Valideerimine ja kvaliteedikontroll

Kõik lemmad valideeriti EstNLTK/Vabamorf süsteemiga ranges režiimis:

- Kolme kategooria klassifikatsioon: valid\_lemmas, invalid, not\_lemmas  
- Leitud sõnavormid, mis ei olnud lemmad (nt jalge→jalg) parandati automaatselt

## Lõpptulemused

**Korpuse maht**: 7 302 185 sõna **Unikaalsed sõnavormid**: 452 161 **Unikaalsed lemmad**: 192 756  \- millest 60 993 ehk 31,6% valideeritavad standardeesti morfoloogiaga; ülejäänud on arhailised või murdelemmad (kui lemma genereerimine ei andnud tulemuseks EstNLTK-ga valideeritavat lemmat) või sõnavormid.

Korpus on kättesaadav SQLite andmebaasina (corpus\_v3.db) ning sisaldab täielikku metainfot iga sõna kohta: lemma, POS-märgend, morfoloogiline kood, töötlusmeetod, usaldusväärsus, alternatiivid ning sagedusinfo. See võimaldab nii keeleteaduslikku analüüsi kui ka masinõppe rakendusi, samuti regilaulutekstide senisest paremat SKM-töötlust.  
