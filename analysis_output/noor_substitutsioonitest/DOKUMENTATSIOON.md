# Substitutsioonitest: 'noor' sünonüümide tuvastamine

## Ülevaade

See analüüs tuvastab lemma **'noor'** ja selle variantide (**'nooreke'**, **'nooruke'**)
võimalikud sünonüümid eesti regilaulude korpusest, kasutades distribatiivse semantika
meetodit — substitutsioonitesti.

**NB!** Analüüs lähtub kolmest lemmast korraga:
- `noor` (peamine lemma)
- `nooreke` (deminutiiv)
- `nooruke` (deminutiiv)

Kõigi kolme lemma kontekstid (värsimallid) on kokku liidetud, et leida sõnu,
mis võivad neid asendada sarnastes värsistruktuurides.

---

## Lähtefailid

| Fail | Kirjeldus |
|------|-----------|
| `poems_index_v2.json.gz` | Eesti regilaulude korpuse v2 indeks (108 969 laulu, ~4,5 miljonit värsimalli) |



---

## Kasutatud skript

**Fail:** `substitution_test_noor_pos_filtered.py`

Skript teostab järgmised etapid:
1. Laeb korpuse ja analüüsib kõigi lemmade sõnaliike (POS)
2. Ehitab värsimallide andmebaasi kõigile lemmadele
3. Leiab lemmad, mis jagavad malle sihtlemmadega
4. Filtreerib tulemused sõnaliigi järgi (ainult A ja S)
5. Arvutab erinevad sarnasuse skoorid
6. Järjestab tulemused `candidate_coverage` järgi

---

## Algoritmi selgitus

### 1. Värsimallide loomine

Iga värsi jaoks, kus esineb sihtlemma, luuakse "mall", asendades sihtsõna kohahoidjaga `___`:

```
Algne värss: "noore ema nutuvaeva"
Mall:        "___ ema nutuvaeva"
```

### 2. Mallide võrdlemine

Kui teine lemma esineb samas mallis, saab ta sihtlemmat asendada:

```
'noor' → "___ mees tuleb" (15 korda)
'vana' → "___ mees tuleb" (8 korda)
→ 'vana' saab asendada 'noor' selles kontekstis
```

### 3. Sõnaliigi filtreerimine

Kuna 'noor' on peamiselt omadussõna (A) ja nimisõna (S), filtreeritakse kandidaadid:

| Sihtlemma | Sõnaliikide jaotus |
|-----------|-------------------|
| noor | A: 21 320, S: 5 881, V: 18, C: 3 |
| nooreke | A: 1 351, S: 51, V: 1 |
| nooruke | A: 439, S: 145 |

Kandidaatidena jäetakse alles ainult lemmad, mille peamine sõnaliik on A või S.

### 4. Sünonüümiskoori arvutamine

Põhimõõdik on **candidate_coverage** (kandidaadi katvus):

```
candidate_coverage = jagatud_mallid / kandidaadi_kõik_mallid
```

See näitab, kui suur osa kandidaadi kasutuskontekstidest kattub sihtlemmaga.

**Miks see töötab:**
- **Sünonüümid/variandid** kasutavad peaaegu ainult sihtlemma kontekste (kõrge katvus)
- **Antonüümid** jagavad mõningaid kontekste, kuid neil on palju unikaalseid (madal katvus)

**Näide:**
- `noorukene`: 45/84 = **53,6%** katvus → tõenäoline sünonüüm/deminutiiv
- `vana`: 163/11 157 = **1,5%** katvus → antonüüm, mitte sünonüüm

---

## Väljundfailid

### 1. `substitution_test_noor_SYNONYM_RANKED.csv`

**Peamine tulemfail** — järjestatud `candidate_coverage` järgi (parim sünonüümide leidmiseks).

| Veerg | Kirjeldus |
|-------|-----------|
| `rank` | Järjestuskoht (candidate_coverage järgi) |
| `lemma` | Kandidaatlemma, mis saab asendada sihtlemmat |
| `primary_pos` | Kandidaadi peamine sõnaliik (A=omadussõna, S=nimisõna) |
| `pos_distribution` | Sõnaliikide täielik jaotus, nt `{'A': 500, 'S': 100}` |
| `shared_templates` | Jagatud värsimallide arv sihtlemmaga |
| `target_occurrences_in_shared` | Mitu korda sihtlemma esineb jagatud mallides |
| `candidate_coverage` | **Põhimõõdik:** jagatud_mallid / kandidaadi_kõik_mallid |
| `candidate_occurrences_in_shared` | Mitu korda kandidaat esineb jagatud mallides |
| `jaccard_score` | Jaccardi sarnasus: jagatud / (siht + kand - jagatud) |
| `dice_score` | Dice'i koefitsient: 2×jagatud / (siht + kand) |
| `weighted_overlap` | Esinemissagedusega kaalutud kattuvus |
| `candidate_total_templates` | Kandidaadi unikaalsete mallide koguarv |
| `top_template_examples` | Näited populaarseimast jagatud mallidest |

### 2. `substitution_test_noor_POS_FILTERED.csv`

Sama sisu, kuid järjestatud `shared_templates` järgi (algne järjestus).

### 3. `substitution_test_noor_POS_FILTERED_detailed.csv`

Detailne fail, kus on **iga jagatud mall eraldi real**.

| Veerg | Kirjeldus |
|-------|-----------|
| `candidate_lemma` | Kandidaatlemma |
| `candidate_pos` | Kandidaadi sõnaliik |
| `template` | Värsimall koos `___` kohahoidjaga |
| `target_occurrences` | Sihtlemma esinemised selles mallis |
| `candidate_occurrences` | Kandidaadi esinemised selles mallis |
| `combined_occurrences` | Kokku (järjestamiseks) |
| `ratio_target_to_candidate` | Suhtarv siht/kandidaat |

---

## Tulemuste tõlgendamine

### Kõrge candidate_coverage (> 30%)
**Tõenäoline sünonüüm või morfoloogiline variant**

| Lemma | Katvus | Tõlgendus |
|-------|--------|-----------|
| noorukene | 53,6% | Deminutiiv lemmast 'noor' |
| nooruk | 41,2% | Lühendatud variant |
| nooru | 39,3% | Murdevariant |

### Madal candidate_coverage (< 5%)
**Antonüüm või semantiliselt kaugem sõna**

| Lemma | Katvus | Tõlgendus |
|-------|--------|-----------|
| vana | 1,5% | Antonüüm (vastand) |
| suur | 0,1% | Jagab süntaktilisi positsioone, kuid teine tähendusväli |

### Keskmine candidate_coverage (5–30%)
**Semantiline naaber, kohüponüüm või lähedane mõiste**

| Lemma | Katvus | Tõlgendus |
|-------|--------|-----------|
| hellake | 8,9% | "hell" deminutiiv, tähenduslikult lähedane |
| noormees | 4,9% | Tuletis samast tüvest |

---

## Meetodi piirangud

1. **Distribatiivne semantika ei erista sünonüüme antonüümidest automaatselt** — mõlemad esinevad sarnastes kontekstides. Seetõttu kasutame `candidate_coverage` mõõdikut.

2. **Harvad sõnad** võivad saada kunstlikult kõrge katvuse, kui neil on vähe malle.

3. **Funktsioonisõnad** (ja, ei, kui) jagavad palju malle juhuslikult — seetõttu filtreerime sõnaliigi järgi.

---

## Statistika

| Näitaja | Väärtus |
|---------|---------|
| Korpuse suurus | 108 969 laulu |
| Analüüsitud lemmade arv | 124 504 |
| Sihtlemmade malle kokku | 12 715 |
| Kandidaate enne POS-filtrit | 1 883 |
| Kandidaate pärast POS-filtrit | 397 |
| Tulemfailis lemmasid | 100 (top) |

---

## Genereerimine

- **Kuupäev:** 2025-12-14
- **Skript:** `substitution_test_noor_pos_filtered.py`
- **Python:** 3.10+
- **Sõltuvused:** Ainult Pythoni standardteek (json, gzip, csv, collections)

---

## Viited

- Harris, Z. S. (1954). Distributional structure. *Word*, 10(2-3), 146–162.
- Firth, J. R. (1957). A synopsis of linguistic theory, 1930–1955. *Studies in Linguistic Analysis*.
- Sahlgren, M. (2008). The distributional hypothesis. *Italian Journal of Linguistics*, 20(1), 33–54.
