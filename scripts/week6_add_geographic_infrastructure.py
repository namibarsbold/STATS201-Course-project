"""
Add Geographic Infrastructure Features to Tiles Panel
======================================================

This script adds infrastructure accessibility measures WITHOUT downloading external data.
Computes for ALL countries and ALL years in your panel:
  - distance_to_urban_core: pixels to nearest urban tile
  - local_urban_density: count of urban tiles nearby
  - centrality_score: position relative to country center

Much faster than downloading roads (~30 min for all countries/years).

Install (first time):
  pip install pandas numpy matplotlib rasterio --break-system-packages

Run:
  python week6_add_geographic_infrastructure.py

Output:
  - Updated panel CSV with new infrastructure columns
  - 4-panel visualization figures per country (2020)
  - Regression comparison tables
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import rasterio

# ============================================================================
# USER CONFIG - EDIT THESE PATHS
# ============================================================================

PANEL_PATH = r"C:\Users\BOUCHRA\Desktop\stats201_project\Week6_outputs_tiles\tiles_panel_all_countries_2014-2023.csv"
IMAGES_ROOT = r"C:\Users\BOUCHRA\Desktop\stats201_project\STATS201_Week5_outputs"
OUTPUT_DIR = r"C:\Users\BOUCHRA\Desktop\stats201_project\Week6_outputs_tiles\geographic_infrastructure"

COUNTRIES = ["Morocco", "Brazil", "China"]
DEMO_YEAR = 2020  # Year to create visualization figures
URBAN_DENSITY_RADIUS = 100  # pixels


# ============================================================================
# Helper Functions
# ============================================================================

def ensure_dir(p):
    """Create directory if it doesn't exist"""
    p = Path(p)
    p.mkdir(parents=True, exist_ok=True)
    return p


def compute_infrastructure_features(df_country_year):
    """
    Compute geographic infrastructure features for one country-year
    
    Returns DataFrame with added columns:
      - center_r, center_c: tile centers
      - distance_to_urban_core: pixels to nearest urban tile
      - local_urban_density: count of urban tiles within radius
      - centrality_score: 0-1 score based on distance to country center
    """
    df = df_country_year.copy()
    
    # Compute tile centers
    df['center_r'] = (df['r0'] + df['r1']) / 2
    df['center_c'] = (df['c0'] + df['c1']) / 2
    
    # 1. Distance to nearest urban_core tile
    urban_tiles = df[df['region_type'] == 'urban_core']
    
    distances = []
    for idx, tile in df.iterrows():
        if tile['region_type'] == 'urban_core':
            distances.append(0.0)
        elif len(urban_tiles) == 0:
            distances.append(np.nan)
        else:
            # Compute distance to each urban tile
            urban_centers = urban_tiles[['center_r', 'center_c']].values
            tile_pos = np.array([tile['center_r'], tile['center_c']])
            dists = np.sqrt(((urban_centers - tile_pos)**2).sum(axis=1))
            distances.append(float(dists.min()))
    
    df['distance_to_urban_core'] = distances
    
    # 2. Local urban density (count of urban tiles within radius)
    all_positions = df[['center_r', 'center_c']].values
    is_urban = (df['region_type'] == 'urban_core').values
    
    urban_density = []
    for idx, tile in df.iterrows():
        tile_pos = np.array([tile['center_r'], tile['center_c']])
        dists = np.sqrt(((all_positions - tile_pos)**2).sum(axis=1))
        nearby_urban = (dists < URBAN_DENSITY_RADIUS) & is_urban
        urban_density.append(int(nearby_urban.sum()))
    
    df['local_urban_density'] = urban_density
    
    # 3. Centrality score (based on distance to geographic center)
    center_r = df['center_r'].mean()
    center_c = df['center_c'].mean()
    
    df['distance_to_center'] = np.sqrt(
        (df['center_r'] - center_r)**2 + 
        (df['center_c'] - center_c)**2
    )
    
    # Normalize to 0-1 score (closer to center = higher score)
    max_dist = df['distance_to_center'].max()
    if max_dist > 0:
        df['centrality_score'] = 1.0 - (df['distance_to_center'] / max_dist)
    else:
        df['centrality_score'] = 1.0
    
    # Add log-transformed versions for regression
    df['log_distance_to_urban'] = np.log1p(df['distance_to_urban_core'])
    df['log_local_urban_density'] = np.log1p(df['local_urban_density'])
    
    return df


def create_infrastructure_maps(country, year, tiles_df, tif_path, output_path):
    """
    Create 4-panel visualization: lights + 3 infrastructure measures
    """
    print(f"  Creating visualization for {country} {year}...")
    
    # Load nightlights
    with rasterio.open(tif_path) as src:
        h, w = src.height, src.width
        nl = src.read(1)
    
    # Initialize maps
    distance_map = np.full((h, w), np.nan, dtype=float)
    density_map = np.full((h, w), np.nan, dtype=float)
    centrality_map = np.full((h, w), np.nan, dtype=float)
    
    # Fill maps from tiles
    for _, tile in tiles_df.iterrows():
        r0, r1 = int(tile['r0']), int(tile['r1'])
        c0, c1 = int(tile['c0']), int(tile['c1'])
        
        distance_map[r0:r1, c0:c1] = tile['distance_to_urban_core']
        density_map[r0:r1, c0:c1] = tile['local_urban_density']
        centrality_map[r0:r1, c0:c1] = tile['centrality_score']
    
    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # 1. Nightlights
    nl_valid = nl[np.isfinite(nl)]
    if len(nl_valid) > 0:
        nl_clip = np.clip(nl, 0, np.percentile(nl_valid, 99))
    else:
        nl_clip = nl
    
    axes[0, 0].imshow(nl_clip, cmap='hot', aspect='auto')
    axes[0, 0].set_title(f'{country} {year}: Nightlights', 
                         fontsize=13, fontweight='bold')
    axes[0, 0].axis('off')
    
    # 2. Distance to urban
    im1 = axes[0, 1].imshow(distance_map, cmap='viridis_r', aspect='auto')
    axes[0, 1].set_title('Distance to Urban Core\n(Darker = closer to cities)', 
                         fontsize=13, fontweight='bold')
    axes[0, 1].axis('off')
    cbar1 = plt.colorbar(im1, ax=axes[0, 1], fraction=0.046)
    cbar1.set_label('Pixels', fontsize=10)
    
    # 3. Local urban density
    im2 = axes[1, 0].imshow(density_map, cmap='YlOrRd', aspect='auto')
    axes[1, 0].set_title('Local Urban Density\n(Brighter = more urban neighbors)', 
                         fontsize=13, fontweight='bold')
    axes[1, 0].axis('off')
    cbar2 = plt.colorbar(im2, ax=axes[1, 0], fraction=0.046)
    cbar2.set_label('# Urban tiles', fontsize=10)
    
    # 4. Centrality
    im3 = axes[1, 1].imshow(centrality_map, cmap='plasma', aspect='auto')
    axes[1, 1].set_title('Geographic Centrality\n(Brighter = more central)', 
                         fontsize=13, fontweight='bold')
    axes[1, 1].axis('off')
    cbar3 = plt.colorbar(im3, ax=axes[1, 1], fraction=0.046)
    cbar3.set_label('Score (0-1)', fontsize=10)
    
    plt.suptitle(f'{country} {year}: Geographic Infrastructure Accessibility', 
                 fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close(fig)
    
    print(f"  ✓ Saved: {output_path.name}")


def run_regression_comparison(tiles_df, country, year, output_path):
    """
    Compare regression models with infrastructure features
    """
    try:
        from statsmodels.formula.api import ols
    except ImportError:
        print("  [SKIP] statsmodels not installed, skipping regression")
        return
    
    # Check required columns
    required = ['log_light', 'log_pop', 'log_distance_to_urban', 
                'log_local_urban_density', 'centrality_score']
    if not all(col in tiles_df.columns for col in required):
        print("  [SKIP] Missing required columns for regression")
        return
    
    print(f"  Running regression comparison for {country} {year}...")
    
    # Fit models
    m1 = ols('log_light ~ log_pop', data=tiles_df).fit()
    m2 = ols('log_light ~ log_pop + log_distance_to_urban', data=tiles_df).fit()
    m3 = ols('log_light ~ log_pop + log_local_urban_density', data=tiles_df).fit()
    m4 = ols('log_light ~ log_pop + centrality_score', data=tiles_df).fit()
    m5 = ols('log_light ~ log_pop + log_distance_to_urban + log_local_urban_density', 
             data=tiles_df).fit()
    
    # Create comparison table
    results = pd.DataFrame({
        'Model': [
            '1. Pop only',
            '2. Pop + Distance to urban',
            '3. Pop + Local urban density',
            '4. Pop + Centrality',
            '5. Pop + Distance + Density'
        ],
        'R²': [m1.rsquared, m2.rsquared, m3.rsquared, m4.rsquared, m5.rsquared],
        'Adj_R²': [m1.rsquared_adj, m2.rsquared_adj, m3.rsquared_adj, 
                   m4.rsquared_adj, m5.rsquared_adj],
        'ΔR²_vs_Pop': [
            0.0,
            m2.rsquared - m1.rsquared,
            m3.rsquared - m1.rsquared,
            m4.rsquared - m1.rsquared,
            m5.rsquared - m1.rsquared
        ],
        'N_obs': [int(m1.nobs), int(m2.nobs), int(m3.nobs), int(m4.nobs), int(m5.nobs)]
    })
    
    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_path, index=False, float_format='%.4f')
    
    print(f"  ✓ Saved: {output_path.name}")
    print("\n  Regression Results:")
    print(results.to_string(index=False))
    print()


# ============================================================================
# Main Processing
# ============================================================================

def main():
    print("="*80)
    print("Adding Geographic Infrastructure Features to Tiles Panel")
    print("="*80)
    
    # Setup
    output_dir = ensure_dir(OUTPUT_DIR)
    
    # Load panel
    print(f"\n[1/4] Loading panel: {PANEL_PATH}")
    panel = pd.read_csv(PANEL_PATH)
    print(f"  Loaded {len(panel):,} rows")
    
    # Verify required columns
    required_cols = ['country', 'year', 'r0', 'r1', 'c0', 'c1', 'region_type']
    missing = [col for col in required_cols if col not in panel.columns]
    if missing:
        raise ValueError(f"Panel missing required columns: {missing}")
    
    # Initialize new columns
    new_cols = [
        'center_r', 'center_c',
        'distance_to_urban_core', 'log_distance_to_urban',
        'local_urban_density', 'log_local_urban_density',
        'distance_to_center', 'centrality_score'
    ]
    for col in new_cols:
        if col not in panel.columns:
            panel[col] = np.nan
    
    # Process each country-year
    print(f"\n[2/4] Computing infrastructure features...")
    
    total_processed = 0
    
    for country in COUNTRIES:
        print(f"\n{'─'*80}")
        print(f"Country: {country}")
        print(f"{'─'*80}")
        
        country_mask = panel['country'] == country
        country_years = sorted(panel.loc[country_mask, 'year'].dropna().unique())
        
        if len(country_years) == 0:
            print(f"  No data for {country}, skipping...")
            continue
        
        print(f"  Processing {len(country_years)} years: {country_years[0]}-{country_years[-1]}")
        
        for year in country_years:
            year = int(year)
            
            # Get subset for this country-year
            mask = (panel['country'] == country) & (panel['year'] == year)
            idx = panel.index[mask]
            
            if len(idx) == 0:
                continue
            
            df_subset = panel.loc[idx].copy()
            
            # Compute features
            df_enhanced = compute_infrastructure_features(df_subset)
            
            # Update panel
            for col in new_cols:
                panel.loc[idx, col] = df_enhanced[col].values
            
            total_processed += len(idx)
            
            # Summary stats
            mean_dist = df_enhanced['distance_to_urban_core'].mean()
            mean_dens = df_enhanced['local_urban_density'].mean()
            
            print(f"    {year}: {len(idx):,} tiles | "
                  f"dist_to_urban={mean_dist:.1f} | "
                  f"urban_density={mean_dens:.1f}")
    
    print(f"\n  ✓ Processed {total_processed:,} total tile-years")
    
    # Save updated panel
    print(f"\n[3/4] Saving updated panel...")
    output_panel_path = Path(PANEL_PATH).with_name(
        Path(PANEL_PATH).stem + "_WITH_GEO_INFRASTRUCTURE.csv"
    )
    panel.to_csv(output_panel_path, index=False)
    print(f"  ✓ Saved: {output_panel_path}")
    print(f"  Size: {len(panel):,} rows × {len(panel.columns)} columns")
    
    # Create visualizations and regressions for demo year
    print(f"\n[4/4] Creating visualizations and regressions (year={DEMO_YEAR})...")
    
    for country in COUNTRIES:
        print(f"\n  {country}:")
        
        # Get data for demo year
        mask = (panel['country'] == country) & (panel['year'] == DEMO_YEAR)
        df_demo = panel.loc[mask].copy()
        
        if len(df_demo) == 0:
            print(f"    No data for {DEMO_YEAR}, skipping...")
            continue
        
        # Find TIF path
        tif_path = Path(IMAGES_ROOT) / country / f"{country}_{DEMO_YEAR}.tif"
        if not tif_path.exists():
            print(f"    TIF not found: {tif_path.name}, skipping...")
            continue
        
        # Create visualization
        fig_path = output_dir / f"figure_infrastructure_{country}_{DEMO_YEAR}.png"
        create_infrastructure_maps(country, DEMO_YEAR, df_demo, tif_path, fig_path)
        
        # Run regression comparison
        reg_path = output_dir / f"regression_compare_{country}_{DEMO_YEAR}.csv"
        run_regression_comparison(df_demo, country, DEMO_YEAR, reg_path)
    
    # Final summary
    print("\n" + "="*80)
    print("COMPLETE ✓")
    print("="*80)
    print(f"\nOutputs:")
    print(f"  1. Updated panel: {output_panel_path.name}")
    print(f"  2. Figures: {output_dir / 'figure_infrastructure_*.png'}")
    print(f"  3. Regressions: {output_dir / 'regression_compare_*.csv'}")
    print(f"\nNew columns added:")
    for col in new_cols:
        print(f"  - {col}")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("\nIf you see import errors, install dependencies:")
        print("  pip install pandas numpy matplotlib rasterio --break-system-packages")
