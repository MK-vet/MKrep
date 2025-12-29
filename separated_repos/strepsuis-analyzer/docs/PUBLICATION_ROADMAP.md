# StrepSuis-Analyzer: Plan Rozwoju dla Niezależnej Publikacji

## Wersja dokumentu: 1.0.0
## Data: 2025-12-29
## Status: Propozycja

---

## Spis treści

1. [Podsumowanie obecnego stanu](#1-podsumowanie-obecnego-stanu)
2. [Cele publikacji](#2-cele-publikacji)
3. [Propozycje rozwoju funkcjonalności](#3-propozycje-rozwoju-funkcjonalności)
4. [Harmonogram wdrożenia](#4-harmonogram-wdrożenia)
5. [Wymagania techniczne](#5-wymagania-techniczne)
6. [Metryki sukcesu](#6-metryki-sukcesu)

---

## 1. Podsumowanie obecnego stanu

### ✅ Co jest gotowe

| Komponent | Status | Uwagi |
|-----------|--------|-------|
| Struktura pakietu | ✅ Kompletna | `pyproject.toml`, CLI entry points |
| Dokumentacja | ✅ Kompletna | README, USER_GUIDE, API, 2000+ linii |
| Testy | ✅ 85% pokrycia | Unit, integration, mathematical |
| CI/CD | ✅ Skonfigurowane | GitHub Actions dla testów i E2E |
| Docker | ✅ Gotowe | Dockerfile + docker-compose.yml |
| Dane przykładowe | ✅ Dostępne | 91 szczepów + dane syntetyczne |
| Licencja | ✅ MIT | CITATION.cff, SECURITY.md |

### ⚠️ Do rozwiązania przed publikacją

1. Aktualizacja URL-i w pyproject.toml (obecnie wskazują na MKrep)
2. Utworzenie dedykowanego repozytorium GitHub
3. Workflow publikacji do PyPI

---

## 2. Cele publikacji

### Cel główny
Opublikowanie `strepsuis-analyzer` jako **niezależnego, profesjonalnego narzędzia bioinformatycznego** dostępnego przez:
- PyPI (`pip install strepsuis-analyzer`)
- conda-forge
- Docker Hub
- Dedykowane repozytorium GitHub

### Cele dodatkowe
- Publikacja w czasopiśmie (JOSS, SoftwareX, Bioinformatics)
- Uzyskanie DOI przez Zenodo
- Budowa społeczności użytkowników

---

## 3. Propozycje rozwoju funkcjonalności

### 3.1 Rozszerzenie formatów danych wejściowych

**Priorytet: WYSOKI** | **Złożoność: ŚREDNIA**

#### Obecny stan
- CSV (jedyny obsługiwany format tabelaryczny)
- Newick (drzewa filogenetyczne)

#### Propozycja rozszerzenia

```
Nowe formaty wejściowe:
├── Bioinformatyczne
│   ├── FASTA/FASTQ - sekwencje nukleotydowe/aminokwasowe
│   ├── GenBank (.gb, .gbk) - adnotowane genomy
│   ├── VCF - warianty genetyczne (SNP/indels)
│   ├── GFF3/GTF - adnotacje genomowe
│   └── PHYLIP - dane filogenetyczne
├── Tabelaryczne
│   ├── TSV - Tab-separated values
│   ├── Excel (.xlsx, .xls) - import bezpośredni
│   ├── Parquet - dla dużych zbiorów danych
│   └── JSON/JSONL - dane strukturalne
└── Specjalistyczne
    ├── ResFinder output - wyniki AMR
    ├── CARD format - baza CARD
    ├── MLST output - wyniki typowania
    └── Roary/Panaroo - pan-genome matrices
```

#### Implementacja

**Nowy moduł: `src/strepsuis_analyzer/io/`**

```python
# io/__init__.py
from .fasta import read_fasta, write_fasta
from .genbank import read_genbank
from .vcf import read_vcf
from .excel import read_excel_advanced
from .auto_detect import detect_format, load_any

# io/auto_detect.py
def detect_format(file_path: str) -> str:
    """Automatyczne wykrywanie formatu pliku."""
    ...

def load_any(file_path: str) -> pd.DataFrame:
    """Uniwersalny loader z auto-detekcją."""
    ...
```

**Korzyści:**
- Eliminacja potrzeby ręcznej konwersji danych
- Integracja z popularnymi pipeline'ami bioinformatycznymi
- Obsługa standardowych formatów NCBI/EBI

---

### 3.2 REST API dla integracji zewnętrznej

**Priorytet: WYSOKI** | **Złożoność: WYSOKA**

#### Cel
Umożliwienie programowego dostępu do analiz bez potrzeby interfejsu webowego.

#### Architektura

```
strepsuis-analyzer/
├── src/strepsuis_analyzer/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI app
│   │   ├── routes/
│   │   │   ├── analysis.py   # /api/v1/analysis/*
│   │   │   ├── stats.py      # /api/v1/stats/*
│   │   │   ├── phylo.py      # /api/v1/phylogenetic/*
│   │   │   └── export.py     # /api/v1/export/*
│   │   ├── models/
│   │   │   ├── requests.py   # Pydantic models
│   │   │   └── responses.py
│   │   └── auth/             # Opcjonalna autoryzacja
│   │       └── api_key.py
```

#### Przykładowe endpointy

```yaml
API Endpoints:
  /api/v1/analysis:
    POST /upload:
      description: "Upload dataset for analysis"
      accepts: multipart/form-data
      returns: { session_id, file_info }

    POST /correlation:
      description: "Calculate correlations"
      body: { session_id, method, columns }
      returns: { correlation_matrix, p_values }

    POST /clustering:
      description: "Perform clustering"
      body: { session_id, algorithm, params }
      returns: { labels, metrics }

  /api/v1/stats:
    POST /hypothesis-test:
      description: "Statistical hypothesis testing"
      body: { data, test_type, groups }
      returns: { statistic, p_value, effect_size }

    POST /meta-analysis:
      description: "Meta-analysis of studies"
      body: { studies, model_type }
      returns: { pooled_effect, heterogeneity }

  /api/v1/phylogenetic:
    POST /compare-trees:
      description: "Compare phylogenetic trees"
      body: { tree1, tree2, metric }
      returns: { distance, support }

  /api/v1/export:
    POST /report:
      description: "Generate analysis report"
      body: { session_id, format, sections }
      returns: file (PDF/HTML/Excel)
```

#### CLI rozszerzenie

```bash
# Nowe komendy CLI
strepsuis-analyzer api --port 8000           # Start REST API server
strepsuis-analyzer api --workers 4           # Multi-worker mode
strepsuis-analyzer client analyze data.csv   # CLI client for API
```

**Korzyści:**
- Integracja z Nextflow/Snakemake pipelines
- Automatyzacja w środowiskach HPC
- Budowa ekosystemu narzędzi

---

### 3.3 Rozszerzone formaty eksportu

**Priorytet: ŚREDNI** | **Złożoność: NISKA**

#### Obecny stan
- Excel (.xlsx)
- HTML

#### Propozycja rozszerzenia

```
Nowe formaty eksportu:
├── Dokumenty
│   ├── PDF - profesjonalne raporty (ReportLab/WeasyPrint)
│   ├── LaTeX - dla publikacji naukowych
│   ├── Word (.docx) - python-docx
│   └── Markdown - dla GitHub/dokumentacji
├── Dane
│   ├── Parquet - efektywne przechowywanie
│   ├── HDF5 - duże zbiory danych
│   ├── SQLite - lokalna baza danych
│   └── JSON-LD - linked data
├── Wizualizacje
│   ├── Interactive HTML (standalone Plotly)
│   ├── SVG z metadanymi
│   └── Animated GIF (dla prezentacji)
└── Integracyjne
    ├── Jupyter Notebook (.ipynb)
    ├── R Markdown (.Rmd)
    └── Galaxy compatible output
```

#### Implementacja szablonów raportów

```python
# report_templates/__init__.py
TEMPLATES = {
    "scientific": "templates/scientific_report.html",
    "clinical": "templates/clinical_summary.html",
    "surveillance": "templates/surveillance_report.html",
    "publication": "templates/publication_figures.tex"
}

def generate_report(data, template="scientific", format="pdf"):
    """Generate formatted report from analysis results."""
    ...
```

---

### 3.4 System pluginów (rozszerzalność)

**Priorytet: ŚREDNI** | **Złożoność: WYSOKA**

#### Cel
Umożliwienie społeczności tworzenia własnych rozszerzeń bez modyfikacji kodu głównego.

#### Architektura

```python
# plugins/__init__.py
from pluggy import HookimplMarker, HookspecMarker

hookspec = HookspecMarker("strepsuis")
hookimpl = HookimplMarker("strepsuis")

class AnalyzerHookSpec:
    """Hook specifications for plugins."""

    @hookspec
    def register_analysis_method(self) -> dict:
        """Register new analysis method."""

    @hookspec
    def register_visualization(self) -> dict:
        """Register new visualization type."""

    @hookspec
    def register_data_loader(self) -> dict:
        """Register new data format loader."""

    @hookspec
    def modify_report(self, report_data: dict) -> dict:
        """Modify report before export."""
```

#### Przykładowy plugin

```python
# strepsuis_plugin_gwas/__init__.py
"""GWAS analysis plugin for strepsuis-analyzer."""

import strepsuis_analyzer.plugins as plugins

@plugins.hookimpl
def register_analysis_method():
    return {
        "name": "gwas",
        "display_name": "Genome-Wide Association Study",
        "function": run_gwas_analysis,
        "parameters": [
            {"name": "phenotype", "type": "column"},
            {"name": "correction", "type": "select", "options": ["bonferroni", "fdr"]}
        ]
    }

def run_gwas_analysis(data, phenotype, correction="fdr"):
    """Perform GWAS analysis."""
    ...
```

#### Instalacja pluginów

```bash
# Użytkownik może instalować pluginy przez pip
pip install strepsuis-plugin-gwas
pip install strepsuis-plugin-amr-prediction
pip install strepsuis-plugin-mlst-typing

# Pluginy są automatycznie wykrywane
strepsuis-analyzer --list-plugins
```

**Korzyści:**
- Rozszerzalność bez forków
- Społeczność może kontrybuować
- Specjalistyczne analizy dla różnych gatunków

---

### 3.5 Integracja z zewnętrznymi bazami danych

**Priorytet: ŚREDNI** | **Złożoność: ŚREDNIA**

#### Cel
Automatyczne pobieranie i wzbogacanie danych z publicznych baz.

#### Obsługiwane bazy

```yaml
Bazy danych:
  Sekwencje i genomy:
    - NCBI GenBank/RefSeq
    - ENA (European Nucleotide Archive)
    - DDBJ

  AMR (oporność na antybiotyki):
    - CARD (Comprehensive Antibiotic Resistance Database)
    - ResFinder
    - AMRFinderPlus
    - NCBI AMR Reference Gene Database

  Typowanie:
    - PubMLST (MLST profiles)
    - CGE databases (serotyping)
    - BIGSdb

  Wirulencja:
    - VFDB (Virulence Factor Database)
    - Victors

  Taksonomia:
    - GTDB (Genome Taxonomy Database)
    - NCBI Taxonomy

  Gatunkowo-specyficzne:
    - StreptDB (dla Streptococcus)
    - BacDive (bacterial diversity)
```

#### Implementacja

```python
# databases/__init__.py
class DatabaseConnector:
    """Universal connector for bioinformatics databases."""

    def __init__(self, cache_dir="~/.strepsuis_cache"):
        self.cache = CacheManager(cache_dir)

    async def fetch_amr_genes(self, sequence: str, database="card") -> dict:
        """Query AMR database for resistance genes."""
        ...

    async def fetch_mlst_profile(self, genome: str, scheme="ssuis") -> dict:
        """Get MLST profile from PubMLST."""
        ...

    async def enrich_metadata(self, strain_ids: list) -> pd.DataFrame:
        """Enrich local data with database metadata."""
        ...
```

#### UI integracja

```
Streamlit Interface:
├── "Fetch from Database" button
├── Database selector (CARD, PubMLST, VFDB...)
├── Query builder (strain ID, gene name, accession)
├── Results preview
└── "Merge with current dataset" option
```

---

### 3.6 Tryb offline / Desktop Application

**Priorytet: NISKI** | **Złożoność: WYSOKA**

#### Cel
Umożliwienie pracy bez połączenia internetowego i jako aplikacja desktopowa.

#### Opcje implementacji

```
Podejście 1: PyInstaller Bundle
├── Jeden plik wykonywalny (.exe, .app, .AppImage)
├── Wbudowany Python + wszystkie zależności
├── Streamlit uruchamiany lokalnie
└── ~200-500 MB rozmiar

Podejście 2: Electron + Python Backend
├── Native GUI (cross-platform)
├── Python backend jako subprocess
├── Lepsza integracja z systemem
└── ~300-600 MB rozmiar

Podejście 3: Tauri + Python (najlżejsze)
├── Rust-based GUI framework
├── Python jako backend
├── ~50-100 MB rozmiar
└── Wymaga więcej pracy
```

#### Rekomendacja: PyInstaller

```bash
# Build script
pyinstaller --onefile \
    --add-data "data:data" \
    --add-data "templates:templates" \
    --name strepsuis-analyzer \
    src/strepsuis_analyzer/desktop_launcher.py
```

---

### 3.7 Integracja z Jupyter Notebooks

**Priorytet: ŚREDNI** | **Złożoność: NISKA**

#### Cel
Umożliwienie użycia funkcji analizatora bezpośrednio w notebookach.

#### Implementacja

```python
# jupyter/__init__.py
"""Jupyter integration for strepsuis-analyzer."""

from IPython.display import display, HTML
import ipywidgets as widgets

class InteractiveAnalyzer:
    """Interactive analyzer widget for Jupyter."""

    def __init__(self, data: pd.DataFrame):
        self.data = data
        self._build_ui()

    def _build_ui(self):
        """Build interactive widget UI."""
        self.method_selector = widgets.Dropdown(
            options=['correlation', 'clustering', 'hypothesis_test'],
            description='Analysis:'
        )
        # ... more widgets

    def display(self):
        """Display interactive widget."""
        display(self.ui)

# Użycie w Jupyter:
# from strepsuis_analyzer.jupyter import InteractiveAnalyzer
# analyzer = InteractiveAnalyzer(my_data)
# analyzer.display()
```

#### Magic commands

```python
# jupyter/magics.py
from IPython.core.magic import register_line_magic, register_cell_magic

@register_cell_magic
def strepsuis_analyze(line, cell):
    """
    %%strepsuis_analyze correlation
    data = my_dataframe
    method = spearman
    """
    ...
```

---

### 3.8 Wsparcie wielogatunkowe (generalizacja)

**Priorytet: WYSOKI** | **Złożoność: ŚREDNIA**

#### Cel
Rozszerzenie narzędzia poza *Streptococcus suis* na inne gatunki bakteryjne.

#### Propozycja rebrandingu

```
Opcja 1: Zachowanie nazwy z rozszerzeniem
  strepsuis-analyzer → strepsuis-analyzer (dla S. suis)
                     + bacterial-analyzer (generyczny)

Opcja 2: Generyczna nazwa
  strepsuis-analyzer → BacAnalyzer
                     → MicrobeStats
                     → GenoPhenoAnalyzer

Opcja 3: Modułowa architektura
  core-analyzer (uniwersalny silnik)
  ├── strepsuis-module (S. suis specyficzny)
  ├── ecoli-module (E. coli specyficzny)
  ├── staph-module (S. aureus specyficzny)
  └── generic-module (dowolny gatunek)
```

#### Implementacja profilów gatunkowych

```python
# species_profiles/__init__.py
SPECIES_PROFILES = {
    "streptococcus_suis": {
        "display_name": "Streptococcus suis",
        "mlst_scheme": "ssuis",
        "amr_databases": ["card", "resfinder"],
        "virulence_database": "vfdb",
        "reference_genome": "NC_012925.1",
        "serotypes": ["1", "2", "3", ...],
        "default_analyses": ["amr", "virulence", "mlst", "serotyping"]
    },
    "escherichia_coli": {
        "display_name": "Escherichia coli",
        "mlst_scheme": "ecoli_achtman",
        # ...
    },
    "staphylococcus_aureus": {
        "display_name": "Staphylococcus aureus",
        "mlst_scheme": "saureus",
        # ...
    },
    "generic": {
        "display_name": "Generic Bacterial Analysis",
        # Minimalna konfiguracja dla dowolnego gatunku
    }
}

def get_profile(species: str) -> dict:
    """Get species-specific configuration."""
    return SPECIES_PROFILES.get(species, SPECIES_PROFILES["generic"])
```

---

### 3.9 Internacjonalizacja (i18n)

**Priorytet: NISKI** | **Złożoność: ŚREDNIA**

#### Cel
Wsparcie dla wielu języków w interfejsie.

#### Implementacja

```python
# i18n/__init__.py
import gettext
from pathlib import Path

LOCALES_DIR = Path(__file__).parent / "locales"
SUPPORTED_LANGUAGES = ["en", "pl", "es", "de", "zh", "pt"]

def get_translator(lang: str = "en"):
    """Get translator for specified language."""
    return gettext.translation(
        "strepsuis-analyzer",
        localedir=LOCALES_DIR,
        languages=[lang],
        fallback=True
    )

# Użycie
_ = get_translator("pl").gettext
print(_("Correlation Analysis"))  # "Analiza korelacji"
```

#### Struktura plików językowych

```
i18n/
├── locales/
│   ├── en/LC_MESSAGES/strepsuis-analyzer.po
│   ├── pl/LC_MESSAGES/strepsuis-analyzer.po
│   ├── es/LC_MESSAGES/strepsuis-analyzer.po
│   └── ...
└── extract_strings.py  # Skrypt ekstrakcji stringów
```

---

### 3.10 Zaawansowane funkcje analityczne

**Priorytet: ŚREDNI** | **Złożoność: WYSOKA**

#### Nowe metody statystyczne

```python
# Propozycje nowych analiz:

1. Machine Learning:
   - Random Forest feature importance
   - Gradient Boosting classification
   - SVM dla klasyfikacji fenotypowej
   - Neural network (opcjonalnie, z TensorFlow Lite)

2. Analiza przeżycia (Survival Analysis):
   - Kaplan-Meier curves
   - Cox proportional hazards
   - Log-rank test

3. Analiza sieci (Network Analysis):
   - Gene co-occurrence networks
   - AMR gene networks
   - Strain similarity networks
   - Community detection

4. Genomika populacyjna:
   - Tajima's D
   - Fu and Li's statistics
   - Linkage disequilibrium
   - Population structure (STRUCTURE-like)

5. Analiza pan-genomu:
   - Core/accessory genome analysis
   - Gene presence/absence patterns
   - Heap's law fitting
   - Functional enrichment
```

---

## 4. Harmonogram wdrożenia

### Faza 1: Przygotowanie do publikacji (natychmiastowe)
- [ ] Utworzenie dedykowanego repozytorium GitHub
- [ ] Aktualizacja URL-i w pyproject.toml
- [ ] Konfiguracja GitHub Actions dla PyPI
- [ ] Publikacja na PyPI (wersja 1.0.0)
- [ ] Rejestracja DOI przez Zenodo

### Faza 2: Podstawowe rozszerzenia
- [ ] 3.1 Rozszerzenie formatów wejściowych (FASTA, VCF, Excel import)
- [ ] 3.3 Rozszerzone formaty eksportu (PDF, LaTeX)
- [ ] 3.8 Wsparcie wielogatunkowe (profile gatunkowe)

### Faza 3: Zaawansowane funkcje
- [ ] 3.2 REST API
- [ ] 3.5 Integracja z bazami danych (CARD, PubMLST)
- [ ] 3.7 Integracja z Jupyter

### Faza 4: Ekosystem
- [ ] 3.4 System pluginów
- [ ] 3.10 Zaawansowane funkcje analityczne
- [ ] 3.6 Aplikacja desktopowa (opcjonalnie)

### Faza 5: Społeczność
- [ ] 3.9 Internacjonalizacja
- [ ] Dokumentacja wideo
- [ ] Warsztaty/tutoriale
- [ ] Publikacja naukowa (JOSS/SoftwareX)

---

## 5. Wymagania techniczne

### Nowe zależności (propozycje)

```toml
# pyproject.toml - rozszerzenia

[project.optional-dependencies]
api = [
    "fastapi>=0.100.0",
    "uvicorn>=0.23.0",
    "pydantic>=2.0.0",
]
formats = [
    "pyvcf3>=1.0.0",
    "gffpandas>=1.2.0",
    "openpyxl>=3.1.0",
]
databases = [
    "aiohttp>=3.8.0",
    "httpx>=0.24.0",
]
pdf = [
    "weasyprint>=59.0",
    "reportlab>=4.0.0",
]
jupyter = [
    "ipywidgets>=8.0.0",
    "jupyter>=1.0.0",
]
ml = [
    "xgboost>=1.7.0",
    "lightgbm>=4.0.0",
]
all = [
    "strepsuis-analyzer[api,formats,databases,pdf,jupyter,ml]"
]
```

### Struktura rozszerzona

```
strepsuis-analyzer/
├── src/strepsuis_analyzer/
│   ├── core/              # Rdzeń (obecna funkcjonalność)
│   ├── api/               # REST API (3.2)
│   ├── io/                # Formaty I/O (3.1, 3.3)
│   ├── databases/         # Integracja baz (3.5)
│   ├── plugins/           # System pluginów (3.4)
│   ├── species/           # Profile gatunkowe (3.8)
│   ├── jupyter/           # Integracja Jupyter (3.7)
│   ├── i18n/              # Internacjonalizacja (3.9)
│   └── advanced/          # Zaawansowane analizy (3.10)
```

---

## 6. Metryki sukcesu

### KPI dla publikacji

| Metryka | Cel (6 miesięcy) | Cel (12 miesięcy) |
|---------|------------------|-------------------|
| Pobrania PyPI | 500 | 2,000 |
| GitHub Stars | 50 | 200 |
| Cytowania | 5 | 20 |
| Issues/PRs | 20 | 50 |
| Aktywni kontrybutorzy | 3 | 10 |
| Pluginy społeczności | 0 | 5 |

### Kryteria jakości

- [ ] Pokrycie testami ≥ 85%
- [ ] Dokumentacja API 100%
- [ ] Zero krytycznych CVE
- [ ] Czas odpowiedzi API < 500ms (p95)
- [ ] Czas ładowania UI < 3s

---

## 7. Podsumowanie

### Priorytety rekomendowane

1. **NATYCHMIAST**: Publikacja obecnej wersji (jest gotowa!)
2. **WYSOKI**: Rozszerzenie formatów (3.1), REST API (3.2), Wielogatunkowość (3.8)
3. **ŚREDNI**: Eksport PDF/LaTeX (3.3), Bazy danych (3.5), Jupyter (3.7)
4. **NISKI**: Pluginy (3.4), Desktop (3.6), i18n (3.9)

### Rekomendacja

Narzędzie jest **już gotowe do publikacji** w obecnej formie. Proponowane rozszerzenia mogą być wdrażane **iteracyjnie po publikacji** wersji 1.0.0, co pozwoli na:
- Szybkie zdobycie użytkowników
- Zbieranie feedbacku
- Priorytetyzację funkcji na podstawie rzeczywistych potrzeb

---

## Kontakt

Pytania dotyczące tego planu: [maintainer email]

---

*Dokument wygenerowany: 2025-12-29*
*Wersja: 1.0.0*
