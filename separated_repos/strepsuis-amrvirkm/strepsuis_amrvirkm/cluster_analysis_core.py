###########################################
# Comprehensive Sample Code - Final (EN)
# Single HTML Report, With Additional Bootstrap CIs
# Certain CSV Excluded from Final Report
###########################################

# -----------------------------------------
# 1. Required Packages
# -----------------------------------------
# Run: pip install kmodes prince ydata-profiling joblib numba tqdm psutil statsmodels jinja2 plotly openpyxl

import gc
import logging
import multiprocessing
import os

# -----------------------------------------
# 2. Imports
# -----------------------------------------
import sys
import traceback

# Jinja2 for HTML templating
import jinja2
import numpy as np
import pandas as pd

# Visualization
import plotly.express as px
import psutil

# Excel report generation
try:
    from .excel_report_utils import ExcelReportGenerator, sanitize_sheet_name
except ImportError:
    from strepsuis_amrvirkm.excel_report_utils import ExcelReportGenerator, sanitize_sheet_name
from joblib import Parallel, delayed

# K-Modes
from kmodes.kmodes import KModes
from numba import jit
from prince import MCA
from scipy.stats import chi2_contingency, fisher_exact
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score, silhouette_score
from sklearn.preprocessing import StandardScaler

# Statistics
from sklearn.utils import resample
from statsmodels.stats.multitest import multipletests
from tqdm import tqdm

# Data Profiling (ydata-profiling)

# -----------------------------------------
# 3. Logging & Global Configuration
# -----------------------------------------
logging.basicConfig(
    filename="analysis.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

sys.setrecursionlimit(10000)
gc.enable()
gc.set_threshold(100, 5, 5)
np.seterr(all="ignore")
np.random.seed(42)

output_folder = "clustering_analysis_results6"
os.makedirs(output_folder, exist_ok=True)


def print_memory_usage():
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / (1024**2)
    logging.info(f"Memory Usage: {mem:.2f} MB")
    print(f"Memory Usage: {mem:.2f} MB")


# -----------------------------------------
# 4. Retry Decorator
# -----------------------------------------
def retry_operation(func, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            logging.error(f"Attempt {attempt+1} failed: {str(e)}")
            print(f"Attempt {attempt+1} failed: {str(e)}")
            if attempt == max_attempts - 1:
                raise
    return None


# -----------------------------------------
# 5. Binary Data Validation
# -----------------------------------------
def validate_binary_data(df):
    if not ((df.values == 0) | (df.values == 1)).all():
        raise ValueError("Data is not strictly 0/1 binary.")


# -----------------------------------------
# 6. K-Modes Clustering + Silhouette
# -----------------------------------------
def determine_optimal_clusters_sqrt(data):
    max_clusters = max(2, int(np.sqrt(len(data))))
    silhouette_scores = []
    for k in range(2, max_clusters + 1):
        km = KModes(n_clusters=k, init="Huang", n_init=5, random_state=42)
        clusters = km.fit_predict(data)
        try:
            score = silhouette_score(data, clusters)
            silhouette_scores.append(score)
            print(f"For n_clusters={k}, silhouette_score={score:.2f}")
        except ValueError as e:
            silhouette_scores.append(-1)
            print(f"Silhouette not computed for k={k}: {e}")
    if silhouette_scores:
        best_k = silhouette_scores.index(max(silhouette_scores)) + 2
        print(f"Optimal k = {best_k}")
        return best_k
    else:
        raise ValueError("No valid silhouette score found.")


def perform_kmodes(data, n_clusters):
    km = KModes(n_clusters=n_clusters, init="Huang", n_init=5, random_state=42)
    clusters = km.fit_predict(data)
    return km, clusters + 1  # shift to 1-based cluster labels


def extract_characteristic_patterns(model, data):
    patterns = {}
    for i in range(model.n_clusters):
        cluster_data = data[model.labels_ == i]
        if cluster_data.empty:
            continue
        mode_row = cluster_data.mode().iloc[0]
        sig_feats = mode_row[mode_row > 0.5]
        patterns[i + 1] = sig_feats
    return patterns


# -----------------------------------------
# 7. Bootstrapping + CI
# -----------------------------------------
@jit(nopython=True)
def _numba_bootstrap(total_samples, p, num_bootstrap):
    results = np.zeros(num_bootstrap)
    for i in range(num_bootstrap):
        sample = np.random.binomial(total_samples, p)
        results[i] = sample / total_samples * 100
    return results


def bootstrap_confidence_interval(
    percentage, count, total_samples, num_bootstrap=500, confidence_level=0.95
):
    if total_samples == 0:
        return (np.nan, np.nan)
    p = (count + 0.5) / (total_samples + 1)
    boots = _numba_bootstrap(total_samples, p, num_bootstrap)
    ci_low = np.percentile(boots, ((1 - confidence_level) / 2) * 100)
    ci_high = np.percentile(boots, (1 - (1 - confidence_level) / 2) * 100)
    return round(ci_low, 2), round(ci_high, 2)


def patterns_to_dataframe(patterns, pattern_type, data, clusters):
    out_list = []
    for cls, feats in patterns.items():
        c_data = data[clusters == cls]
        total = len(c_data)
        counts = c_data[feats.index].sum()
        perc = (counts / total * 100).round(2)

        ci_vals = [
            bootstrap_confidence_interval(pp, cc, total, num_bootstrap=500)
            for pp, cc in zip(perc, counts)
        ]

        if ci_vals:
            ci_low, ci_high = zip(*ci_vals)
            details = []
            for f, c, p, ci_l, ci_h in zip(feats.index, counts, perc, ci_low, ci_high):
                details.append(f"{f} ({c}/{total}, {p}%, CI:{ci_l}-{ci_h}%)")
        else:
            details = ["No significant features"]

        out_list.append(
            {
                "Cluster": cls,
                "Size": total,
                "Characteristic_Pattern": "; ".join(details),
                "Type": pattern_type,
            }
        )
    return pd.DataFrame(out_list)


# -----------------------------------------
# 8. Pairwise FDR Post-Hoc
# -----------------------------------------


def pairwise_fdr_post_hoc(data, clusters, category):
    unique_cls = np.unique(clusters)
    if len(unique_cls) < 2:
        return pd.DataFrame()
    results = []
    for feat in data.columns:
        for i in range(len(unique_cls)):
            for j in range(i + 1, len(unique_cls)):
                cl_a = unique_cls[i]
                cl_b = unique_cls[j]
                mask_a = clusters == cl_a
                mask_b = clusters == cl_b
                a1 = data[feat][mask_a].sum()
                a0 = mask_a.sum() - a1
                b1 = data[feat][mask_b].sum()
                b0 = mask_b.sum() - b1
                cont = np.array([[a1, a0], [b1, b0]])
                if cont.sum() == 0:
                    p = np.nan
                    chi2_val = np.nan
                else:
                    try:
                        if (cont < 5).any() and cont.shape == (2, 2):
                            _, p = fisher_exact(cont)
                            chi2_val = np.nan
                        else:
                            chi2_val, p, _, _ = chi2_contingency(cont)
                    except (ValueError, TypeError):
                        p = np.nan
                        chi2_val = np.nan
                results.append(
                    {
                        "Feature": feat,
                        "ClusterA": cl_a,
                        "ClusterB": cl_b,
                        "Chi2": round(chi2_val, 2) if not np.isnan(chi2_val) else np.nan,
                        "P_Value": round(p, 2) if not np.isnan(p) else np.nan,
                    }
                )
    df_res = pd.DataFrame(results).dropna(subset=["P_Value"])
    if df_res.empty:
        return df_res
    pvals = df_res["P_Value"].values
    rej, corr, _, _ = multipletests(pvals, alpha=0.05, method="fdr_bh")
    df_res["Adjusted_P"] = corr
    df_res["FDR_Rejected"] = rej
    df_res.to_csv(
        os.path.join(output_folder, f"{category.lower()}_fdr_post_hoc_results.csv"), index=False
    )
    return df_res


# -----------------------------------------
# 9. Phi Correlation
# -----------------------------------------
def compute_phi(x, y):
    a = np.sum((x == 1) & (y == 1))
    b = np.sum((x == 1) & (y == 0))
    c = np.sum((x == 0) & (y == 1))
    d = np.sum((x == 0) & (y == 0))
    denom = (a + b) * (c + d) * (a + c) * (b + d)
    if denom == 0:
        return np.nan
    return (a * d - b * c) / np.sqrt(denom)


def phi_correlation_matrix(df):
    cols = df.columns
    n = len(cols)
    corr = pd.DataFrame(np.zeros((n, n)), index=cols, columns=cols)
    for i in range(n):
        for j in range(i, n):
            val = compute_phi(df[cols[i]], df[cols[j]])
            corr.iloc[i, j] = round(val, 2) if not np.isnan(val) else np.nan
            corr.iloc[j, i] = round(val, 2) if not np.isnan(val) else np.nan
    return corr


def analyze_virulence_correlations(data, clusters):
    correlations = pd.DataFrame()
    for cluster in np.unique(clusters):
        cluster_data = data[clusters == cluster]
        if cluster_data.empty:
            continue
        corr_matrix = phi_correlation_matrix(cluster_data).reset_index().melt(id_vars="index")
        corr_matrix.columns = ["Row", "Column", "Phi"]
        corr_matrix["Cluster"] = cluster
        correlations = pd.concat([correlations, corr_matrix], ignore_index=True)
    return correlations


def cluster_correlation_analysis(data, clusters, category):
    if category.lower() == "virulence":
        corr_df = analyze_virulence_correlations(data, clusters)
    else:
        out = []
        for cl in np.unique(clusters):
            c_data = data[clusters == cl]
            if not c_data.empty:
                phi_mat = phi_correlation_matrix(c_data).round(2)
                for r in phi_mat.index:
                    for c in phi_mat.columns:
                        out.append({"Cluster": cl, "Row": r, "Column": c, "Phi": phi_mat.loc[r, c]})
        if out:
            corr_df = pd.DataFrame(out).dropna(subset=["Phi"])
        else:
            corr_df = pd.DataFrame()
    corr_df.to_csv(
        os.path.join(output_folder, f"{category.lower()}_cluster_correlation.csv"), index=False
    )
    return corr_df


# -----------------------------------------
# 10. Logistic Regression + Bootstrap
# -----------------------------------------
def stratified_bootstrap(X, y):
    lbls = np.unique(y)
    Xb_list, yb_list = [], []
    for lab in lbls:
        X_lab = X[y == lab]
        y_lab = y[y == lab]
        X_res, y_res = resample(X_lab, y_lab, replace=True, n_samples=len(X_lab))
        Xb_list.append(X_res)
        yb_list.append(y_res)
    return np.vstack(Xb_list), np.concatenate(yb_list)


def logistic_regression_feature_selection(data, clusters, with_ci=True, n_bootstrap=200):
    sc = StandardScaler()
    Xs = sc.fit_transform(data)
    y = clusters
    model = LogisticRegression(penalty="l1", solver="saga", max_iter=10000, random_state=42)
    model.fit(Xs, y)
    feats = data.columns
    n_classes = model.coef_.shape[0]

    base_coef = model.coef_
    coef_df = pd.DataFrame(base_coef, columns=feats)
    coef_df["Cluster"] = np.arange(1, n_classes + 1)
    coef_long = coef_df.melt(id_vars=["Cluster"], var_name="Feature", value_name="Coefficient")
    coef_long["Abs_Coefficient"] = coef_long["Coefficient"].abs()
    coef_long.sort_values(["Cluster", "Abs_Coefficient"], ascending=[True, False], inplace=True)

    if not with_ci:
        return coef_long.round(2)

    def single_boot(_):
        Xb, yb = stratified_bootstrap(Xs, y)
        mb = LogisticRegression(penalty="l1", solver="saga", max_iter=10000, random_state=None)
        mb.fit(Xb, yb)
        return mb.coef_

    num_cores = multiprocessing.cpu_count()
    all_coefs = Parallel(n_jobs=num_cores)(delayed(single_boot)(i) for i in range(n_bootstrap))
    boot_coefs = []
    for c in all_coefs:
        if c.shape[0] == n_classes:
            boot_coefs.append(c)
    if len(boot_coefs) == 0:
        return coef_long.round(2)

    boot_coefs = np.array(boot_coefs)
    ci_list = []
    for class_idx in range(n_classes):
        class_c = boot_coefs[:, class_idx, :]
        ci_low = np.percentile(class_c, 2.5, axis=0)
        ci_high = np.percentile(class_c, 97.5, axis=0)
        tmp = pd.DataFrame(
            {
                "Feature": feats,
                "Cluster": class_idx + 1,
                "CI_low": ci_low.round(2),
                "CI_high": ci_high.round(2),
            }
        )
        ci_list.append(tmp)
    ci_df = pd.concat(ci_list, ignore_index=True)
    coef_merged = pd.merge(coef_long, ci_df, on=["Cluster", "Feature"], how="left")
    coef_merged.sort_values(["Cluster", "Abs_Coefficient"], ascending=[True, False], inplace=True)
    return coef_merged.round(2)


# -----------------------------------------
# 11. Modified Standard Cluster Stats (with Bootstrap CI)
# -----------------------------------------
def calculate_cluster_stats(clusters):
    total = len(clusters)
    c_counts = pd.Series(clusters).value_counts().sort_index()
    c_perc = (c_counts / total * 100).round(2)
    stats_df = pd.DataFrame({"Count": c_counts, "Percentage": c_perc})

    ci_list = []
    for idx, row in stats_df.iterrows():
        cluster_count = row["Count"]
        cluster_perc = row["Percentage"]
        low_ci, high_ci = bootstrap_confidence_interval(cluster_perc, cluster_count, total)
        ci_list.append((low_ci, high_ci))
    stats_df["CI_low"], stats_df["CI_high"] = zip(*ci_list)

    return stats_df


def validate_clusters(data, clusters):
    try:
        ch = calinski_harabasz_score(data, clusters)
        ch = round(ch, 2)
    except ValueError:
        ch = np.nan
    try:
        db = davies_bouldin_score(data, clusters)
        db = round(db, 2)
    except ValueError:
        db = np.nan
    return ch, db


# -----------------------------------------
# 12. Chi-square Analysis
# -----------------------------------------
def chi_square_analysis(data, clusters):
    results_global = []
    for feat in data.columns:
        cont = pd.crosstab(clusters, data[feat])
        expected = np.outer(cont.sum(axis=1), cont.sum(axis=0)) / cont.values.sum()
        if (expected < 5).any() or cont.values.sum() == 0:
            try:
                if cont.shape == (2, 2):
                    _, p = fisher_exact(cont)
                    chi2 = np.nan
                else:
                    chi2, p, _, _ = chi2_contingency(cont)
            except (ValueError, TypeError):
                chi2, p = np.nan, np.nan
        else:
            try:
                chi2, p, _, _ = chi2_contingency(cont)
            except (ValueError, TypeError):
                chi2, p = np.nan, np.nan

        results_global.append(
            {
                "Feature": feat,
                "Chi2": round(chi2, 2) if not np.isnan(chi2) else np.nan,
                "P_Value": round(p, 2) if not np.isnan(p) else np.nan,
            }
        )

    dfg = pd.DataFrame(results_global).dropna(subset=["P_Value"])
    if not dfg.empty:
        pvals = dfg["P_Value"].values
        rej, corr, _, _ = multipletests(pvals, alpha=0.05, method="fdr_bh")
        dfg["Adjusted_P"] = corr
        dfg["FDR_Rejected"] = rej

    results_cluster = []
    for cl in np.unique(clusters):
        c_labels = (clusters == cl).astype(int)
        for feat in data.columns:
            cont = pd.crosstab(c_labels, data[feat])
            if cont.shape != (2, 2):
                cont = cont.reindex(index=[0, 1], columns=[0, 1], fill_value=0)
            if cont.values.sum() == 0:
                p = np.nan
                chi2_val = np.nan
            else:
                try:
                    if (cont < 5).any() and cont.shape == (2, 2):
                        _, p = fisher_exact(cont)
                        chi2_val = np.nan
                    else:
                        chi2_val, p, _, _ = chi2_contingency(cont)
                except (ValueError, TypeError):
                    chi2_val, p = np.nan, np.nan
            results_cluster.append(
                {
                    "Cluster": cl,
                    "Feature": feat,
                    "Chi2": round(chi2_val, 2) if not np.isnan(chi2_val) else np.nan,
                    "P_Value": round(p, 2) if not np.isnan(p) else np.nan,
                }
            )

    dfc = pd.DataFrame(results_cluster).dropna(subset=["P_Value"])
    if not dfc.empty:
        for cl in np.unique(clusters):
            mask = dfc["Cluster"] == cl
            subp = dfc.loc[mask, "P_Value"]
            if not subp.empty:
                rej, corr, _, _ = multipletests(subp, alpha=0.05, method="fdr_bh")
                dfc.loc[mask, "Adjusted_P"] = corr
                dfc.loc[mask, "FDR_Rejected"] = rej

    return dfg, dfc


# -----------------------------------------
# 13. Log-Odds Ratio
# -----------------------------------------
def _bootstrap_log_odds(a, b, c, d, n_bootstrap=500):
    out = []
    total_a = a + b
    total_b = c + d
    for _ in range(n_bootstrap):
        a_star = np.random.binomial(total_a, a / (a + b) if (a + b) > 0 else 0)
        c_star = np.random.binomial(total_b, c / (c + d) if (c + d) > 0 else 0)
        b_star = total_a - a_star
        d_star = total_b - c_star
        a_ = a_star + 0.5
        b_ = b_star + 0.5
        c_ = c_star + 0.5
        d_ = d_star + 0.5
        ratio = (a_ / b_) / (c_ / d_) if (b_ > 0 and d_ > 0) else 0
        out.append(np.log(ratio) if ratio > 0 else 0)
    return out


def log_odds_ratio_analysis(
    data, clusters, with_bootstrap_ci=True, n_bootstrap=500, confidence_level=0.95
):
    gl = []
    for feat in data.columns:
        a = data[feat].sum()
        b = len(data) - a
        ratio = (a / b) if b > 0 else np.nan
        lv = np.log(ratio) if (ratio and ratio > 0) else 0
        gl.append({"Feature": feat, "Log_Odds_Ratio": round(lv, 2) if not np.isnan(lv) else np.nan})

    df_global = pd.DataFrame(gl)

    out = []
    for cl in np.unique(clusters):
        c_mask = clusters == cl
        for feat in data.columns:
            a = data[feat][c_mask].sum()
            b = c_mask.sum() - a
            c = data[feat][~c_mask].sum()
            d = (~c_mask).sum() - c
            a_ = a + 0.5
            b_ = b + 0.5
            c_ = c + 0.5
            d_ = d + 0.5
            ratio = (a_ / b_) / (c_ / d_) if (b_ > 0 and d_ > 0) else 0
            lv = np.log(ratio) if ratio > 0 else 0
            ci_low, ci_high = np.nan, np.nan
            if with_bootstrap_ci:
                lom = _bootstrap_log_odds(a, b, c, d, n_bootstrap=n_bootstrap)
                ci_low = round(np.percentile(lom, ((1 - confidence_level) / 2) * 100), 2)
                ci_high = round(np.percentile(lom, (1 - (1 - confidence_level) / 2) * 100), 2)
            out.append(
                {
                    "Cluster": cl,
                    "Feature": feat,
                    "Odds_Ratio": round(ratio, 2) if not np.isnan(ratio) else np.nan,
                    "Log_Odds_Ratio": round(lv, 2) if not np.isnan(lv) else np.nan,
                    "CI_low": ci_low,
                    "CI_high": ci_high,
                }
            )
    df_cluster = pd.DataFrame(out)
    return df_global, df_cluster


# -----------------------------------------
# 14. Shared/Unique Features
# -----------------------------------------
def label_shared_unique_features(data, clusters):
    unique_clusters = np.unique(clusters)
    cluster_sets = {}
    for cluster_id in unique_clusters:
        c_data = data[clusters == cluster_id]
        feats_in_cluster = c_data.columns[c_data.sum() > 0]
        cluster_sets[cluster_id] = set(feats_in_cluster)

    global_counts = data.sum()
    all_features = data.columns
    feature_cluster_map = {}
    for feat in all_features:
        cls_list = []
        for cl in unique_clusters:
            if feat in cluster_sets[cl]:
                cls_list.append(cl)
        feature_cluster_map[feat] = cls_list

    shared_feats = []
    unique_feats = []
    for feat, cls_list in feature_cluster_map.items():
        if len(cls_list) >= 2:
            shared_feats.append(feat)
        elif len(cls_list) == 1:
            unique_feats.append(feat)

    df_shared_rows = []
    num_clusters_total = len(unique_clusters)
    for feat in shared_feats:
        cls_list = feature_cluster_map[feat]
        count_in_data = global_counts[feat]
        num_clusters_feat = len(cls_list)
        percent_in_clusters = round(100.0 * num_clusters_feat / num_clusters_total, 2)
        df_shared_rows.append(
            {
                "Feature": feat,
                "Clusters": ",".join(map(str, sorted(cls_list))),
                "NumClusters": num_clusters_feat,
                "Count": int(count_in_data),
                "Percent_in_Clusters": percent_in_clusters,
            }
        )
    df_shared = pd.DataFrame(df_shared_rows)

    df_unique_rows = []
    for feat in unique_feats:
        cls_list = feature_cluster_map[feat]
        cl = cls_list[0]
        sub_data = data[clusters == cl]
        count_in_cluster = sub_data[feat].sum()
        df_unique_rows.append({"Cluster": cl, "Feature": feat, "Count": int(count_in_cluster)})
    df_unique = pd.DataFrame(df_unique_rows)
    return df_shared, df_unique, cluster_sets


# -----------------------------------------
# 15. Association Rule Mining
# -----------------------------------------
def format_association_rules(df):
    df["antecedent"] = df["antecedent"].apply(lambda x: ", ".join(sorted(list(x))))
    df["consequent"] = df["consequent"].apply(lambda x: ", ".join(sorted(list(x))))
    return df


def association_rule_mining(data, clusters, min_support=0.3, min_confidence=0.7):
    rules_list = []
    for cluster in np.unique(clusters):
        c_mask = clusters == cluster
        c_data = data[c_mask]
        if c_data.empty:
            continue
        try:
            chunk_size = 1000
            n_chunks = max(1, len(c_data) // chunk_size)
            freq_items = set()
            for i in range(n_chunks):
                start = i * chunk_size
                end = start + chunk_size
                chunk = c_data.iloc[start:end].astype(bool)
                sup_counts = chunk.sum() / len(chunk)
                chunk_frequent = sup_counts[sup_counts >= min_support].index.tolist()
                freq_items.update(chunk_frequent)
            if not freq_items:
                continue
            f_items = list(freq_items)
            local_rules = []
            for i in range(len(f_items)):
                for j in range(i + 1, len(f_items)):
                    it1 = f_items[i]
                    it2 = f_items[j]
                    sup1 = c_data[it1].mean()
                    sup2 = c_data[it2].mean()
                    joint_sup = (c_data[it1] & c_data[it2]).mean()
                    if sup1 > 0:
                        conf = joint_sup / sup1
                        if conf >= min_confidence:
                            local_rules.append(
                                {
                                    "antecedent": frozenset([it1]),
                                    "consequent": frozenset([it2]),
                                    "support": round(joint_sup, 2),
                                    "confidence": round(conf, 2),
                                }
                            )
                    if sup2 > 0:
                        conf = joint_sup / sup2
                        if conf >= min_confidence:
                            local_rules.append(
                                {
                                    "antecedent": frozenset([it2]),
                                    "consequent": frozenset([it1]),
                                    "support": round(joint_sup, 2),
                                    "confidence": round(conf, 2),
                                }
                            )
            if local_rules:
                df_r = pd.DataFrame(local_rules)
                df_r["Cluster"] = cluster
                rules_list.append(df_r)
        except Exception as e:
            print(f"Association rule error in cluster {cluster}: {str(e)}")
            continue
    if rules_list:
        try:
            df_rules = pd.concat(rules_list, ignore_index=True)
            df_rules = format_association_rules(df_rules)
            return df_rules
        except (ValueError, TypeError, KeyError):
            return pd.DataFrame()
    return pd.DataFrame()


# -----------------------------------------
# 16. MCA with HTML
# -----------------------------------------
def multiple_correspondence_analysis(data, clusters, feature_group):
    try:
        mca_data = data.astype("category")
        mca = MCA(n_components=2, random_state=42)
        mca.fit(mca_data)
        row_coords = mca.row_coordinates(mca_data)
        row_coords.columns = ["Component_1", "Component_2"]
        row_coords["Cluster"] = clusters

        col_coords = mca.column_coordinates(mca_data)
        col_coords.columns = ["Component_1", "Component_2"]

        eigenvalues = mca.eigenvalues_
        total_inertia = sum(eigenvalues)

        mca_plot_html = create_mca_plot(row_coords, clusters, feature_group)

        corr_path = os.path.join(output_folder, f"{feature_group.lower()}_cluster_correlation.csv")
        heatmap_html = ""
        if os.path.exists(corr_path):
            corr_data = pd.read_csv(corr_path)
            if not corr_data.empty and all(
                x in corr_data.columns for x in ["Phi", "Row", "Column"]
            ):
                phi_matrix = pd.pivot_table(corr_data, values="Phi", index="Row", columns="Column")
                heatmap_html = create_correlation_heatmap(phi_matrix, feature_group)

        save_rounded_csv(
            row_coords, os.path.join(output_folder, f"MCA_{feature_group}_row_coordinates.csv")
        )
        save_rounded_csv(
            col_coords, os.path.join(output_folder, f"MCA_{feature_group}_column_coordinates.csv")
        )
        summary_df = pd.DataFrame(
            {
                "Component": range(1, len(eigenvalues) + 1),
                "Eigenvalue": [round(ev, 2) for ev in eigenvalues],
                "Explained_Variance": [round(ev / total_inertia, 4) for ev in eigenvalues],
                "Cumulative_Explained_Variance": [
                    round(np.sum(eigenvalues[: i + 1]) / total_inertia, 4)
                    for i in range(len(eigenvalues))
                ],
            }
        )
        save_rounded_csv(
            summary_df, os.path.join(output_folder, f"MCA_{feature_group}_summary.csv")
        )

        return row_coords, mca_plot_html, heatmap_html

    except Exception as e:
        print(f"Error in MCA for {feature_group}: {e}")
        traceback.print_exc()
        return pd.DataFrame(), "", ""


def create_mca_plot(data, clusters, feature_group):
    COLOR_SCHEME = px.colors.qualitative.Set1
    fig = px.scatter(
        data,
        x="Component_1",
        y="Component_2",
        color=clusters.astype(str),
        color_discrete_sequence=COLOR_SCHEME,
        title=f"MCA Analysis - {feature_group}",
        labels={"Component_1": "Dim1", "Component_2": "Dim2"},
        hover_data=["Cluster"],
    )
    return fig.to_html(full_html=False, include_plotlyjs=False)


def create_correlation_heatmap(corr_data, feature_group):
    COLOR_SCHEME = px.colors.diverging.RdBu
    fig = px.imshow(
        corr_data,
        title=f"Correlation Heatmap - {feature_group}",
        labels=dict(color="Phi Correlation"),
        x=corr_data.columns,
        y=corr_data.index,
        color_continuous_scale=COLOR_SCHEME,
        aspect="auto",
    )
    return fig.to_html(full_html=False, include_plotlyjs=False)


# -----------------------------------------
# 17. RandomForest Analysis
# -----------------------------------------
def analyze_cluster_importance(data, clusters):
    try:
        rf = RandomForestClassifier(n_estimators=50, random_state=42)
        rf.fit(data, clusters)
        imps = rf.feature_importances_
        df_imp = pd.DataFrame({"Feature": data.columns, "Importance": imps})
        df_imp["Importance"] = df_imp["Importance"].round(4)
        return df_imp.sort_values("Importance", ascending=False)
    except Exception as e:
        print(f"RandomForest error: {e}")
        return pd.DataFrame()


# -----------------------------------------
# 18. Save CSV (rounded)
# -----------------------------------------
def save_rounded_csv(df, filename):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].round(2)
    df.to_csv(filename, index=False)


# -----------------------------------------
# 19. Main Pipeline
# -----------------------------------------
def run_pipeline():
    print_memory_usage()

    # Load data from CSV
    mic_df = pd.read_csv(
        "MIC.csv",
        usecols=["Strain_ID"]
        + [c for c in pd.read_csv("MIC.csv", nrows=0).columns if c != "Strain_ID"],
    )
    amr_df = pd.read_csv(
        "AMR_genes.csv",
        usecols=["Strain_ID"]
        + [c for c in pd.read_csv("AMR_genes.csv", nrows=0).columns if c != "Strain_ID"],
    )
    vir_df = pd.read_csv(
        "Virulence.csv",
        usecols=["Strain_ID"]
        + [c for c in pd.read_csv("Virulence.csv", nrows=0).columns if c != "Strain_ID"],
    )

    print_memory_usage()

    # Separate Strain_ID
    strain_ids = mic_df["Strain_ID"]
    mic_df.drop(columns=["Strain_ID"], inplace=True)
    amr_df.drop(columns=["Strain_ID"], inplace=True)
    vir_df.drop(columns=["Strain_ID"], inplace=True)

    # Fill NAs
    mic_df.fillna(0, inplace=True)
    amr_df.fillna(0, inplace=True)
    vir_df.fillna(0, inplace=True)

    # Convert to binary
    bin_mic = mic_df.astype(int)
    bin_amr = amr_df.astype(int)
    bin_vir = vir_df.astype(int)

    # Validate
    validate_binary_data(bin_mic)
    validate_binary_data(bin_amr)
    validate_binary_data(bin_vir)

    categories = ["MIC", "AMR", "Virulence"]
    dataframes = [bin_mic, bin_amr, bin_vir]
    results = {}

    for cat, df in tqdm(
        zip(categories, dataframes), total=len(categories), desc="Analyzing categories"
    ):
        print(f"\n=== Analyzing {cat} Data ===")
        opt_k = retry_operation(lambda: determine_optimal_clusters_sqrt(df))
        model, clusters = retry_operation(lambda: perform_kmodes(df, opt_k))

        # Characteristic patterns
        pat_dict = extract_characteristic_patterns(model, df)
        pat_df = patterns_to_dataframe(pat_dict, cat, df, clusters)

        # Cluster stats (with bootstrap CI for cluster proportions)
        stats_df = calculate_cluster_stats(clusters)
        save_rounded_csv(
            stats_df, os.path.join(output_folder, f"{cat.lower()}_cluster_statistics.csv")
        )
        save_rounded_csv(
            pat_df, os.path.join(output_folder, f"{cat.lower()}_characteristic_patterns.csv")
        )

        # Chi-square
        chi2_global, chi2_per = chi_square_analysis(df, clusters)
        save_rounded_csv(chi2_global, os.path.join(output_folder, f"{cat.lower()}_chi2_global.csv"))
        save_rounded_csv(
            chi2_per, os.path.join(output_folder, f"{cat.lower()}_chi2_per_cluster.csv")
        )

        # Log-odds
        log_g, log_c = log_odds_ratio_analysis(
            df, clusters, with_bootstrap_ci=True, n_bootstrap=200
        )
        save_rounded_csv(log_g, os.path.join(output_folder, f"{cat.lower()}_log_odds_global.csv"))
        save_rounded_csv(
            log_c, os.path.join(output_folder, f"{cat.lower()}_log_odds_per_cluster.csv")
        )

        # Shared/Unique
        df_shared, df_unique, _ = label_shared_unique_features(df, clusters)
        save_rounded_csv(
            df_shared, os.path.join(output_folder, f"{cat.lower()}_shared_features.csv")
        )
        save_rounded_csv(
            df_unique, os.path.join(output_folder, f"{cat.lower()}_unique_features.csv")
        )

        # Logistic Regression
        coef_df = logistic_regression_feature_selection(df, clusters, with_ci=True, n_bootstrap=50)
        save_rounded_csv(
            coef_df,
            os.path.join(output_folder, f"{cat.lower()}_logistic_regression_coefficients.csv"),
        )

        # Association Rules
        rules_df = association_rule_mining(df, clusters, min_support=0.3, min_confidence=0.7)
        if not rules_df.empty:
            save_rounded_csv(
                rules_df, os.path.join(output_folder, f"{cat.lower()}_association_rules.csv")
            )

        # MCA + correlation Heatmap
        mca_coords, mca_plot_html, heatmap_html = multiple_correspondence_analysis(
            df, clusters, cat
        )
        if not mca_coords.empty:
            save_rounded_csv(
                mca_coords, os.path.join(output_folder, f"{cat.lower()}_MCA_results.csv")
            )

        # Random Forest
        rf_df = analyze_cluster_importance(df, clusters)
        if not rf_df.empty:
            save_rounded_csv(
                rf_df, os.path.join(output_folder, f"{cat.lower()}_cluster_importance.csv")
            )

        # Validation
        ch_score, db_score = validate_clusters(df, clusters)
        val_df = pd.DataFrame(
            {"Metric": ["Calinski-Harabasz", "Davies-Bouldin"], "Score": [ch_score, db_score]}
        )
        save_rounded_csv(
            val_df, os.path.join(output_folder, f"{cat.lower()}_validation_scores.csv")
        )

        # Pairwise FDR
        _ = pairwise_fdr_post_hoc(df, clusters, cat)
        # Correlation
        corr_df = cluster_correlation_analysis(df, clusters, cat)

        # Store results
        results[cat] = {
            "clusters": clusters,
            "patterns": pat_df,
            "stats": stats_df,
            "chi2_global": chi2_global,
            "chi2_per_cluster": chi2_per,
            "log_odds_global": log_g,
            "log_odds_per_cluster": log_c,
            "shared_features": df_shared,
            "unique_features": df_unique,
            "logistic_regression": coef_df,
            "association_rules": rules_df,
            "correlations": corr_df,
            "cluster_importance": rf_df,
            "validation_scores": val_df,
            "mca_plot": mca_plot_html,
            "heatmap_plot": heatmap_html,
        }

        print_memory_usage()

    integrated_df = pd.DataFrame(
        {
            "Strain_ID": strain_ids,
            "MIC_Cluster": results["MIC"]["clusters"],
            "AMR_Cluster": results["AMR"]["clusters"],
            "Virulence_Cluster": results["Virulence"]["clusters"],
        }
    )
    save_rounded_csv(
        integrated_df, os.path.join(output_folder, "integrated_clustering_results.csv")
    )

    combo = (
        integrated_df.groupby(["MIC_Cluster", "AMR_Cluster", "Virulence_Cluster"])
        .size()
        .reset_index(name="Count")
    )
    tot_samples = len(integrated_df)
    combo["Percentage"] = (combo["Count"] / tot_samples * 100).round(2)
    ci_list = []
    for _, row in combo.iterrows():
        ci = bootstrap_confidence_interval(row["Percentage"], row["Count"], tot_samples)
        ci_list.append(ci)
    combo["CI_low"], combo["CI_high"] = zip(*ci_list)
    combo = combo.sort_values("Count", ascending=False)
    save_rounded_csv(combo, os.path.join(output_folder, "combined_cluster_statistics_with_ci.csv"))

    all_pats = pd.concat([results[c]["patterns"] for c in categories])
    save_rounded_csv(all_pats, os.path.join(output_folder, "all_characteristic_patterns.csv"))

    print("\nPipeline complete. CSV results are in:", output_folder)
    print_memory_usage()

    return integrated_df, results


# -----------------------------------------
# 20. Load All CSV (Excluding Certain Files)
# -----------------------------------------
def load_all_csv_from_folder(folder_path):
    excluded_substrings = [
        "_column_coordinates.csv",
        "_row_coordinates.csv",
        "all_characteristic_patterns.csv",
    ]
    csv_results = {}
    for fname in os.listdir(folder_path):
        if fname.lower().endswith(".csv"):
            if any(substr in fname for substr in excluded_substrings):
                continue
            full_path = os.path.join(folder_path, fname)
            try:
                df = pd.read_csv(full_path)
                csv_results[fname] = df
            except Exception as e:
                print(f"[WARN] Could not load {fname}: {e}")
    return csv_results


# -----------------------------------------
# 21. Generate HTML Report
# -----------------------------------------
def generate_comprehensive_html_report(
    output_folder, results_dict, integrated_clusters, csv_results
):
    # Expanded methodology text with more technical/statistical details
    methodology_text = """
    <h3>Methodology</h3>
    <ul>
      <li><strong>Clustering Algorithm:</strong> K-Modes (Huang initialization). We use categorical data to define clusters
          via matching dissimilarities (mode-based distance). The number of clusters is determined via:
          <ul>
            <li><em>Sqrt heuristic:</em> upper bound as sqrt(N)</li>
            <li><em>Silhouette score:</em> we check 2..max_k and select the cluster count that gives the best silhouette.</li>
          </ul>
      </li>
      <li><strong>Assumptions for Clustering:</strong>
          <ul>
            <li>Binary 0/1 data is appropriate for K-Modes (no standard scaling needed, but we do ensure data is strictly binary).</li>
            <li>Features are independent indicators (though we later examine correlation/association).</li>
          </ul>
      </li>
      <li><strong>Statistical Tests and Corrections:</strong>
          <ul>
            <li>Chi-square tests for global associations with correction if < 5 expected counts (fallback to Fisher exact for 2x2).
                Benjamini-Hochberg FDR correction at alpha=0.05.</li>
            <li>Pairwise post-hoc FDR also uses multiple testing correction on P-values from chi-square or Fisher tests between clusters.</li>
            <li>Log-odds ratio with 0.5 pseudo-count correction to avoid infinite or zero ratio, plus bootstrap confidence intervals.</li>
          </ul>
      </li>
      <li><strong>Logistic Regression (L1):</strong>
          <ul>
            <li>Binary classification of cluster labels. We run logistic regression with L1 penalty (saga solver) to identify key features per cluster.</li>
            <li>Bootstrap approach with stratified sampling (200+ re-samples) to get coefficient confidence intervals (2.5%..97.5%).</li>
          </ul>
      </li>
      <li><strong>Multiple Correspondence Analysis (MCA):</strong>
          <ul>
            <li>We apply MCA to reduce dimensionality in categorical data, producing two principal components for visualization.</li>
            <li>Eigenvalue-based inertia is reported, along with row/column coordinates. We embed a scatter plot for a quick 2D overview.</li>
            <li>Optionally embed a correlation heatmap if available (Phi correlation within clusters).</li>
          </ul>
      </li>
      <li><strong>Random Forest Analysis:</strong>
          <ul>
            <li>We run a random forest classifier (50 trees) to estimate feature importance.
                This is a heuristic measure of how each binary feature influences cluster separation.</li>
          </ul>
      </li>
      <li><strong>Association Rules:</strong>
          <ul>
            <li>Within each cluster, we look for pairs of features with a minimum support=0.3 and confidence=0.7.
                Items meeting these thresholds are listed as rules (antecedent => consequent).</li>
          </ul>
      </li>
      <li><strong>Bootstrap Confidence Intervals:</strong>
          <ul>
            <li>We add bootstrap CIs for cluster percentage (e.g., cluster size ratio) and also for log-odds.
                A small 0.5 pseudo-count corrects extremes (0 or 100%).</li>
          </ul>
      </li>
      <li><strong>DataTables & Reporting:</strong>
          <ul>
            <li>All results are compiled into a single HTML report with interactive tables (sorting, searching, pagination).
                We exclude certain CSV files (MCA coordinates, all_characteristic_patterns) to keep the final section simpler.</li>
          </ul>
      </li>
    </ul>
    """

    html_template = r"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>StrepSuis-AMRVirKM: K-Modes Clustering of Antimicrobial Resistance and Virulence Profiles in Streptococcus suis</title>
      <!-- Bootstrap -->
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
      <!-- DataTables -->
      <link href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css" rel="stylesheet">
      <link href="https://cdn.datatables.net/buttons/2.4.1/css/buttons.dataTables.min.css" rel="stylesheet">
      <link href="https://cdn.datatables.net/searchbuilder/1.4.2/css/searchBuilder.dataTables.min.css" rel="stylesheet">
      <link href="https://cdn.datatables.net/searchpanes/2.1.2/css/searchPanes.dataTables.min.css" rel="stylesheet">
      <!-- Plotly -->
      <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
      <style>
      body { font-family: Arial,sans-serif; margin:10px; }
      .navbar-brand { font-weight:bold; }
      .container-fluid { width:95%; margin:0 auto; }
      .table-container { margin:20px 0; }
      .plot-container { margin:20px 0; }
      .heatmap-container { margin:20px 0; }
      </style>
    </head>
    <body>

      <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
          <a class="navbar-brand" href="#">StrepSuis-AMRVirKM</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
              <li class="nav-item"><a class="nav-link" href="#methodology">Methodology</a></li>
              {% for cat in categories %}
              <li class="nav-item"><a class="nav-link" href="#{{ cat }}">{{ cat }}</a></li>
              {% endfor %}
              <li class="nav-item"><a class="nav-link" href="#integrated">Integrated</a></li>
              <li class="nav-item"><a class="nav-link" href="#csv-results">All CSV Results</a></li>
            </ul>
          </div>
        </div>
      </nav>

      <div class="container-fluid">
        <h1>StrepSuis-AMRVirKM: K-Modes Clustering of Antimicrobial Resistance and Virulence Profiles in Streptococcus suis</h1>

        <div id="methodology">
          {{ methodology_text|safe }}
        </div>

        <hr/>
        {% for cat in categories %}
        <div id="{{ cat }}">
          <h2>{{ cat }} Analysis</h2>

          <!-- MCA Plot -->
          {% if results_dict[cat]['mca_plot'] %}
          <div class="plot-container">
            <h4>MCA Plot</h4>
            {{ results_dict[cat]['mca_plot']|safe }}
          </div>
          {% endif %}

          <!-- Heatmap -->
          {% if results_dict[cat]['heatmap_plot'] %}
          <div class="heatmap-container">
            <h4>Correlation Heatmap</h4>
            {{ results_dict[cat]['heatmap_plot']|safe }}
          </div>
          {% endif %}

          <!-- Stats table -->
          <div class="table-container">
            <h4>{{ cat }} Cluster Statistics (with CIs)</h4>
            <table class="table table-striped data-table">
              <thead>
                <tr><th>Cluster</th><th>Count</th><th>Percentage</th><th>CI_low</th><th>CI_high</th></tr>
              </thead>
              <tbody>
                {% for idx, row in results_dict[cat]['stats'].iterrows() %}
                <tr>
                  <td>{{ idx }}</td>
                  <td>{{ row['Count'] }}</td>
                  <td>{{ row['Percentage'] }}</td>
                  <td>{{ row['CI_low'] }}</td>
                  <td>{{ row['CI_high'] }}</td>
                </tr>
                {% endfor %}
              </tbody>
            </table>
          </div>

          <!-- Patterns -->
          <div class="table-container">
            <h4>{{ cat }} Characteristic Patterns</h4>
            <table class="table table-striped data-table">
              <thead>
                <tr><th>Cluster</th><th>Size</th><th>Characteristic_Pattern</th><th>Type</th></tr>
              </thead>
              <tbody>
                {% for _, row in results_dict[cat]['patterns'].iterrows() %}
                <tr>
                  <td>{{ row['Cluster'] }}</td>
                  <td>{{ row['Size'] }}</td>
                  <td>{{ row['Characteristic_Pattern'] }}</td>
                  <td>{{ row['Type'] }}</td>
                </tr>
                {% endfor %}
              </tbody>
            </table>
          </div>

          <!-- Shared Features -->
          <div class="table-container">
            <h4>{{ cat }} Shared Features</h4>
            <table class="table table-striped data-table">
              <thead>
                <tr><th>Feature</th><th>Clusters</th><th>NumClusters</th><th>Count</th><th>Percent_in_Clusters</th></tr>
              </thead>
              <tbody>
                {% for _, row in results_dict[cat]['shared_features'].iterrows() %}
                <tr>
                  <td>{{ row['Feature'] }}</td>
                  <td>{{ row['Clusters'] }}</td>
                  <td>{{ row['NumClusters'] }}</td>
                  <td>{{ row['Count'] }}</td>
                  <td>{{ row['Percent_in_Clusters'] }}</td>
                </tr>
                {% endfor %}
              </tbody>
            </table>
          </div>

          <!-- Unique Features -->
          <div class="table-container">
            <h4>{{ cat }} Unique Features</h4>
            <table class="table table-striped data-table">
              <thead>
                <tr><th>Cluster</th><th>Feature</th><th>Count</th></tr>
              </thead>
              <tbody>
                {% for _, row in results_dict[cat]['unique_features'].iterrows() %}
                <tr>
                  <td>{{ row['Cluster'] }}</td>
                  <td>{{ row['Feature'] }}</td>
                  <td>{{ row['Count'] }}</td>
                </tr>
                {% endfor %}
              </tbody>
            </table>
          </div>

          <!-- Log-Odds Per Cluster -->
          <div class="table-container">
            <h4>{{ cat }} Log-Odds Per Cluster</h4>
            <table class="table table-striped data-table">
              <thead>
                <tr><th>Cluster</th><th>Feature</th><th>Odds_Ratio</th><th>Log_Odds_Ratio</th><th>CI_low</th><th>CI_high</th></tr>
              </thead>
              <tbody>
                {% for _, row in results_dict[cat]['log_odds_per_cluster'].iterrows() %}
                <tr>
                  <td>{{ row['Cluster'] }}</td>
                  <td>{{ row['Feature'] }}</td>
                  <td>{{ row['Odds_Ratio'] }}</td>
                  <td>{{ row['Log_Odds_Ratio'] }}</td>
                  <td>{{ row['CI_low'] }}</td>
                  <td>{{ row['CI_high'] }}</td>
                </tr>
                {% endfor %}
              </tbody>
            </table>
          </div>

        </div>
        <hr/>
        {% endfor %}

        <!-- Integrated Clusters -->
        <div id="integrated">
          <h2>Integrated Clustering Results</h2>
          <table class="table table-striped data-table">
            <thead>
              <tr><th>Strain_ID</th><th>MIC_Cluster</th><th>AMR_Cluster</th><th>Virulence_Cluster</th></tr>
            </thead>
            <tbody>
              {% for _, row in integrated_clusters.iterrows() %}
              <tr>
                <td>{{ row['Strain_ID'] }}</td>
                <td>{{ row['MIC_Cluster'] }}</td>
                <td>{{ row['AMR_Cluster'] }}</td>
                <td>{{ row['Virulence_Cluster'] }}</td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </div>

        <!-- All CSV Results -->
        <hr/>
        <div id="csv-results">
          <h2>All CSV Results</h2>
          <p>Below are all CSV files found in <code>{{ output_folder }}</code> (excluding certain files by design).</p>
          {% for filename, df in csv_results.items() %}
          <div class="table-container">
            <h4>{{ filename }}</h4>
            <table class="table table-striped data-table">
              <thead>
                {% if df.shape[1]>0 %}
                <tr>
                  {% for col in df.columns %}
                  <th>{{ col }}</th>
                  {% endfor %}
                </tr>
                {% endif %}
              </thead>
              <tbody>
                {% for _, row in df.iterrows() %}
                <tr>
                  {% for col in df.columns %}
                  <td>{{ row[col] }}</td>
                  {% endfor %}
                </tr>
                {% endfor %}
              </tbody>
            </table>
          </div>
          {% endfor %}
        </div>
      </div>

      <script src="https://code.jquery.com/jquery-3.5.1.js"></script>
      <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
      <script src="https://cdn.datatables.net/buttons/2.4.1/js/dataTables.buttons.min.js"></script>
      <script src="https://cdn.datatables.net/buttons/2.4.1/js/buttons.html5.min.js"></script>
      <script src="https://cdn.datatables.net/buttons/2.4.1/js/buttons.print.min.js"></script>
      <script src="https://cdn.datatables.net/searchbuilder/1.4.2/js/dataTables.searchBuilder.min.js"></script>
      <script src="https://cdn.datatables.net/searchpanes/2.1.2/js/dataTables.searchPanes.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

      <script>
      $(document).ready(function() {
          $('.data-table').DataTable({
              dom: 'Blfrtip',
              buttons: ['copy','csv','excel','pdf','print'],
              lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
              pageLength: 10,
              responsive: true
          });
      });
      </script>
    </body>
    </html>
    """

    template = jinja2.Template(html_template)
    categories = list(results_dict.keys())
    rendered_html = template.render(
        categories=categories,
        results_dict=results_dict,
        integrated_clusters=integrated_clusters,
        csv_results=csv_results,
        output_folder=output_folder,
        methodology_text=methodology_text,
    )

    final_report_path = os.path.join(output_folder, "comprehensive_cluster_analysis_report.html")
    with open(final_report_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)

    print(f"\nFinal HTML report generated: {final_report_path}")


# -----------------------------------------
# 21b. Generate Excel Report
# -----------------------------------------
def generate_comprehensive_excel_report(
    output_folder, results_dict, integrated_clusters, csv_results
):
    """
    Generate comprehensive Excel report with all analysis results and PNG charts.

    This function creates a detailed Excel workbook with multiple sheets containing:
    - Metadata and methodology
    - Clustering results for each category (MIC, AMR, Virulence)
    - Statistical tests (Chi-square, Log-odds, Bootstrap CIs)
    - Feature importance from Random Forest
    - Multiple Correspondence Analysis (MCA) results
    - Association rules
    - Integrated cluster assignments
    - All CSV results from the analysis

    Parameters:
        output_folder (str): Directory for output files
        results_dict (dict): Dictionary containing all analysis results by category
        integrated_clusters (pd.DataFrame): Integrated cluster assignments
        csv_results (dict): Dictionary of all CSV files from analysis

    Returns:
        str: Path to generated Excel file
    """
    # Initialize Excel report generator
    excel_gen = ExcelReportGenerator(output_folder=output_folder)

    # Save any plotly figures as PNG
    for category, cat_results in results_dict.items():
        # Save MCA scatter plots if available
        if "mca_scatter" in cat_results and cat_results["mca_scatter"]:
            try:
                # Parse base64 image data if present
                import re

                match = re.search(r'data:image/png;base64,([^"]+)', str(cat_results["mca_scatter"]))
                if match:
                    img_data = match.group(1)
                    # Decode and save
                    import base64
                    from io import BytesIO

                    from PIL import Image

                    img = Image.open(BytesIO(base64.b64decode(img_data)))
                    filepath = os.path.join(excel_gen.png_folder, f"mca_scatter_{category}.png")
                    img.save(filepath)
                    excel_gen.png_files.append(filepath)
                    print(f"Saved MCA scatter plot: {filepath}")
            except Exception as e:
                print(f"Could not save MCA scatter for {category}: {e}")

        # Save heatmaps if available
        if "heatmap" in cat_results and cat_results["heatmap"]:
            try:
                match = re.search(r'data:image/png;base64,([^"]+)', str(cat_results["heatmap"]))
                if match:
                    img_data = match.group(1)
                    import base64
                    from io import BytesIO

                    from PIL import Image

                    img = Image.open(BytesIO(base64.b64decode(img_data)))
                    filepath = os.path.join(excel_gen.png_folder, f"heatmap_{category}.png")
                    img.save(filepath)
                    excel_gen.png_files.append(filepath)
                    print(f"Saved heatmap: {filepath}")
            except Exception as e:
                print(f"Could not save heatmap for {category}: {e}")

    # Prepare methodology description
    methodology = {
        "K-Modes Clustering": (
            "Huang initialization with automatic cluster number selection using silhouette score. "
            "Cluster count determined via sqrt(N) heuristic and silhouette optimization (2 to max_k). "
            "Binary 0/1 data appropriate for K-Modes (mode-based distance metric)."
        ),
        "Statistical Tests": (
            "Chi-square tests for global associations with Yates correction when expected counts < 5. "
            "Fisher exact test fallback for 2x2 tables. "
            "Benjamini-Hochberg FDR correction at alpha=0.05 for multiple testing. "
            "Pairwise post-hoc tests with FDR correction for cluster comparisons."
        ),
        "Log-odds Ratio": (
            "0.5 pseudo-count correction to avoid infinite or zero ratios. "
            "Bootstrap confidence intervals (200+ resamples) with stratified sampling."
        ),
        "Logistic Regression": (
            "L1 penalty (saga solver) for binary classification of cluster labels. "
            "Bootstrap approach (200+ resamples) for coefficient confidence intervals (2.5%-97.5%)."
        ),
        "Multiple Correspondence Analysis": (
            "Dimensionality reduction for categorical data producing two principal components. "
            "Eigenvalue-based inertia reported with row/column coordinates. "
            "2D scatter plot visualization for cluster separation."
        ),
        "Random Forest": (
            "50-tree classifier for feature importance estimation. "
            "Heuristic measure of feature influence on cluster separation."
        ),
        "Association Rules": (
            "Minimum support=0.3 and confidence=0.7 thresholds. "
            "Items meeting criteria listed as antecedent => consequent rules."
        ),
        "Bootstrap Confidence Intervals": (
            "Applied to cluster percentages and log-odds ratios. "
            "0.5 pseudo-count corrects extreme values (0 or 100%)."
        ),
    }

    # Prepare sheets data
    sheets_data = {}

    # Integrated clusters
    if integrated_clusters is not None and not integrated_clusters.empty:
        sheets_data["Integrated_Clusters"] = (
            integrated_clusters,
            f"Integrated cluster assignments across all categories (N={len(integrated_clusters)} strains)",
        )

    # Category-specific results
    for category, cat_results in results_dict.items():
        prefix = sanitize_sheet_name(category)[:20]  # Limit prefix length

        # Cluster assignments
        if "cluster_df" in cat_results and cat_results["cluster_df"] is not None:
            sheet_name = f"{prefix}_Clusters"
            sheets_data[sheet_name] = (
                cat_results["cluster_df"],
                f"Cluster assignments for {category}",
            )

        # Chi-square results
        if "chi2_results" in cat_results and cat_results["chi2_results"] is not None:
            sheet_name = f"{prefix}_Chi2"
            sheets_data[sheet_name] = (
                cat_results["chi2_results"],
                f"Chi-square test results for {category}",
            )

        # Log-odds results
        if "log_odds_df" in cat_results and cat_results["log_odds_df"] is not None:
            sheet_name = f"{prefix}_LogOdds"
            sheets_data[sheet_name] = (
                cat_results["log_odds_df"],
                f"Log-odds ratios with bootstrap CIs for {category}",
            )

        # Feature importance
        if "feature_importance" in cat_results and cat_results["feature_importance"] is not None:
            sheet_name = f"{prefix}_RF_Import"
            sheets_data[sheet_name] = (
                cat_results["feature_importance"],
                f"Random Forest feature importance for {category}",
            )

        # Association rules
        if "association_rules" in cat_results and cat_results["association_rules"] is not None:
            sheet_name = f"{prefix}_Assoc_Rules"
            sheets_data[sheet_name] = (
                cat_results["association_rules"],
                f"Association rules for {category}",
            )

        # MCA coordinates
        if "mca_coords" in cat_results and cat_results["mca_coords"] is not None:
            sheet_name = f"{prefix}_MCA"
            sheets_data[sheet_name] = (cat_results["mca_coords"], f"MCA coordinates for {category}")

    # Add CSV results that are not already included
    excluded_files = [
        "mca_row_coordinates",
        "mca_column_coordinates",
        "all_characteristic_patterns",
    ]
    for csv_name, csv_df in csv_results.items():
        # Create sheet name from CSV filename
        base_name = csv_name.replace(".csv", "")
        # Check if not already added and not in exclusion list
        if not any(excl in base_name.lower() for excl in excluded_files):
            sheet_name = sanitize_sheet_name(base_name)
            if sheet_name not in sheets_data:
                sheets_data[sheet_name] = (csv_df, f"Results from {csv_name}")

    # Prepare metadata
    total_clusters_per_category = {}
    for category, cat_results in results_dict.items():
        if "cluster_df" in cat_results and cat_results["cluster_df"] is not None:
            n_clusters = (
                cat_results["cluster_df"]["Cluster"].nunique()
                if "Cluster" in cat_results["cluster_df"].columns
                else 0
            )
            total_clusters_per_category[category] = n_clusters

    metadata = {
        "Total_Strains": len(integrated_clusters) if integrated_clusters is not None else 0,
        "Categories_Analyzed": len(results_dict),
        "Total_Sheets": len(sheets_data),
        "Total_PNG_Charts": len(excel_gen.png_files),
    }

    # Add cluster counts to metadata
    for category, n_clusters in total_clusters_per_category.items():
        metadata[f"Clusters_{category}"] = n_clusters

    # Generate Excel report
    excel_path = excel_gen.generate_excel_report(
        report_name="Cluster_Analysis_Report",
        sheets_data=sheets_data,
        methodology=methodology,
        **metadata,
    )

    print(f"\nExcel report generated: {excel_path}")

    return excel_path


# -----------------------------------------
# 22. Main Function
# -----------------------------------------
def main():
    # 1. Run pipeline
    integrated_df, results_dict = run_pipeline()

    # 2. Load all CSV from the output folder (excluding certain files)
    all_csv_results = load_all_csv_from_folder(output_folder)

    # 3. Generate final comprehensive HTML report
    generate_comprehensive_html_report(
        output_folder=output_folder,
        results_dict=results_dict,
        integrated_clusters=integrated_df,
        csv_results=all_csv_results,
    )

    # 4. Generate comprehensive Excel report
    generate_comprehensive_excel_report(
        output_folder=output_folder,
        results_dict=results_dict,
        integrated_clusters=integrated_df,
        csv_results=all_csv_results,
    )

    print("\nAnalysis complete. Please check the HTML and Excel reports in:", output_folder)


if __name__ == "__main__":
    main()
