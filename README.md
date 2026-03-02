# Electrification Inequality and Spatial Infrastructure: A Tile-Level Panel Analysis of Brazil, China, and Morocco (2014–2023)

A machine-learning panel study that uses VIIRS nighttime-light tiles, population rasters, and OpenStreetMap infrastructure data to model and explain electrification inequality across three middle-income countries over a decade.

**GitHub Pages:** https://namibarsbold.github.io/STATS201-Course-project/

---

## Team

| Name | Role |
|------|------|
| Namibarsbold |  |
| Amanda | |
| Bouchra |  |

---

## Folder Structure

```
STATS201-Course-project/
├── data/
│   ├── processed/          # Cleaned panel CSVs (VIIRS country panel)
│   ├── monthly_viirs/      # Raw monthly VIIRS feature/label files
│   └── week_5_robustness_tif_images/  # Morocco annual GeoTIFF rasters
├── notebooks/
│   ├── FINAL_REPORT.ipynb  # Final report notebook (authoritative)
│   ├── Week_2_Preliminary_Model.ipynb
│   ├── week4_submission_pipeline_updated.ipynb
│   ├── week5_*.ipynb       # Image feature extraction notebooks
│   ├── week6_make_time_trends.ipynb
│   └── week7_finalmodel_analysis.ipynb
├── scripts/
│   ├── final_regression.py
│   ├── iae_viirs_yearly.py
│   ├── week6_*.py          # Regression and visualization scripts
│   └── week7_*.py
├── figures/                # All output figures organized by week/stage
├── docs/
│   └── index.html          # GitHub Pages report webpage
├── requirements.txt
└── README.md
```

---

## How to Reproduce

### 1. Environment Setup

```bash
# Clone the repo
git clone https://github.com/namibarsbold/STATS201-Course-project.git
cd STATS201-Course-project

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Script Run Order

```bash
# Step 1 — Build yearly VIIRS country panel
python scripts/iae_viirs_yearly.py

# Step 2 — Build tile-level panel for all years and countries
python scripts/week6_build_tiles_all_years.py

# Step 3 — Add geographic / OSM infrastructure features
python scripts/week6_add_geographic_infrastructure.py

# Step 4 — Run baseline regression and visualizations
python scripts/week6_visualize_baseline_regression.py
python scripts/week6_visualize_structure.py
python scripts/week6_visualize_comparisons.py
python scripts/week6_visualize_interactions.py

# Step 5 — Final regression and figures
python scripts/final_regression.py
python scripts/week7_final_regressiontable.py
python scripts/week7_final_scatterplots.py

# Step 6 — Open final report notebook
jupyter notebook notebooks/FINAL_REPORT.ipynb
```

---

## How to Get the Data

| Dataset | Source | Access |
|---------|--------|--------|
| VIIRS Nighttime Lights (annual composites) | NASA LAADS DAAC | https://ladsweb.modaps.eosdis.nasa.gov — search for VNP46A3 / VNP46A4 products |
| WorldPop population rasters (1 km, annual) | WorldPop Hub | https://www.worldpop.org — download 100m or 1km unconstrained grids |
| OpenStreetMap infrastructure (roads, power lines) | Geofabrik | https://download.geofabrik.de — select country extracts in PBF or SHP format |

Place raw data files under `data/` before running the pipeline scripts.
