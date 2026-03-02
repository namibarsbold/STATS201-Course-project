# Electrification Inequality and Spatial Infrastructure: A Tile-Level Panel Analysis of Brazil, China, and Morocco (2014–2023)

A machine-learning panel study that uses VIIRS nighttime-light tiles, population rasters, and OpenStreetMap infrastructure data to model and explain electrification inequality across three middle-income countries over a decade.

**GitHub Pages:** https://namibarsbold.github.io/STATS201-Course-project/

---

## Team

| Name | Role |
|------|------|
| Nami | Editing, Interpretation, Data Visualization |
| Amanda | Editing, Interpretation, Data Visualization |
| Bouchra | Data Analyst and Model Designer |

---

## Folder Structure

```
STATS201-Course-project/
├── data/
│   ├── processed/          # Cleaned panel CSVs (VIIRS country panel)
│   ├── monthly_viirs/      # Raw monthly VIIRS feature/label files
│   └── week_5_robustness_tif_images/  # Morocco GeoTIFF rasters (Brazil & China excluded — see note below)
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
│   └── index.html          # GitHub Pages report (generated from FINAL_REPORT.ipynb)
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

# Step 6 — Open and edit the final report notebook
jupyter notebook notebooks/FINAL_REPORT.ipynb

# Step 7 — Regenerate the GitHub Pages HTML from the notebook
# Run this after filling in content and re-running all cells in the notebook:
jupyter nbconvert --to html --execute notebooks/FINAL_REPORT.ipynb \
    --output index.html --output-dir docs/
```

---

## How to Get the Data

| Dataset | Format | Source | Access |
|---------|--------|--------|--------|
| VIIRS Nighttime Lights — Morocco GeoTIFF rasters (2014–2023) | `.tif` | Google Earth Engine (GEE) | Already in `data/week_5_robustness_tif_images/` |
| VIIRS Nighttime Lights — Brazil & China GeoTIFF rasters (2014–2023) | `.tif` | Google Earth Engine (GEE) | **Not included** — files are 241–394 MB each, exceeding GitHub's 100 MB limit. Re-export using the GEE script below and place in `data/week_5_robustness_tif_images/` |
| VIIRS Nighttime Lights — country-level CSV panel | `.csv` | Derived from GEE exports | Already in `data/processed/` |
| WorldPop population rasters (1 km, annual) | `.tif` | WorldPop Hub | https://www.worldpop.org — download 100m or 1km unconstrained grids |
| OpenStreetMap infrastructure (roads, power lines) | `.pbf` / `.shp` | Geofabrik | https://download.geofabrik.de — select country extracts |

### VIIRS extraction via Google Earth Engine

The annual VIIRS GeoTIFF rasters were exported using a **Google Earth Engine JavaScript script**. The original script is no longer available, but to reproduce the exports:

1. Go to https://code.earthengine.google.com
2. Use the following template (adjust `country`, `year`, and geometry as needed):

```javascript
// VIIRS Annual Composite Export — Google Earth Engine
var year = 2020;
var country = 'Morocco';  // change to 'Brazil' or 'China'

// Define country geometry (draw or use FAO GAUL)
var geometry = ee.FeatureCollection('FAO/GAUL/2015/level0')
                 .filter(ee.Filter.eq('ADM0_NAME', country))
                 .geometry();

// Load VIIRS monthly composites and compute annual mean
var viirs = ee.ImageCollection('NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG')
              .filterDate(year + '-01-01', (year + 1) + '-01-01')
              .select('avg_rad')
              .mean()
              .clip(geometry);

// Export to Google Drive
Export.image.toDrive({
  image: viirs,
  description: country + '_' + year,
  folder: 'VIIRS_exports',
  fileNamePrefix: country + '_' + year,
  region: geometry,
  scale: 500,
  crs: 'EPSG:4326',
  maxPixels: 1e13
});
```

3. Click **Run**, then **Tasks** tab → click **Run** next to the export task
4. Download the `.tif` from Google Drive and place it in `data/week_5_robustness_tif_images/`

Place all raw data files under `data/` before running the pipeline scripts.
