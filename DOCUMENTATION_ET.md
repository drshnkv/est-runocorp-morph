# Eesti regilaulude korpuse morfoloogiline annotatsioon EstNLTK+dict meetodil – versioon 1\.

## Sissejuhatus

Morfoloogiliselt annoteeritud regilaulutekstide korpus. Töödeldud on kogumahus 108 969 regilauluteksti ning 7,3 miljonit sõnavormi. Annotatsioon põhineb EstNLTK 1.7.4 integratsioonil Eesti murrete korpuse, EKI regilaulukorpuse ning mitmete sõnastike koondindeksiga (175 493 unikaalset sõnavormi). 

Tegu on eksperimendiga, mille eesmärgiks on SKM-e kasutamata lisada suures osas arhailist ja murdelist regilaulukeelt hõlmavale korpusele esialgne oletuslik morfoloogiline analüüs reeglipõhiste meetodite abil. Eksperimendi eesmärk on hõlbustada edasist täpsemat morfoloogilist analüüsi SKM-de abil. Praegune analüüs sisaldab palju vigaseid analüüse (ca 30-40%).

## Algne töövoog: Google Colab paralleelprotsessor

Esmane töötlus toimus Google Colab keskkonnas, kasutades paralleelset partii-põhist töötlust. Süsteem jagas korpuse 1090 partiiks (batch), igaühes 100 regilauluteksti, mis võimaldas kasutada mitme protsessori võimsust ja saavutada 2-4x kiirendus. Iga sõnavorm analüüsiti EstNLTK 1.7.4 abil (analüüs hõlmas ka terviktekstil põhinevat ühestamist).

## EstNLTK+dict hübriidmeetod

Esmalt analüüsiti kogu regilaulukorpus EstNLTK 1.7.4 abil, kasutades VabamorfTagger kontekstipõhist ühestamist (postdisambiguate=True).

Seejärel määrati igale sõnavormile lemma kasutades **esimese sobiva meetodi** tulemust (meetodeid proovitakse järjestikku):

1. **Manual_override (37% korpusest)**: Folkloristide poolt käsitsi määratud lemmad, kaitstud automaatse muutmise eest - pärinevad FILTER töörühma poolt käsitsi annoteeritud regilaulude testkorpusest (93 teksti). Kontrollitakse **esmalt** enne teisi meetodeid.

2. **EstNLTK+dict (33% korpusest)**: EstNLTK leidis sõnavormile lemma **JA** see lemma on koondindeksis olemas **JA** algne sõnavorm on selle lemma variant koondindeksis. Kolme tingimuse koosesinemise tõttu kõrgeim usaldusväärsus (1.00).

3. **EstNLTK (14% korpusest)**: EstNLTK leidis sõnavormile erineva lemma (mitte ainult normaliseeritud sama vorm), kuid koondindeks ei kinnitanud seda. Suhteliselt kõrge usaldusväärsus (0.95).

4. **Dict (8% korpusest)**: Otsene sõnastikumatch koondindeksist, ilma EstNLTK kinnituseta. Mitme sõnavormiga seostatud lemma puhul valitakse lähim Levenshteini kauguse põhjal.

5. **Levenshtein (4% korpusest)**: Hägususe põhine lähimate sõnavormide otsing koondindeksist (Levenshteini kaugus ≤2), leitakse vastava sõnavormiga seostatud lemma. Madalam usaldusväärsus (0.6-0.3 sõltuvalt kaugusest).

6. **suffix_strip (2.91%)**: Liidete eemaldamine (nt -de, -te, -d, -t, samuti murdelised lõpud nagu -nõ, -õ, -kene, -kese) ja seejärel uuesti koondindeksi otsing (dict-meetod).

7. **h_variation (0.10%)**: H-lisamise/-ärajätmise käsitlemine (murdelised erinevused) - proovitakse lisada või eemaldada 'h' sõna algusest ning otsida koondindeksist.

8. **compound (0.7%)**: Liitsõna komponentide eraldamine, mõlema komponendi lemma otsimine koondindeksist.


Iga lemma sai usaldusväärsuse skoori (0-1), mis peegeldab esialgset hinnangut meetodi ja analüüsi kvaliteedile. Korpuse keskmine usaldusväärsuse skoor on 0,92, kuid tõenäoliselt (varasem eksperiment näitas) on õigeid lemmasid umbes 60-70%.

## Kolmeastmeline parandustesüsteem

Pärast esmast töötlust rakendati mitmeastmelist automaatset parandustsüklit, mis kasutas madalama usaldusväärsusega ning madalama sarnasusskooriga lemmakandidaatide automaatseks parandamiseks **hübriidskoori** (60% redigeerimiskaugus originaalvormist \+ 40% sagedusskoor Tartu Ülikooli ilukirjanduskorpuse põhjal) kombineerituna **EstNLTK morfoloogilise valideerimisega**, et valida sõnastikeindeksist suurima tõenäosusega varasemast õigem lemmakandidaat.


Kokku teostati 629 187  parandust (automaatsed \+ osa kõige sagedasemaid vigaseid analüüse käsitsi) murdeliste vormide standardiseerimiseks. Sagedusandmete kasutamine põhineb tõdemusel, et ilukirjanduses rohkem esinevaid sõnu kasutatakse ka regilauludes rohkem, mis aitab valida suurema tõenäosusega õigema lemma.


## Lõpptulemused

**Korpuse maht**: 7 302 185 sõna **Unikaalsed sõnavormid**: 452 161 **Unikaalsed lemmad**: 192 756  \- millest 60 993 ehk 31,6% valideeritavad standardeesti morfoloogiaga; ülejäänud on arhailised või murdelemmad (kui lemma genereerimine ei andnud tulemuseks EstNLTK-ga valideeritavat lemmat) või sõnavormid.

Korpus sisaldab täielikku metainfot iga sõna kohta: lemma, POS-märgend, morfoloogiline kood, töötlusmeetod, usaldusväärsus, alternatiivid ning sagedusinfo. See võimaldab nii keeleteaduslikku analüüsi kui ka masinõppe rakendusi, samuti regilaulutekstide senisest paremat SKM-töötlust.  
