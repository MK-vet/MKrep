#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
StrepSuisPhyloCluster
Integrative Phylogenetic Clustering Tool and Binary Trait Profiling of Antimicrobial Resistance
and Virulence in Streptococcus suis

Single-file, Colab-ready pipeline that produces one interactive HTML report with a visual/UX style
aligned to the "StrepSuis-AMR-Vir-Cluster" report.

Key capabilities
- Tree-aware clustering (+ ensemble fallback: KMeans/GMM/DBSCAN with Optuna)
- Evolutionary metrics (PD, beta diversity, proxy rates, phylogenetic signal)
- Trait profiling (frequencies, chi-square + FDR, log-odds, RF importance bootstrap)
- Association rules (mlxtend), MCA (prince)
- One HTML report (Bootstrap 5 + DataTables, CSV export), shared CSS theme

Note:
- Visual styling and component behavior match the AMR report (DataTables: pageLength=25, CSV export).
- Section order is re-organized into five parts for logical flow.
"""

# =========================
# 0) Robust auto-installer
# =========================
import sys, subprocess, importlib, os, warnings, random, base64, datetime, re
from io import BytesIO
from itertools import combinations

def _pip_install(pkgs):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "--upgrade", *pkgs])

def _ensure(pip_pkg: str, import_name: str):
    """Ensure a library is importable. If import fails, pip-install then import."""
    try:
        return importlib.import_module(import_name or pip_pkg)
    except Exception:
        _pip_install([pip_pkg])
        return importlib.import_module(import_name or pip_pkg)

# Core scientific stack
_ensure("numpy", "numpy"); _ensure("pandas", "pandas")
_ensure("matplotlib", "matplotlib"); _ensure("seaborn", "seaborn")
_ensure("scipy", "scipy")

# Bio & ML toolchain
_ensure("biopython", "Bio"); _ensure("scikit-learn", "sklearn")
_ensure("umap-learn", "umap"); _ensure("mlxtend", "mlxtend")
_ensure("optuna", "optuna"); _ensure("statsmodels", "statsmodels")
_ensure("prince", "prince"); _ensure("plotly", "plotly")
_ensure("tqdm", "tqdm"); _ensure("jinja2", "jinja2")

# Now imports are safe
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Bio import Phylo
from sklearn.cluster import KMeans, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import cdist
from scipy.stats import chi2_contingency, fisher_exact
from statsmodels.stats.multitest import multipletests
from umap import UMAP
from tqdm import tqdm
import optuna
import plotly.express as px
import plotly.graph_objects as go
import jinja2
import prince
from mlxtend.frequent_patterns import apriori, association_rules
from multiprocessing import Pool, cpu_count
from functools import partial

# ------------------ Global settings ------------------
warnings.filterwarnings("ignore", category=UserWarning)
random.seed(42); np.random.seed(42)
os.environ["PYTHONHASHSEED"]="0"; os.environ["OMP_NUM_THREADS"]="1"; os.environ["MKL_NUM_THREADS"]="1"
sns.set(style="whitegrid")


# =====================================================
# 1) Template (AMR-like), single source of truth
# =====================================================
def ensure_template_and_css(output_folder: str):
    """Create Jinja2 template + ensure shared_styles.css next to the final HTML (same folder)."""
    import shutil
    os.makedirs("templates", exist_ok=True)
    template_path = os.path.join("templates", "report_template.html")

    # Template with reorganized sections (PART I–V). Visuals/UX unchanged.
    template_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{{ title }}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>

  <!-- CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.7/css/dataTables.bootstrap5.min.css">
  <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/buttons/2.4.2/css/buttons.bootstrap5.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

  <!-- Plotly -->
  <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

  <!-- Shared theme -->
  <link rel="stylesheet" href="shared_styles.css"/>

  <style>
    :root{
      --primary-color:#2c3e50; --secondary-color:#3498db; --light:#f8f9fa;
      --text:#2c3e50; --muted:#6c757d; --border:#dee2e6;
    }
    body{background:#fff; color:var(--text)}
    .container-wide{max-width:1400px; margin:0 auto; padding:1.25rem;}
    .section-card{background:#fff; border:1px solid var(--border); border-radius:8px; box-shadow:0 2px 4px rgba(0,0,0,.05); margin-bottom:1.25rem;}
    .section-header{background:linear-gradient(135deg,var(--primary-color),var(--secondary-color)); color:#fff; padding:.75rem 1rem; border-radius:8px 8px 0 0;}
    .section-content{padding:1rem;}
    .plotly-wrap{border:1px solid #e5e7eb; border-radius:6px; overflow:hidden;}
    .nav-pills .nav-link{border:1px solid var(--border); margin-right:.4rem; margin-bottom:.4rem;}
    .nav-pills .nav-link.active{background:var(--secondary-color); border-color:var(--secondary-color);}
    table.display thead th{background:linear-gradient(135deg,var(--primary-color),var(--secondary-color)); color:#fff;}
    .methodology p{margin-bottom:.5rem;}
    .method-box{background:linear-gradient(135deg,#f8f9fa,#ffffff); border-left:4px solid #e74c3c; padding:1rem; margin:.8rem 0; border-radius:0 6px 6px 0;}
    .part-label{font-weight:600; color:var(--muted); text-transform:uppercase; letter-spacing:.03em;}
  </style>

</head>
<body>
  <div class="container-wide">
    <header class="section-card">
      <div class="section-header d-flex align-items-center">
        <h1 class="h4 m-0"><i class="fa-solid fa-diagram-project me-2"></i>{{ title }}</h1>
      </div>
      <div class="section-content">
        <p class="m-0 text-muted">Generated on: {{ date }}</p>
      </div>
    </header>

    <!-- Navigation with improved structure -->
    <nav class="section-card">
      <div class="section-content">
        <div class="row">
          <div class="col-12">
            <h6 class="part-label mb-2">PART I: FOUNDATIONAL</h6>
            <ul class="nav nav-pills mb-3">
              <li class="nav-item"><a class="nav-link active" href="#overview">Overview</a></li>
              <li class="nav-item"><a class="nav-link" href="#methodology">Methodology</a></li>
            </ul>

            <h6 class="part-label mb-2">PART II: PHYLOGENETIC STRUCTURE</h6>
            <ul class="nav nav-pills mb-3">
              <li class="nav-item"><a class="nav-link" href="#phylogeny">Phylogenetic Analysis</a></li>
              <li class="nav-item"><a class="nav-link" href="#clustering">Clustering Results</a></li>
              <li class="nav-item"><a class="nav-link" href="#evolution">Evolutionary Metrics</a></li>
            </ul>

            <h6 class="part-label mb-2">PART III: TRAIT PROFILING</h6>
            <ul class="nav nav-pills mb-3">
              <li class="nav-item"><a class="nav-link" href="#traits">Trait Analysis</a></li>
              <li class="nav-item"><a class="nav-link" href="#associations">Trait Associations</a></li>
              <li class="nav-item"><a class="nav-link" href="#comparative">Comparative Analysis</a></li>
            </ul>

            <h6 class="part-label mb-2">PART IV: ADVANCED ANALYSES</h6>
            <ul class="nav nav-pills mb-3">
              <li class="nav-item"><a class="nav-link" href="#mca">Multivariate Analysis</a></li>
              <li class="nav-item"><a class="nav-link" href="#statistical">Statistical Validation</a></li>
            </ul>

            <h6 class="part-label mb-2">PART V: RESOURCES</h6>
            <ul class="nav nav-pills">
              <li class="nav-item"><a class="nav-link" href="#downloads">Downloads</a></li>
            </ul>
          </div>
        </div>
      </div>
    </nav>

    <!-- PART I: FOUNDATIONAL -->
    <section id="overview" class="section-card">
      <div class="section-header"><h2 class="h5 m-0">1. Overview</h2></div>
      <div class="section-content">
        <div class="row g-3">
          <div class="col-lg-6">
            <h6>Configuration</h6>
            <div class="table-responsive">
              <table class="table table-sm table-striped mb-0">
                <tbody>
                {% for key, value in config.items() %}
                  <tr><td class="fw-semibold">{{ key }}</td><td>{{ value }}</td></tr>
                {% endfor %}
                </tbody>
              </table>
            </div>
          </div>
          <div class="col-lg-6">
            <h6>Summary (Clusters)</h6>
            <div class="table-responsive">{{ results.summary_stats|safe }}</div>
          </div>
        </div>
      </div>
    </section>

    <section id="methodology" class="section-card">
      <div class="section-header"><h2 class="h5 m-0">2. Methodology & Statistical Tests</h2></div>
      <div class="section-content methodology">
        {{ results.methodology|safe }}
      </div>
    </section>

    <!-- PART II: PHYLOGENETIC STRUCTURE -->
    <section id="phylogeny" class="section-card">
      <div class="section-header"><h2 class="h5 m-0">3. Phylogenetic Analysis</h2></div>
      <div class="section-content">
        <div class="row g-3">
          <div class="col-lg-8"><div class="plotly-wrap">{{ results.tree_plot|safe }}</div></div>
          <div class="col-lg-4"><div class="table-responsive">{{ results.tree_stats|safe }}</div></div>
        </div>
      </div>
    </section>

    <section id="clustering" class="section-card">
      <div class="section-header"><h2 class="h5 m-0">4. Clustering Results</h2></div>
      <div class="section-content">
        <div class="row g-3">
          <div class="col-lg-6"><div class="plotly-wrap">{{ results.umap_plot|safe }}</div></div>
          <div class="col-lg-6"><div class="plotly-wrap">{{ results.cluster_distribution|safe }}</div></div>
        </div>
        <div class="mt-3">
          <div class="table-responsive">{{ results.cluster_validation|safe }}</div>
        </div>
      </div>
    </section>

    <section id="evolution" class="section-card">
      <div class="section-header"><h2 class="h5 m-0">5. Evolutionary Metrics</h2></div>
      <div class="section-content">
        <div class="row g-3">
          <div class="col-lg-6"><div class="table-responsive">{{ results.evolutionary_metrics|safe }}</div></div>
          <div class="col-lg-6"><div class="plotly-wrap">{{ results.beta_diversity|safe }}</div></div>
        </div>
        <div class="row g-3 mt-1">
          <div class="col-lg-6"><div class="plotly-wrap">{{ results.evolution_rates|safe }}</div></div>
          <div class="col-lg-6"><div class="table-responsive">{{ results.phylogenetic_signal|safe }}</div></div>
        </div>
      </div>
    </section>

    <!-- PART III: TRAIT PROFILING -->
    <section id="traits" class="section-card">
      <div class="section-header"><h2 class="h5 m-0">6. Trait Analysis</h2></div>
      <div class="section-content">
        {{ results.trait_analysis|safe }}
      </div>
    </section>

    <section id="associations" class="section-card">
      <div class="section-header"><h2 class="h5 m-0">7. Trait Associations</h2></div>
      <div class="section-content">
        <div class="row g-3">
          <div class="col-lg-6"><div class="table-responsive">{{ results.global_log_odds|safe }}</div></div>
          <div class="col-lg-6"><div class="table-responsive">{{ results.cluster_log_odds|safe }}</div></div>
        </div>
        <div class="mt-3"><div class="table-responsive">{{ results.association_rules|safe }}</div></div>
      </div>
    </section>

    <section id="comparative" class="section-card">
      <div class="section-header"><h2 class="h5 m-0">8. Comparative Analysis</h2></div>
      <div class="section-content">
        <div class="row g-3">
          <div class="col-lg-6"><div class="table-responsive">{{ results.shared_features|safe }}</div></div>
          <div class="col-lg-6"><div class="table-responsive">{{ results.unique_features|safe }}</div></div>
        </div>
        <div class="mt-3"><div class="table-responsive">{{ results.pairwise_fdr|safe }}</div></div>
      </div>
    </section>

    <!-- PART IV: ADVANCED ANALYSES -->
    <section id="mca" class="section-card">
      <div class="section-header"><h2 class="h5 m-0">9. Multivariate Analysis (MCA)</h2></div>
      <div class="section-content">
        <div class="row g-3">
          <div class="col-lg-6"><div class="plotly-wrap">{{ results.mca_row_plot|safe }}</div></div>
          <div class="col-lg-6"><div class="plotly-wrap">{{ results.mca_column_plot|safe }}</div></div>
        </div>
        <div class="mt-3"><div class="table-responsive">{{ results.mca_summary|safe }}</div></div>
      </div>
    </section>

    <section id="statistical" class="section-card">
      <div class="section-header"><h2 class="h5 m-0">10. Statistical Validation</h2></div>
      <div class="section-content">
        <p class="text-muted">Bootstrap summaries and robustness checks (summary of RF bootstrap importances; see Trait Analysis for per-category details).</p>
        <div class="table-responsive">{{ results.bootstrap_feature_importance|safe }}</div>
        {% if results.bootstrap_log_odds %}
        <div class="mt-3"><div class="table-responsive">{{ results.bootstrap_log_odds|safe }}</div></div>
        {% endif %}
      </div>
    </section>

    <!-- PART V: RESOURCES -->
    <section id="downloads" class="section-card">
      <div class="section-header"><h2 class="h5 m-0">11. Downloads</h2></div>
      <div class="section-content">{{ results.download_section|safe }}</div>
    </section>

    <footer class="section-card">
      <div class="section-content text-center">
        <span>Single-file HTML report using Bootstrap 5 + DataTables (CSV export).</span>
      </div>
    </footer>
  </div>

  <!-- Scripts - EXACT ORDER -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
  <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
  <script src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js"></script>
  <script src="https://cdn.datatables.net/1.13.7/js/dataTables.bootstrap5.min.js"></script>
  <script src="https://cdn.datatables.net/buttons/2.4.2/js/dataTables.buttons.min.js"></script>
  <script src="https://cdn.datatables.net/buttons/2.4.2/js/buttons.bootstrap5.min.js"></script>
  <script src="https://cdn.datatables.net/buttons/2.4.2/js/buttons.html5.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>

  <script>
    // DataTables config (AMR-like: CSV-only export, pageLength=25)
    $.extend(true, DataTable.defaults, {
        pageLength: 25,
        responsive: true,
        dom: 'Bfrtip',
        buttons: [{ extend: 'csv', className: 'btn btn-primary btn-sm' }],
        language: {
            search: "Search:",
            lengthMenu: "Show _MENU_ entries",
            info: "Showing _START_ to _END_ of _TOTAL_ entries"
        }
    });

    // Init all DataTables
    $(function() {
        $('.display').each(function() {
            if (!$(this).hasClass('dataTable')) $(this).DataTable();
        });

        // Smooth scroll + active state (use all pills)
        $('.nav-pills a').on('click', function(e) {
            e.preventDefault();
            const target = $(this.getAttribute('href'));
            if (target.length) {
                $('html, body').animate({ scrollTop: target.offset().top - 20 }, 500);
                $('.nav-pills a').removeClass('active'); $(this).addClass('active');
            }
        });

        $(window).on('scroll', function() {
            let current = '';
            $('.nav-pills a').each(function() {
                const section = $(this.getAttribute('href'));
                if (section.offset() && section.offset().top <= $(window).scrollTop() + 100) current = this.getAttribute('href');
            });
            if (current) {
                $('.nav-pills a').removeClass('active');
                $('.nav-pills a[href="' + current + '"]').addClass('active');
            }
        });
    });
  </script>
</body>
</html>
"""
    with open(template_path, "w", encoding="utf-8") as f:
        f.write(template_html)

    # Ensure shared_styles.css next to the output HTML
    css_target = os.path.join(output_folder, "shared_styles.css")
    if not os.path.isfile(css_target):
        for cand in ["shared_styles.css", "/mnt/data/shared_styles.css", "./shared_styles.css"]:
            if os.path.isfile(cand):
                shutil.copyfile(cand, css_target); break
        else:
            fallback = """:root{
  --primary-color:#2c3e50;--secondary-color:#3498db;--light:#f8f9fa;
  --text:#2c3e50;--muted:#6c757d;--border:#dee2e6;
}
body{background:#fff;color:var(--text)}
.section-card{background:#fff}
.section-header{background:linear-gradient(135deg,var(--primary-color),var(--secondary-color))}
.nav-pills .nav-link{color:var(--text)}
.nav-pills .nav-link.active{color:#fff}
table.display thead th{background:linear-gradient(135deg,var(--primary-color),var(--secondary-color));color:#fff}
"""
            with open(css_target, "w", encoding="utf-8") as fw:
                fw.write(fallback)

    return template_path


# =====================================================
# 2) Core utilities
# =====================================================
class ParallelProcessor:
    @staticmethod
    def parallel_tree_distance_matrix(tree, terminals, n_jobs=None):
        if n_jobs is None:
            n_jobs = max(1, cpu_count() - 1)
        n = len(terminals)
        distance_matrix = np.zeros((n, n))

        def process_row(i, terminals, tree):
            row = np.zeros(len(terminals))
            a = terminals[i]
            for j in range(len(terminals)):
                if i == j: continue
                b = terminals[j]
                try: row[j] = tree.distance(str(a), str(b))
                except Exception: row[j] = np.nan
            return i, row

        with Pool(processes=n_jobs) as pool:
            func = partial(process_row, terminals=terminals, tree=tree)
            results = pool.map(func, range(n))
        for i, row in results:
            distance_matrix[i] = row
            for j in range(n):
                if i != j: distance_matrix[j, i] = distance_matrix[i, j]
        return distance_matrix

class PhylogeneticCore:
    @staticmethod
    def find_tree_file(preferred: str):
        candidates = [preferred, "tree.nwk", "tree.newick", "tree.newick.txt", "tree.nh", "tree.new"]
        for c in candidates:
            if os.path.isfile(c): return c
        raise FileNotFoundError(f"Tree file not found. Tried: {', '.join(candidates)}")

    @staticmethod
    def load_tree(tree_path):
        tp = PhylogeneticCore.find_tree_file(tree_path)
        return Phylo.read(tp, "newick")

    @staticmethod
    def tree_to_distance_matrix(tree, parallel=False, n_jobs=None):
        terminals = tree.get_terminals()
        if parallel:
            dm = ParallelProcessor.parallel_tree_distance_matrix(tree, terminals, n_jobs=n_jobs)
        else:
            n = len(terminals); dm = np.zeros((n, n))
            for i, a in enumerate(terminals):
                for j in range(i+1, n):
                    b = terminals[j]
                    dm[i, j] = dm[j, i] = tree.distance(str(a), str(b))
        return dm, terminals

    @staticmethod
    def umap_embed(dist_matrix, n_components=2, n_neighbors=15, min_dist=0.1, random_state=42):
        reducer = UMAP(n_components=n_components, metric='precomputed',
                       n_neighbors=n_neighbors, min_dist=min_dist, random_state=random_state)
        return reducer.fit_transform(dist_matrix)

    @staticmethod
    def detect_outliers(embeddings, contamination=0.05, n_estimators=200, random_state=42):
        iso = IsolationForest(contamination=contamination, n_estimators=n_estimators, random_state=random_state)
        mask = iso.fit_predict(embeddings) != -1
        return embeddings[mask], mask


class TreeAwareClustering:
    def __init__(self, tree, terminals):
        self.tree = tree; self.terminals = terminals

    def _auto_threshold(self, mode="max", factor=5.0):
        vals=[]
        for cl in self.tree.get_nonterminals():
            leaves = cl.get_terminals()
            if len(leaves) < 2: continue
            if mode == "max":
                m=0.0
                for i in range(len(leaves)):
                    for j in range(i+1, len(leaves)):
                        try: m=max(m, self.tree.distance(leaves[i], leaves[j]))
                        except: pass
                vals.append(m)
            else:
                s,c=0.0,0
                for i in range(len(leaves)):
                    for j in range(i+1, len(leaves)):
                        try: s+=self.tree.distance(leaves[i], leaves[j]); c+=1
                        except: pass
                vals.append(s if mode=="sum" else (s/c if c else 0.0))
        if not vals: return 0.1
        q75,q25=np.percentile(vals,[75,25]); iqr=q75-q25
        return np.median(vals) + factor*iqr

    def _check(self, idxs, dm, mode, thr):
        if len(idxs) <= 1: return True
        if mode == "max":
            m=0.0
            for i in range(len(idxs)):
                for j in range(i+1, len(idxs)):
                    m=max(m, dm[idxs[i], idxs[j]])
            return m <= thr
        s,c=0.0,0
        for i in range(len(idxs)):
            for j in range(i+1, len(idxs)):
                s+=dm[idxs[i], idxs[j]]; c+=1
        return (s<=thr) if mode=="sum" else ((s/c)<=thr if c else True)

    def cluster(self, dm, mode="max", threshold=None):
        if threshold is None: threshold=self._auto_threshold(mode)
        n=len(self.terminals); labs=np.arange(n)
        for node in self.tree.find_clades(order='postorder'):
            if node.is_terminal(): continue
            idxs=[]
            for leaf in node.get_terminals():
                for i,t in enumerate(self.terminals):
                    if str(t)==str(leaf): idxs.append(i); break
            if not idxs: continue
            if self._check(idxs, dm, mode, threshold):
                m=min(labs[idx] for idx in idxs)
                for idx in idxs: labs[idx]=m
        uniq={v:i+1 for i,v in enumerate(sorted(np.unique(labs)))}
        return np.array([uniq[v] for v in labs], dtype=int)


class EnsembleClustering:
    def __init__(self, trials=20, seed=42):
        self.trials=trials; self.seed=seed

    def _optimize_dbscan(self, X):
        def obj(trial):
            eps=trial.suggest_float('eps', 0.1, 2.0)
            ms =trial.suggest_int('min_samples', 3, 8)
            labels=DBSCAN(eps=eps, min_samples=ms).fit_predict(X)
            return -1.0 if len(set(labels))<=1 else silhouette_score(X, labels)
        study=optuna.create_study(direction='maximize')
        study.optimize(obj, n_trials=self.trials)
        return study.best_params

    def fit_best(self, X):
        best_s, best_labels = -1, None
        db=self._optimize_dbscan(X)
        for k in range(2,10):
            for mdl in (KMeans(n_clusters=k, random_state=self.seed),
                        GaussianMixture(n_components=k, random_state=self.seed)):
                try:
                    labs=mdl.fit_predict(X)
                    if len(set(labs))>1:
                        s=silhouette_score(X, labs)
                        if s>best_s: best_s, best_labels = s, (labs+1)
                except Exception: pass
        try:
            labs=DBSCAN(**db).fit_predict(X)
            if len(set(labs))>1:
                s=silhouette_score(X, labs)
                if s>best_s: best_s, best_labels = s, (labs+1)
        except Exception: pass
        return best_labels, best_s


class Evolution:
    @staticmethod
    def by_cluster(tree, labels, names):
        lab_u=np.unique(labels); rows=[]
        for lab in lab_u:
            ids=[names[i] for i in range(len(names)) if labels[i]==lab]
            if len(ids)<=1:
                rows.append([lab, ids, 0.0, 0.0, 0, len(ids)]); continue
            try:
                mrca=tree.common_ancestor(ids)
                pd_val=sum((cl.branch_length or 0) for cl in mrca.find_clades())
                d=[tree.distance(a,b) for i,a in enumerate(ids) for b in ids[i+1:]]
                mpd=float(np.mean(d)) if d else 0.0
                internal=sum(1 for cl in mrca.find_clades() if not cl.is_terminal())
                rows.append([lab, ids, pd_val, mpd, internal, len(mrca.get_terminals())])
            except Exception:
                rows.append([lab, ids, np.nan, np.nan, np.nan, np.nan])
        return pd.DataFrame(rows, columns=["Cluster_ID","Strains","PD","MeanPairwiseDist","InternalNodes","SubtreeTerminals"])

    @staticmethod
    def beta(tree, labels, names):
        labs=np.unique(labels); m=np.zeros((len(labs), len(labs)))
        by_lab={lab:[names[i] for i in range(len(names)) if labels[i]==lab] for lab in labs}
        for i,a in enumerate(labs):
            for j in range(i+1,len(labs)):
                b=labs[j]
                d=[tree.distance(x,y) for x in by_lab[a] for y in by_lab[b]]
                m[i,j]=m[j,i]=float(np.mean(d)) if d else 0.0
        return pd.DataFrame(m, index=labs, columns=labs)

    @staticmethod
    def rates(df_clusters):
        out=[]
        for _,r in df_clusters.iterrows():
            rate = (r["PD"]/r["InternalNodes"]) if r["InternalNodes"] and r["InternalNodes"]>0 else 0.0
            out.append({"Cluster_ID":r["Cluster_ID"], "EvolutionRate":rate})
        return pd.DataFrame(out)

    @staticmethod
    def signal(df_clusters, outdir):
        rec=[]
        for _,r in df_clusters.iterrows():
            n=len(r["Strains"]) if isinstance(r["Strains"], list) else 0
            s=(r["PD"]/n) if n else np.nan
            rec.append({"Cluster_ID":r["Cluster_ID"], "PhylogeneticSignal":round(s,2) if pd.notna(s) else np.nan})
        df=pd.DataFrame(rec); df.to_csv(os.path.join(outdir,"phylogenetic_signal.csv"), index=False)
        return df


# =====================================================
# 3) Data loading with robust prefixing
# =====================================================
class DataLoader:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    @staticmethod
    def _slug(s: str) -> str:
        return re.sub(r'[^a-z0-9]+', '_', str(s).strip().lower()).strip('_')

    def _load_and_prefix(self, path, prefix):
        df = pd.read_csv(path)
        # detect ID column
        id_candidates = [c for c in df.columns if self._slug(c) in ("strain_id","strain","id","isolate","sample")]
        if not id_candidates:
            raise RuntimeError(f"{os.path.basename(path)}: missing Strain_ID/ID column")
        id_col = id_candidates[0]
        df = df.rename(columns={id_col:"Strain_ID"})
        # normalize names & add prefix to all non-ID columns
        new_cols = {}
        for c in df.columns:
            if c == "Strain_ID":
                new_cols[c] = c
            else:
                sc = self._slug(c)
                if not sc.startswith(prefix):
                    sc = f"{prefix}{sc}"
                new_cols[c] = sc
        df = df.rename(columns=new_cols)
        # binarize everything except ID
        bin_cols = [c for c in df.columns if c != "Strain_ID"]
        df[bin_cols] = (df[bin_cols].fillna(0) > 0).astype(int)
        # normalize ID
        df["Strain_ID"] = df["Strain_ID"].astype(str).str.strip().str.lower()
        return df

    def load(self, clusters_csv):
        try:
            c = pd.read_csv(clusters_csv)
            c["Strain_ID"] = c["Strain_ID"].astype(str).str.strip().str.lower()

            mic = self._load_and_prefix(os.path.join(self.base_dir,"MIC.csv"), "mic_")
            amr = self._load_and_prefix(os.path.join(self.base_dir,"AMR_genes.csv"), "amr_")
            vir = self._load_and_prefix(os.path.join(self.base_dir,"Virulence3.csv"), "vir_")

            df = c.merge(mic, on="Strain_ID", how="left").merge(amr, on="Strain_ID", how="left").merge(vir, on="Strain_ID", how="left")
            feat_cols = [x for x in df.columns if x not in ("Strain_ID","Cluster")]
            df[feat_cols] = df[feat_cols].fillna(0).astype(int)
            return df
        except Exception as e:
            raise RuntimeError(f"Data load error: {e}. Expect MIC.csv, AMR_genes.csv, Virulence3.csv in {self.base_dir}")


# =====================================================
# 4) Visuals
# =====================================================
class Visuals:
    def __init__(self, outdir): self.outdir=outdir

    def cluster_distribution(self, df):
        g=df.groupby("Cluster").agg(Strain_Count=("Strain_ID","count")).reset_index()
        g["Percentage"]=(g["Strain_Count"]/len(df)*100).round(2)
        g.to_csv(os.path.join(self.outdir,"cluster_distribution.csv"), index=False)
        fig=px.bar(g, x="Cluster", y="Percentage", text="Strain_Count",
                   title="Cluster Distribution (%)", labels={"Percentage":"% of strains"})
        fig.update_traces(textposition="outside")
        return g, fig.to_html(full_html=False, include_plotlyjs=False)

    def tree_png_html(self, tree, labels, names):
        uniq=np.unique(labels); cmap=plt.cm.tab20(np.linspace(0,1,max(20,len(uniq))))
        color_by_name={}
        for i,lab in enumerate(uniq):
            for idx,nm in enumerate(names):
                if labels[idx]==lab: color_by_name[nm]=cmap[i]
        plt.figure(figsize=(14, max(8,len(names)*0.22))); ax=plt.gca()
        Phylo.draw(tree, axes=ax, do_show=False,
                   label_func=lambda x: x.name if (x.is_terminal() and x.name in color_by_name) else None)
        for txt in ax.texts:
            nm=txt.get_text().strip()
            if nm in color_by_name:
                txt.set_color(color_by_name[nm]); txt.set_fontweight("bold"); txt.set_fontsize(8.5)
        buf=BytesIO(); plt.tight_layout(); plt.savefig(buf, format="png", dpi=110, bbox_inches="tight"); plt.close()
        img64=base64.b64encode(buf.getvalue()).decode("utf-8")
        return f'<div class="text-center"><img class="img-fluid" src="data:image/png;base64,{img64}"/></div>'

    def umap_plotly(self, emb, labels):
        df=pd.DataFrame({"UMAP1":emb[:,0],"UMAP2":emb[:,1],"Cluster":labels})
        fig=px.scatter(df, x="UMAP1", y="UMAP2", color="Cluster", title="UMAP (clusters)")
        return fig.to_html(full_html=False, include_plotlyjs=False)

    def heatmap_plotly(self, df, title, zlabel):
        fig=go.Figure(data=go.Heatmap(z=df.values, x=df.columns, y=df.index, colorscale="Viridis",
                                      colorbar=dict(title=zlabel)))
        fig.update_layout(title=title, height=520)
        return fig.to_html(full_html=False, include_plotlyjs=False)


# =====================================================
# 5) Traits block
# =====================================================
class Traits:
    def __init__(self, outdir): self.outdir=outdir

    @staticmethod
    def _to_dt_html(df, table_id):
        """Render a pandas DF as a DataTables-ready HTML table - optimized."""
        if df is None or (hasattr(df, "empty") and df.empty):
            return "<div class='alert alert-info mb-0'>No data available.</div>"
        d = df.copy()

        # Numeric rounding
        num_cols = d.select_dtypes(include=[np.number]).columns
        for c in num_cols:
            if c.lower() != "strain_id":
                d[c] = d[c].round(3)

        d = d.fillna("")
        return d.to_html(
            table_id=table_id,
            classes="display table table-striped table-hover",
            index=False,
            escape=False,
            border=0
        )

    def frequencies(self, df, prefix):
        cols=[c for c in df.columns if c not in ["Strain_ID","Cluster"]]
        fr=(df.groupby("Cluster")[cols].mean()*100).round(2)
        fr.to_csv(os.path.join(self.outdir, f"trait_frequencies_{prefix}.csv"))
        return fr

    def tests(self, df, prefix, alpha=0.05):
        cols=[c for c in df.columns if c not in ["Strain_ID","Cluster"]]
        rows=[]
        for feat in cols:
            tab=pd.crosstab(df["Cluster"], df[feat])
            if tab.values.sum()==0: continue
            chi2,p,_,_=chi2_contingency(tab)
            rows.append({"Feature":feat,"Chi2":chi2,"p_value":p})
        res=pd.DataFrame(rows)
        if not res.empty:
            _, padj, _, _ = multipletests(res["p_value"], alpha=alpha, method="fdr_bh")
            res["p_adjusted"]=padj; res["significant"]=res["p_adjusted"]<alpha
        res.to_csv(os.path.join(self.outdir, f"statistical_tests_{prefix}.csv"), index=False)
        return res

    def rf_importance(self, df, prefix, n_bootstrap=100):
        cols=[c for c in df.columns if c not in ["Strain_ID","Cluster"]]
        X,y=df[cols].values, df["Cluster"].values
        scores=[]
        for _ in tqdm(range(n_bootstrap), desc=f"RF bootstrap {prefix}"):
            idx=np.random.choice(len(X), len(X), replace=True)
            rf=RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
            rf.fit(X[idx], y[idx]); scores.append(rf.feature_importances_)
        imp=pd.DataFrame({
            "Feature":cols,
            "Importance_Mean":np.mean(scores,axis=0),
            "Importance_Std": np.std(scores,axis=0),
            "Importance_Lower":np.percentile(scores,2.5,axis=0),
            "Importance_Upper":np.percentile(scores,97.5,axis=0)
        }).sort_values("Importance_Mean", ascending=False)
        imp.to_csv(os.path.join(self.outdir, f"feature_importance_{prefix}.csv"), index=False)
        return imp

    def log_odds(self, df):
        feats=[c for c in df.columns if c not in ["Strain_ID","Cluster"]]
        glob=[]; per=[]
        for f in feats:
            a=df[f].sum(); b=len(df)-a
            glob.append({"Feature":f,"Log_Odds_Ratio":round(np.log((a+0.5)/(b+0.5)),3)})
            for cl in sorted(df["Cluster"].unique()):
                sub=df[df["Cluster"]==cl]; ac=sub[f].sum(); bc=len(sub)-ac
                per.append({"Cluster":cl,"Feature":f,"Log_Odds_Ratio":round(np.log((ac+0.5)/(bc+0.5)),3)})
        g=pd.DataFrame(glob); p=pd.DataFrame(per)
        g.to_csv(os.path.join(self.outdir,"log_odds_global.csv"), index=False)
        p.to_csv(os.path.join(self.outdir,"log_odds_per_cluster.csv"), index=False)
        return g, p

    def assoc_rules(self, df, min_support=0.05, min_conf=0.7, max_features=50):
        feats=[c for c in df.columns if c not in ["Strain_ID","Cluster"]]
        top=df[feats].sum().sort_values(ascending=False).index[:max_features]
        basket=df[top].astype(bool)  # boolean DF to avoid mlxtend warning
        if basket.shape[1]==0:
            out=pd.DataFrame(columns=["Antecedent","Consequent","Support","Confidence","Lift"])
            out.to_csv(os.path.join(self.outdir,"association_rules.csv"), index=False); return out
        freq=apriori(basket, min_support=min_support, use_colnames=True, max_len=3)
        if freq.empty:
            out=pd.DataFrame(columns=["Antecedent","Consequent","Support","Confidence","Lift"])
            out.to_csv(os.path.join(self.outdir,"association_rules.csv"), index=False); return out
        rules=association_rules(freq, metric="confidence", min_threshold=min_conf)
        if rules.empty:
            out=pd.DataFrame(columns=["Antecedent","Consequent","Support","Confidence","Lift"])
        else:
            rules["Antecedent"]=rules["antecedents"].apply(lambda s:", ".join(sorted(list(s))))
            rules["Consequent"]=rules["consequents"].apply(lambda s:", ".join(sorted(list(s))))
            out=rules[["Antecedent","Consequent","support","confidence","lift"]].rename(
                columns={"support":"Support","confidence":"Confidence","lift":"Lift"}).round(4)
        out.to_csv(os.path.join(self.outdir,"association_rules.csv"), index=False)
        return out

    def shared_unique(self, df, thr=0.30):
        feats=[c for c in df.columns if c not in ["Strain_ID","Cluster"]]
        clusters=sorted(df["Cluster"].unique())
        shared=[]; unique=[]
        for f in feats:
            present=[]
            for cl in clusters:
                sub=df[df["Cluster"]==cl]
                if len(sub)==0: continue
                if sub[f].mean()>=thr: present.append(cl)
            if len(present)>1:
                shared.append({"Feature":f,"Clusters":", ".join(map(str,present)),
                               "NumClusters":len(present),"Count":int(df[f].sum()),
                               "Percent_in_All":round(df[f].mean()*100,2)})
            elif len(present)==1:
                cl=present[0]; sub=df[df["Cluster"]==cl]
                unique.append({"Cluster":cl,"Feature":f,"Count":int(sub[f].sum())})
        dfS=pd.DataFrame(shared).sort_values(["NumClusters","Count"], ascending=[False,False])
        dfU=pd.DataFrame(unique).sort_values(["Cluster","Count"], ascending=[True,False])
        dfS.to_csv(os.path.join(self.outdir,"shared_features.csv"), index=False)
        dfU.to_csv(os.path.join(self.outdir,"unique_features.csv"), index=False)
        return dfS, dfU

    def pairwise_fdr(self, df, alpha=0.05):
        feats=[c for c in df.columns if c not in ["Strain_ID","Cluster"]]
        cls=sorted(df["Cluster"].unique())
        res=[]; pvals=[]
        for f in [f for f in feats if df[f].sum()>0]:
            for i in range(len(cls)):
                for j in range(i+1,len(cls)):
                    A=df[df["Cluster"]==cls[i]][f]; B=df[df["Cluster"]==cls[j]][f]
                    tab=[[int(A.sum()), int(B.sum())],
                         [len(A)-int(A.sum()), len(B)-int(B.sum())]]
                    if (tab[0][0]+tab[0][1])==0 or (tab[1][0]+tab[1][1])==0: continue
                    _, p = fisher_exact(tab)
                    res.append({"Feature":f,"ClusterA":int(cls[i]),"ClusterB":int(cls[j]),"p_value_raw":float(p)})
                    pvals.append(p)
        if pvals:
            _, padj, _, _ = multipletests(pvals, alpha=alpha, method="fdr_bh")
            k=0
            for r in res:
                r["p_value_adj"]=float(padj[k]); r["significant"]=bool(padj[k]<alpha); k+=1
        out=pd.DataFrame(res).sort_values(["p_value_adj","Feature","ClusterA","ClusterB"])
        out.to_csv(os.path.join(self.outdir,"pairwise_fdr_post_hoc.csv"), index=False)
        return out


# =====================================================
# 6) MCA
# =====================================================
class MCA:
    def __init__(self, outdir): self.outdir=outdir
    def run(self, df):
        cols=[c for c in df.columns if c not in ["Strain_ID","Cluster"]]
        if not cols: return None, None, None
        X=df[cols].astype("category")
        m=prince.MCA(n_components=2, random_state=42).fit(X)
        rows=m.row_coordinates(X); rows.columns=["Component_1","Component_2"]; rows["Cluster"]=df["Cluster"].values
        colsC=m.column_coordinates(X); colsC.columns=["Component_1","Component_2"]; colsC["Feature_Type"]="Other"
        for f in colsC.index:
            fl=f.lower()
            if fl.startswith("mic_"): colsC.loc[f,"Feature_Type"]="MIC"
            elif fl.startswith("amr_"): colsC.loc[f,"Feature_Type"]="AMR"
            elif fl.startswith("vir_"): colsC.loc[f,"Feature_Type"]="Virulence"
        eig=m.eigenvalues_; total=sum(eig)
        summ=pd.DataFrame({
            "Component":range(1,len(eig)+1),
            "Eigenvalue":[round(x,4) for x in eig],
            "Explained_Inertia":[round(x/total,4) for x in eig],
            "Cumulative_Explained_Inertia":[round(sum(eig[:i+1])/total,4) for i in range(len(eig))]
        })
        rows.to_csv(os.path.join(self.outdir,"mca_row_coordinates.csv"), index=False)
        colsC.to_csv(os.path.join(self.outdir,"mca_column_coordinates.csv"))
        summ.to_csv(os.path.join(self.outdir,"mca_summary.csv"), index=False)
        return rows, colsC, summ


# =====================================================
# 7) Report generator (single writer)
# =====================================================
class Report:
    def __init__(self, outdir, base_dir="."):
        self.outdir=outdir; self.base_dir=base_dir
        ensure_template_and_css(outdir)
        self.env=jinja2.Environment(loader=jinja2.FileSystemLoader("templates"),
                                    autoescape=jinja2.select_autoescape(['html','xml']))

    @staticmethod
    def datatable(df, table_id):
        """Render a pandas DF as a DataTables-ready HTML table - OPTIMIZED."""
        if df is None or (hasattr(df,"empty") and df.empty):
            return "<div class='alert alert-info mb-0'>No data available.</div>"
        d=df.copy()
        num_cols=d.select_dtypes(include=[np.number]).columns
        for c in num_cols:
            if c.lower()!="strain_id": d[c]=d[c].round(3)
        d=d.fillna("")
        return d.to_html(table_id=table_id, classes="display table table-striped table-hover", index=False, escape=False)

    def scan_downloads(self):
        rows=[]
        for f in sorted(os.listdir(self.outdir)):
            p=os.path.join(self.outdir,f)
            if not os.path.isfile(p): continue
            size=os.path.getsize(p)/1024.0
            if f.lower().endswith((".csv",".txt",".tsv")) and size<5000:
                with open(p,"rb") as fh:
                    b64=base64.b64encode(fh.read()).decode("utf-8")
                link=f"<a class='btn btn-sm btn-primary' download='{f}' href='data:text/plain;base64,{b64}'>Download</a>"
            else:
                link="<span class='btn btn-sm btn-secondary disabled'>No direct link</span>"
            rows.append({"File":f,"Size_KB":round(size,2),"Action":link})
        df=pd.DataFrame(rows, columns=["File","Size_KB","Action"])
        return Report.datatable(df, "tbl-downloads")

    def create(self, payload, config, html_name="phylogenetic_report.html"):
        tpl=self.env.get_template("report_template.html")
        context={
            "title":"StrepSuisPhyloCluster: Integrative Phylogenetic Clustering Tool and Binary Trait Profiling of Antimicrobial Resistance and Virulence in Streptococcus suis",
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "config": vars(config),
            "results": payload
        }
        html=tpl.render(**context)
        out=os.path.join(self.outdir, html_name)
        with open(out,"w",encoding="utf-8") as f: f.write(html)
        print(f"HTML report saved to: {out}")
        return out


# =====================================================
# 8) Pipeline
# =====================================================
class Config:
    def __init__(self, **kw):
        self.base_dir=kw.get("base_dir",".")
        self.output_folder=kw.get("output_folder","phylogenetic_clustering_results_fixed")
        self.tree_file=kw.get("tree_file","tree.nwk")
        self.umap_components=kw.get("umap_components",2)
        self.umap_neighbors=kw.get("umap_neighbors",15)
        self.umap_min_dist=kw.get("umap_min_dist",0.1)
        self.outlier_contamination=kw.get("outlier_contamination",0.05)
        self.outlier_estimators=kw.get("outlier_estimators",200)
        self.parallel_tree=kw.get("parallel_tree",False)
        self.parallel_jobs=kw.get("parallel_jobs",1)

class Pipeline:
    def __init__(self, cfg: Config):
        self.cfg=cfg
        self.outdir=os.path.join(cfg.base_dir, cfg.output_folder)
        os.makedirs(self.outdir, exist_ok=True)
        self.core=PhylogeneticCore()
        self.tr=Traits(self.outdir)
        self.vis=Visuals(self.outdir)
        self.mca=MCA(self.outdir)

    @staticmethod
    def _methodology_html():
        return """
        <div class="method-box">
          <h6 class="mb-2"><i class="fa-solid fa-tree me-2"></i>Tree-aware Clustering</h6>
          <p>Pairwise patristic distances from the Newick tree are computed. For each internal clade we test
             intra-clade distances against a robust threshold (median + IQR factor) under <em>max</em>, <em>avg</em>, and
             <em>sum</em> criteria. The best solution is selected by the silhouette score on the precomputed matrix.</p>
        </div>
        <div class="method-box">
          <h6 class="mb-2"><i class="fa-solid fa-diagram-project me-2"></i>Ensemble Fallback</h6>
          <p>If no valid tree-aware clustering is found, UMAP embeddings are clustered using an ensemble
             (KMeans, Gaussian Mixture, and DBSCAN with Optuna search). We keep the labeling with the highest silhouette.</p>
        </div>
        <div class="method-box">
          <h6 class="mb-2"><i class="fa-solid fa-dna me-2"></i>Evolutionary Metrics</h6>
          <ul class="mb-0">
            <li><strong>Phylogenetic Diversity (PD):</strong> sum of branch lengths within cluster MRCA.</li>
            <li><strong>Mean Pairwise Distance (MPD):</strong> average patristic distance among strains in a cluster.</li>
            <li><strong>Beta Diversity:</strong> mean inter-cluster patristic distances.</li>
            <li><strong>Evolution Rate (proxy):</strong> PD / #internal nodes in cluster MRCA.</li>
            <li><strong>Phylogenetic Signal:</strong> PD normalized by cluster size.</li>
          </ul>
        </div>
        <div class="method-box">
          <h6 class="mb-2"><i class="fa-solid fa-flask me-2"></i>Trait Analysis & Hypothesis Testing</h6>
          <p>Binary traits are merged (MIC / AMR genes / Virulence). We report per-cluster frequencies and test cluster–trait
             independence via chi-square; multiple tests are corrected using Benjamini–Hochberg FDR (α=0.05).
             Pairwise cluster comparisons for each feature use Fisher's Exact test with FDR correction.</p>
        </div>
        <div class="method-box">
          <h6 class="mb-2"><i class="fa-solid fa-seedling me-2"></i>Effect Size & Model-Based Importance</h6>
          <p>Global and per-cluster log-odds ratios quantify association strength. Random Forest classifiers (bootstrap)
             yield feature importance distributions with 95% percentile intervals.</p>
        </div>
        <div class="method-box">
          <h6 class="mb-2"><i class="fa-solid fa-layer-group me-2"></i>Association Rules</h6>
          <p>Frequent itemsets (apriori) from booleanized traits (top features by prevalence) followed by confidence/lift
             rules support multi-trait pattern discovery.</p>
        </div>
        <div class="method-box">
          <h6 class="mb-2"><i class="fa-solid fa-chart-scatter me-2"></i>MCA</h6>
          <p>Multiple Correspondence Analysis (prince) on the categorical trait matrix; row (strain) and column (feature) coordinates
             summarize joint structure. We report explained inertia per component.</p>
        </div>
        """

    def run(self):
        print("=== Starting Complete Phylogenetic Analysis ===")
        print("Start:", pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))

        # Step 1: phylogeny & clustering
        print("\n=== Step 1: Phylogenetic Clustering ===")
        tree_path=os.path.join(self.cfg.base_dir, self.cfg.tree_file)
        tree=self.core.load_tree(tree_path)
        dm, terms=self.core.tree_to_distance_matrix(tree, parallel=self.cfg.parallel_tree, n_jobs=self.cfg.parallel_jobs)
        names=[str(t).strip() for t in terms]
        emb=self.core.umap_embed(dm, self.cfg.umap_components, self.cfg.umap_neighbors, self.cfg.umap_min_dist, 42)

        tac=TreeAwareClustering(tree, terms)
        best_labels=None; best_s=-1; best_method="TreeCluster"
        for mode in ["max","avg","sum"]:
            try:
                labs=tac.cluster(dm, mode=mode)
                if len(np.unique(labs))>1:
                    s=silhouette_score(dm, labs, metric="precomputed")
                    if s>best_s: best_s, best_labels, best_method = s, labs, f"TreeCluster-{mode}"
            except Exception: pass
        if best_labels is None:
            clean, mask=self.core.detect_outliers(emb, self.cfg.outlier_contamination, self.cfg.outlier_estimators, 42)
            ens=EnsembleClustering(trials=20, seed=42)
            lbls, s=ens.fit_best(clean)
            if lbls is None: raise RuntimeError("Clustering failed")
            uniq=np.unique(lbls); centers=np.vstack([clean[lbls==u].mean(axis=0) for u in uniq])
            full=np.zeros(len(emb), dtype=int); full[mask]=lbls
            if (~mask).any():
                D=cdist(emb[~mask], centers); nearest=uniq[D.argmin(axis=1)]
                full[~mask]=nearest
            best_labels, best_s, best_method = full, s, "Ensemble"
        print(f"Best clustering: {best_method} | silhouette={best_s:.3f}")

        # Save clusters CSV (Strain_ID + Cluster)
        os.makedirs(self.outdir, exist_ok=True)
        clusters_csv=os.path.join(self.outdir,"phylogenetic_clusters.csv")
        pd.DataFrame({"Strain_ID":names, "Cluster":best_labels}).to_csv(clusters_csv, index=False)

        # Visuals
        tree_html=self.vis.tree_png_html(tree, best_labels, names)
        umap_html=self.vis.umap_plotly(emb, best_labels)

        # Step 2: Evolutionary
        print("\n=== Step 2: Evolutionary Analysis ===")
        evo_df=Evolution.by_cluster(tree, best_labels, names)
        evo_df.to_csv(os.path.join(self.outdir,"evolutionary_cluster_analysis.csv"), index=False)
        beta_df=Evolution.beta(tree, best_labels, names)
        beta_df.to_csv(os.path.join(self.outdir,"phylogenetic_beta_diversity.csv"))
        rates_df=Evolution.rates(evo_df); rates_df.to_csv(os.path.join(self.outdir,"evolution_rates.csv"), index=False)
        signal_df=Evolution.signal(evo_df, self.outdir)

        # Step 3: Trait Analysis
        print("\n=== Step 3: Trait Analysis ===")
        merged=DataLoader(self.cfg.base_dir).load(clusters_csv)

        mic_cols = [c for c in merged.columns if c.lower().startswith("mic_")]
        amr_cols = [c for c in merged.columns if c.lower().startswith("amr_")]
        vir_cols = [c for c in merged.columns if c.lower().startswith("vir_")]
        for cols in (mic_cols, amr_cols, vir_cols):
            if cols: merged[cols] = (merged[cols] > 0).astype(int)

        blocks=[]; all_feat_imps=[]

        def _do_block(cat_name, cols, short):
            sub = merged[["Strain_ID","Cluster"]+cols].copy()
            fr  = self.tr.frequencies(sub, short)
            tst = self.tr.tests(sub, short)
            imp = self.tr.rf_importance(sub, short, n_bootstrap=50)  # fewer iters for speed; summaries later
            imp.insert(0,"Category",cat_name)
            all_feat_imps.append(imp)

            # Build HTML blocks
            blocks.append(f"<h5 class='mt-2'>{cat_name} Frequencies</h5>" + Traits._to_dt_html(fr.reset_index(), f"tbl-fr-{short}"))
            blocks.append(f"<h6 class='mt-3'>Chi-square + FDR</h6>" + Traits._to_dt_html(tst, f"tbl-test-{short}"))
            blocks.append(f"<h6 class='mt-3'>RF Importance (bootstrap)</h6>" + Traits._to_dt_html(imp.head(50), f"tbl-imp-{short}"))

        if mic_cols: _do_block("MIC", mic_cols, "mic")
        if amr_cols: _do_block("AMR", amr_cols, "amr")
        if vir_cols: _do_block("Virulence", vir_cols, "vir")

        # Fallback: if none of the prefixed groups exist, show ALL traits together
        if not blocks:
            all_cols = [c for c in merged.columns if c not in ("Strain_ID","Cluster")]
            if all_cols:
                sub = merged[["Strain_ID","Cluster"]+all_cols].copy()
                sub[all_cols] = (sub[all_cols] > 0).astype(int)
                fr  = self.tr.frequencies(sub, "all")
                tst = self.tr.tests(sub, "all")
                imp = self.tr.rf_importance(sub, "all", n_bootstrap=50)
                imp.insert(0,"Category","All")
                all_feat_imps.append(imp)

                blocks.append("<h5 class='mt-2'>All Traits - Frequencies</h5>" + Traits._to_dt_html(fr.reset_index(), "tbl-fr-all"))
                blocks.append("<h6 class='mt-3'>Chi-square + FDR</h6>" + Traits._to_dt_html(tst, "tbl-test-all"))
                blocks.append("<h6 class='mt-3'>RF Importance (bootstrap)</h6>" + Traits._to_dt_html(imp.head(50), "tbl-imp-all"))

        # Combine blocks into trait_html
        trait_html = "\n".join(blocks) if blocks else "<div class='alert alert-warning'>No trait data available</div>"

        # Cluster distribution (table + plot)
        dist_df, dist_plot_html = self.vis.cluster_distribution(merged)

        # Log-odds
        g_log, c_log = self.tr.log_odds(merged)

        # Association rules
        rules_df=self.tr.assoc_rules(merged)

        # Shared/unique
        shared_df, unique_df = self.tr.shared_unique(merged, thr=0.30)

        # Pairwise FDR
        fdr_df=self.tr.pairwise_fdr(merged)

        # Step 4: MCA
        print("\n=== Step 4: MCA Analysis ===")
        mca_rows, mca_cols, mca_sum = self.mca.run(merged)

        # Assemble report payload
        rep=Report(self.outdir, base_dir=self.cfg.base_dir)
        payload={}

        # --- PART I: FOUNDATIONAL ---
        payload["summary_stats"]=Report.datatable(
            dist_df.rename(columns={"Strain_Count":"Count","Percentage":"%"}), "tbl-summary")
        payload["methodology"]=self._methodology_html()

        # --- PART II: PHYLOGENETIC STRUCTURE ---
        payload["tree_plot"]=tree_html
        payload["tree_stats"]=Report.datatable(evo_df, "tbl-tree-stats")

        payload["umap_plot"]=umap_html
        payload["cluster_distribution"]=dist_plot_html
        payload["cluster_validation"]=Report.datatable(
            pd.DataFrame({"Best_Method":[best_method],
                          "Silhouette":[round(best_s,3)],
                          "Num_Clusters":[len(np.unique(best_labels))]}),
            "tbl-valid")

        payload["evolutionary_metrics"]=Report.datatable(evo_df, "tbl-evo")
        payload["beta_diversity"]=self.vis.heatmap_plotly(beta_df, "Beta Diversity (Mean Inter-Cluster Distance)", "Distance")
        payload["evolution_rates"]=px.bar(rates_df, x="Cluster_ID", y="EvolutionRate", title="Evolution Rates").to_html(False, False)
        payload["phylogenetic_signal"]=Report.datatable(signal_df, "tbl-signal")

        # --- PART III: TRAIT PROFILING ---
        payload["trait_analysis"]=trait_html
        payload["global_log_odds"]=Report.datatable(g_log, "tbl-log-global")
        payload["cluster_log_odds"]=Report.datatable(c_log, "tbl-log-cluster")
        payload["association_rules"]=Report.datatable(rules_df, "tbl-assoc")
        payload["shared_features"]=Report.datatable(shared_df, "tbl-shared")
        payload["unique_features"]=Report.datatable(unique_df, "tbl-unique")
        payload["pairwise_fdr"]=Report.datatable(fdr_df, "tbl-fdr")

        # --- PART IV: ADVANCED ANALYSES ---
        if mca_rows is not None and mca_sum is not None:
            fig_row=px.scatter(mca_rows, x="Component_1", y="Component_2", color="Cluster",
                               title="MCA Row Points (Strains)")
            payload["mca_row_plot"]=fig_row.to_html(False, False)
            dfc=mca_cols.reset_index().rename(columns={"index":"Feature"})
            fig_col=px.scatter(dfc, x="Component_1", y="Component_2", color="Feature_Type",
                               hover_name="Feature", title="MCA Column Points (Features)")
            payload["mca_column_plot"]=fig_col.to_html(False, False)
            payload["mca_summary"]=Report.datatable(mca_sum, "tbl-mca-sum")
        else:
            payload["mca_row_plot"]="<div class='alert alert-secondary mb-0'>MCA not available.</div>"
            payload["mca_column_plot"]="<div class='alert alert-secondary mb-0'>MCA not available.</div>"
            payload["mca_summary"]="<div class='alert alert-secondary mb-0'>MCA not available.</div>"

        # Bootstrap summary table (top features across categories)
        comb_imp=pd.concat(all_feat_imps, ignore_index=True) if all_feat_imps else pd.DataFrame()
        comb_imp=comb_imp.sort_values("Importance_Mean", ascending=False).head(50) if not comb_imp.empty else comb_imp
        payload["bootstrap_feature_importance"]=Report.datatable(comb_imp, "tbl-boot-feat") if not comb_imp.empty else ""
        payload["bootstrap_log_odds"]=Report.datatable(pd.DataFrame(), "tbl-boot-log")  # placeholder

        # --- PART V: RESOURCES ---
        payload["download_section"]=rep.scan_downloads()

        # Create report
        path=rep.create(payload, self.cfg, html_name="phylogenetic_report.html")

        print("\n=== Analysis completed successfully! ===")
        print("End:", pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))
        return path


# =====================================================
# 9) Run (adjust paths if needed)
# =====================================================
if __name__ == "__main__":
    cfg=Config(
        base_dir=".",                      # CSVs + tree file live here
        output_folder="phylogenetic_clustering_results_fixed-001",
        tree_file="tree.nwk",              # auto-tries common alternatives if missing
        umap_components=2,
        umap_neighbors=15,
        umap_min_dist=0.1,
        outlier_contamination=0.05,
        outlier_estimators=200,
        parallel_tree=False,
        parallel_jobs=1
    )
    Pipeline(cfg).run()
