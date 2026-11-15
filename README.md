# ENEM Analytics

An exploratory and statistical analysis of the official 2025 ENEM microdata, comparing performance across Brazilian states, regions, knowledge areas and school types (public vs. private).

Data source: [INEP microdata](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem). State boundaries: IBGE territorial mesh (2025).

## Questions

- Which states and regions have the highest and lowest mean scores?
- Which region stands out in each knowledge area, and how different are states within a region?
- How large is the gap between public and private school students, and does it repeat across regions and states?
- In which areas is the gap largest?

## Key results

All means refer to participants present in each test, with blank objective answer sheets excluded (see Methodology). They describe exam takers, not the whole population, and they are not causal.

**National means**

| CN | CH | LC | MT | Essay (with zeros) | Essay (valid only) |
|---|---|---|---|---|---|
| 500.1 | 512.5 | 532.5 | 520.1 | 580.8 | 618.7 |

CN = natural sciences, CH = human sciences, LC = languages, MT = mathematics. Each area has its own scale, so raw scores of different areas are not compared with each other.

**Means by region of the exam**

| Region | CN | CH | LC | MT | Essay (with zeros) | Essay (valid only) |
|---|---|---|---|---|---|---|
| Southeast | 514.1 | 531.3 | 551.3 | 551.7 | 609.8 | 632.7 |
| South | 512.5 | 529.9 | 550.2 | 548.5 | 592.1 | 620.3 |
| Center-West | 504.8 | 516.5 | 535.9 | 524.1 | 593.2 | 624.4 |
| Northeast | 490.0 | 497.1 | 518.7 | 497.3 | 563.0 | 613.5 |
| North | 476.3 | 487.5 | 502.4 | 471.1 | 532.3 | 585.0 |

- The Southeast is highest and the North lowest in every column. The South is within about 1 to 3 points of the Southeast in the objective tests.
- Which state is "highest" depends on the column (for example DF in CN and CH, SP in LC and MT, MG in both essay averages).
- The spread of individual scores inside a state is larger than the distance between the highest and the lowest state mean in LC.

**Private minus public school mean (participants with school information)**

| CN | CH | LC | MT | Essay (with zeros) | Essay (valid only) |
|---|---|---|---|---|---|
| 75.0 | 77.8 | 65.5 | 132.3 | 193.2 | 150.7 |

- In standard deviations of each area the gap is similar across the four objective tests (0.91 in LC to 1.06 in MT). In raw points it looks much larger in Mathematics because Mathematics scores are more spread out.
- The private mean is higher in every region and in every state with enough private-school students. The gap in LC is largest in the Northeast and smallest in the South and Southeast; at state level it ranges from about 47 points (SP, SC) to about 88 (AM).
- Federal schools are close to private schools and well above state and municipal schools, a difference hidden when all are grouped as "public".
- The distributions overlap: about 14% of public-school students score above the private-school median in LC.

Charts are in `images/` and are produced by notebooks 03 to 05.

## Methodology

- **File used:** `RESULTADOS_2025.csv`. The `PARTICIPANTES` file cannot be joined to it: according to the INEP dictionary, the identifiers are not related by design.
- **Unit of analysis:** records in the results file, not unique people who took the exam. Each area is averaged over records marked present in that area (`TP_PRESENCA_* == 1`). About 28% to 32% of records are absentees and have no score.
- **Blank answer sheets:** in all four objective tests, every record with score 0 has all 45 answers blank, and every blank sheet has score 0 (CN 775, CH 9,087, LC 2,361, MT 893 records). The 0 is assigned to a blank sheet rather than estimated by IRT. These records are excluded from objective means by recoding presence to code 3 (a code created for this project, not in the INEP dictionary); the original value is kept in `TP_PRESENCA_*_ORIG`.
- **Essay:** reported two ways, including zeros (invalid essays receive 0, status codes 2 to 9) and with valid essays only (`TP_STATUS_REDACAO == 1`).
- **Geography:** state means use the state where the exam was taken (`SG_UF_PROVA`), because municipality of residence was removed from the 2025 microdata. State gaps between school types use the state of the school (`SG_UF_ESC`) and only states with at least 1,000 private-school students; the effect of this threshold was tested at 500, 1,000 and 2,000.
- **School information:** comes from the 2025 School Census linked by CPF, restricted to final-year high school enrollments (INEP read-me, pp. 7 to 8). Participants without such an enrollment have no school information.
- **Comparing areas:** each area has its own scale (INEP participant guide). Comparisons are made within an area. Standard deviations and z-scores are used only to describe relative position inside each area.

## Limitations

- About 61% of present participants have no school information, so public vs. private results apply only to participants matched to a final-year enrollment, which is not a random sample.
- The socioeconomic questionnaire is in the file that cannot be linked, so the school-type gap mixes the effect of the school with the profile of its students. No result here is causal.
- Trainees (`IN_TREINEIRO`) cannot be identified in the results file.
- Absence rates differ by state (about 21% to 41% in the first exam day), so state means describe different shares of each state's registered population.
- State of the exam is not state of residence.
- INEP advises against using these data to rank schools; this project reports only aggregates by region, state and school type.
- INEP removed participants of a few exam versions with very few takers to prevent identification.
- State-level extremes with small samples are fragile. For example, the smallest public-private gap in MT changes between AP, RO and SP depending on the minimum sample size.
- The reason why some participants marked as present left the objective tests blank is not documented in the data.
- Differences of 1 to 2 points between neighboring states are small compared with the spread of individual scores and should not be ranked.

## Project structure

```
enem-analytics/
├── data/
│   ├── raw/            INEP microdata and IBGE shapefile (not versioned)
│   └── processed/      cached Parquet files (not versioned)
├── images/             charts produced by the notebooks
├── notebooks/
│   ├── 01_initial_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_geographic_analysis.ipynb
│   ├── 04_public_vs_private.ipynb
│   └── 05_analysis_by_area.ipynb
├── src/
│   ├── config.py       constants, paths, region mapping
│   ├── load.py         loading, recoding, derived columns
│   ├── stats.py        tables and statistics
│   └── plots.py        charts and maps
├── requirements.txt
└── README.md
```

Notebook 02 documents how the data was first inspected and cleaned. Notebooks 03 to 05 hold the analysis and use the functions in `src/`.

## How to reproduce

1. Create and activate a virtual environment, then install the dependencies (developed with Python 3.14):

   ```powershell
   py -3.14 -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Download the ENEM 2025 microdata from INEP and extract it so that the files are in `data/raw/microdados_enem_2025/` (with the `DADOS`, `DICIONÁRIO` and `LEIA-ME E DOCUMENTOS TÉCNICOS` folders).
3. Download the IBGE state boundaries (shapefile, 2025) and extract them to `data/raw/ibge_uf_2025/`. The maps are skipped if this folder is missing.
4. Open the notebooks in order and run them. The first call to `prepare_dataset()` reads the 2 GB results file (a few minutes) and caches the selected columns in `data/processed/`.

The full results file has about 4.8 million records. Only 14 columns are loaded.

## Tools

Python, Pandas, NumPy, Matplotlib, Seaborn, GeoPandas, Jupyter, Git.
