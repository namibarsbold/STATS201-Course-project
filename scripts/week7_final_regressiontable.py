import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

# =========================================================
# 1) PATHS
# =========================================================
BASE_PATH = r"C:\Users\amimi\OneDrive - Duke University\SCHOOL\SPRING 2026\STATS201\Week 6 Files\STATS201-Course-project\figures"
INPUT_PATH = os.path.join(BASE_PATH, "week6_outputs")
OUTPUT_PATH = os.path.join(BASE_PATH, "week7_outputs")
os.makedirs(OUTPUT_PATH, exist_ok=True)

OUTFILE = os.path.join(OUTPUT_PATH, "week7_baseline_regression_table.png")

COUNTRIES = ["Brazil", "China", "Morocco"]
YEAR = 2023
FORMULA = "log_light ~ log_pop + C(region_type) + log_pop:C(region_type)"

# Project regime order + labels (reader friendly)
REGIME_ORDER = ["empty_or_rural", "mixed", "bright_sparse", "dense_dim", "urban_core"]
REGIME_LABELS = {
    "empty_or_rural": "Empty / Rural",
    "mixed": "Mixed",
    "bright_sparse": "Bright Sparse",
    "dense_dim": "Dense-Intermediate",
    "urban_core": "Urban Core",
}

# =========================================================
# 2) HELPERS
# =========================================================
def star(p):
    if p < 0.01: return "***"
    if p < 0.05: return "**"
    if p < 0.10: return "*"
    return ""

def interaction_name(level):
    # statsmodels names look like: "log_pop:C(region_type)[T.urban_core]"
    return f"log_pop:C(region_type)[T.{level}]"

def main_effect_name():
    return "log_pop"

def safe_get(series, key, default=np.nan):
    return series[key] if key in series.index else default

# Compute implied slope for regime r:
# - reference regime slope = beta_log_pop
# - other regime slope = beta_log_pop + beta_interaction_r
# SE computed from covariance matrix (delta method):
# Var(beta + gamma) = Var(beta) + Var(gamma) + 2Cov(beta,gamma)
def implied_slope(model, regime_level, ref_level):
    params = model.params
    cov = model.cov_params()

    b = safe_get(params, main_effect_name())
    var_b = cov.loc[main_effect_name(), main_effect_name()] if main_effect_name() in cov.index else np.nan

    if regime_level == ref_level:
        slope = b
        se = np.sqrt(var_b) if np.isfinite(var_b) else np.nan
        # p-value: use main effect p-value
        p = safe_get(model.pvalues, main_effect_name(), np.nan)
        return slope, se, p

    inter = interaction_name(regime_level)
    g = safe_get(params, inter)

    if (main_effect_name() not in cov.index) or (inter not in cov.index):
        return np.nan, np.nan, np.nan

    var_g = cov.loc[inter, inter]
    cov_bg = cov.loc[main_effect_name(), inter]

    slope = b + g
    se = np.sqrt(var_b + var_g + 2 * cov_bg)

    # two-sided p-value for linear combination: t = slope / se, df = model.df_resid
    if se == 0 or not np.isfinite(se):
        p = np.nan
    else:
        t = slope / se
        df = model.df_resid
        # statsmodels uses scipy; avoid importing: approximate with normal if needed
        # but scipy is typically available with statsmodels; we’ll use it safely:
        try:
            from scipy import stats
            p = 2 * (1 - stats.t.cdf(abs(t), df))
        except Exception:
            # fallback normal approx
            from math import erf, sqrt
            p = 2 * (1 - 0.5 * (1 + erf(abs(t) / sqrt(2))))
    return slope, se, p

# =========================================================
# 3) RUN MODELS + BUILD TABLE CONTENT
# =========================================================
models = {}
meta = {}
ref_levels = {}

for country in COUNTRIES:
    file_path = os.path.join(INPUT_PATH, f"tiles_{country}_{YEAR}.csv")
    if not os.path.exists(file_path):
        print(f"⚠️ Missing: {file_path}")
        continue

    df = pd.read_csv(file_path)

    pop_col = "sum_pop" if "sum_pop" in df.columns else "mean_pop"
    df["log_pop"] = np.log1p(df[pop_col])
    df["log_light"] = np.log1p(df["mean_light"])

    # enforce categorical with stable ordering if possible
    df["region_type"] = df["region_type"].astype("category")

    # Fit
    m = smf.ols(FORMULA, data=df).fit()

    models[country] = m
    meta[country] = {"N": int(m.nobs), "R2": m.rsquared}

    # statsmodels reference category is the first category in the dtype
    ref_levels[country] = df["region_type"].cat.categories[0]

# Determine a single reference level for reporting:
# We’ll use Brazil's ref if available, else first available model's ref.
ref_level = None
for c in COUNTRIES:
    if c in ref_levels:
        ref_level = ref_levels[c]
        break
if ref_level is None:
    raise RuntimeError("No models ran. Check file paths and inputs.")

# If your ref level isn't empty_or_rural, this will still work,
# but your “Empty/Rural” row might not be the reference.
# Ideally you set region_type categories so empty_or_rural is the reference in your data.

# Build rows: one per regime, with implied slope
row_labels = [REGIME_LABELS.get(r, r) + " elasticity" for r in REGIME_ORDER]

table_cells = []
for r in REGIME_ORDER:
    row = []
    for c in COUNTRIES:
        if c not in models:
            row.append("")
            continue
        slope, se, p = implied_slope(models[c], r, ref_level)
        if not np.isfinite(slope) or not np.isfinite(se):
            row.append("—")
        else:
            row.append(f"{slope:.3f}{star(p)}\n({se:.3f})")
    table_cells.append(row)

# Add meta rows
table_cells.append([f"{meta[c]['N']:,}" if c in meta else "" for c in COUNTRIES])
row_labels.append("Observations")

table_cells.append([f"{meta[c]['R2']:.3f}" if c in meta else "" for c in COUNTRIES])
row_labels.append("R-squared")

# =========================================================
# 4) RENDER PUBLICATION-READY PNG (ROW HEIGHT + NOTE PLACEMENT FIXED)
# =========================================================
fig = plt.figure(figsize=(14.5, 8.8))  # larger canvas to prevent crowding
ax = fig.add_axes([0, 0, 1, 1])
ax.axis("off")

col_labels = COUNTRIES

# ---- Define a fixed table bounding box (axes coordinates) ----
# left, bottom, width, height
TABLE_BBOX = [0.05, 0.16, 0.90, 0.70]  # big table area; leaves room for title + note

tbl = ax.table(
    cellText=table_cells,
    rowLabels=row_labels,
    colLabels=col_labels,
    cellLoc="center",
    rowLoc="left",
    loc="center",
    bbox=TABLE_BBOX
)

# ---- Typography ----
tbl.auto_set_font_size(False)
tbl.set_fontsize(12)

# ---- Explicit column widths ----
rowlabel_w = 0.42
datacol_w = 0.19

n_rows = len(row_labels) + 1   # header included
n_cols = len(col_labels)

# Apply widths
for r in range(1, n_rows):
    if (r, -1) in tbl.get_celld():
        tbl[(r, -1)].set_width(rowlabel_w)

for r in range(0, n_rows):
    for c in range(0, n_cols):
        if (r, c) in tbl.get_celld():
            tbl[(r, c)].set_width(datacol_w)

# ---- Force row heights (this is the real fix for “rows too small”) ----
# Compute a sensible row height relative to the table bbox height.
# Give header a bit more height.
base_h = (TABLE_BBOX[3] / n_rows) * 1.10   # 10% extra height
header_h = base_h * 1.20

for r in range(0, n_rows):
    for c in range(-1, n_cols):
        if (r, c) in tbl.get_celld():
            tbl[(r, c)].set_height(header_h if r == 0 else base_h)

# ---- Padding + line spacing ----
for (r, c), cell in tbl.get_celld().items():
    cell.PAD = 0.28            # MUCH more whitespace inside each cell
    cell.set_edgecolor("black")
    cell.set_linewidth(0.35)
    cell.get_text().set_linespacing(1.55)  # more breathing room for coef + (se)

# ---- Header styling ----
for j in range(n_cols):
    if (0, j) in tbl.get_celld():
        cell = tbl[(0, j)]
        cell.set_text_props(weight="bold")
        cell.set_linewidth(0.9)
        cell.PAD = 0.32

# ---- Row label styling ----
for i in range(1, n_rows):
    if (i, -1) in tbl.get_celld():
        tbl[(i, -1)].set_text_props(weight="bold", ha="left")
        tbl[(i, -1)].PAD = 0.34

# ---- Light row striping for readability (regime rows only) ----
data_row_count = len(REGIME_ORDER)
for i in range(1, data_row_count + 1):
    if i % 2 == 0:
        if (i, -1) in tbl.get_celld():
            tbl[(i, -1)].set_facecolor((0, 0, 0, 0.04))
        for j in range(n_cols):
            if (i, j) in tbl.get_celld():
                tbl[(i, j)].set_facecolor((0, 0, 0, 0.04))

# ---- Title (tight, above table) ----
fig.text(
    0.5, 0.93,
    f"Week 7 — Baseline Model Fit & Elasticities ({YEAR})",
    ha="center",
    va="center",
    fontsize=16,
    weight="bold"
)
fig.text(
    0.5, 0.90,
    "DV: log(1 + Nighttime Lights) • Elasticities by Development Regime",
    ha="center",
    va="center",
    fontsize=12
)

# ---- Note placed relative to the table bbox (close to table) ----
note_y = TABLE_BBOX[1] - 0.035  # just under the table
fig.text(
    0.5, note_y,
    "Notes: Cells show the implied slope of log(1+Population) within each regime (standard errors in parentheses). "
    "*** p<0.01, ** p<0.05, * p<0.10.",
    ha="center",
    va="top",
    fontsize=10
)

plt.savefig(OUTFILE, dpi=300, bbox_inches="tight")
plt.close()
print(f"✅ Saved: {OUTFILE}")