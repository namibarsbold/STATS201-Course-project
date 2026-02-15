import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# ==========================================
# 1. SETUP
# ==========================================
BASE_PATH = r"C:\Users\amimi\OneDrive - Duke University\SCHOOL\SPRING 2026\STATS201\Week 6 Files\STATS201-Course-project\figures\week6_outputs"
COUNTRIES = ["Brazil", "China", "Morocco"]
YEARS = range(2014, 2024)

print("🚀 Analyzing Structural Evolution (Region Shares)...")

all_data = []

# ==========================================
# 2. AGGREGATE DATA
# ==========================================
for country in COUNTRIES:
    for year in YEARS:
        filename = f"tiles_{country}_{year}.csv"
        file_path = os.path.join(BASE_PATH, filename)
        
        if not os.path.exists(file_path):
            continue
            
        df = pd.read_csv(file_path)
        
        # Count tiles per region type
        if 'region_type' in df.columns:
            counts = df['region_type'].value_counts(normalize=True).reset_index()
            counts.columns = ['Region', 'Share']
            counts['Country'] = country
            counts['Year'] = year
            all_data.append(counts)

# Combine into one DataFrame
share_df = pd.concat(all_data, ignore_index=True)

# ==========================================
# 3. VISUALIZE (Stacked Area Chart)
# ==========================================
# We create a separate chart for each country
for country in COUNTRIES:
    country_data = share_df[share_df['Country'] == country]
    
    # Pivot for plotting: Rows=Year, Cols=Region, Values=Share
    pivot_df = country_data.pivot(index='Year', columns='Region', values='Share').fillna(0)
    
    # Sort columns for consistency (Urban at bottom, Rural at top usually looks best)
    # Adjust this order based on your specific region names
    desired_order = ['urban_core', 'mixed', 'dense_dim', 'bright_sparse', 'empty_or_rural']
    # Filter to keep only columns that actually exist in the data
    existing_order = [r for r in desired_order if r in pivot_df.columns]
    pivot_df = pivot_df[existing_order]

    plt.figure(figsize=(10, 6))
    
    # Stackplot
    plt.stackplot(pivot_df.index, pivot_df.T, labels=pivot_df.columns, alpha=0.8, cmap='viridis')
    
    plt.title(f"Structural Evolution: Region Shares Over Time\n{country} (2014-2023)")
    plt.xlabel("Year")
    plt.ylabel("Share of Total Land Area (Tiles)")
    plt.margins(0, 0) # Removes white space on sides
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Region Type")
    plt.tight_layout()
    
    output_name = f"structure_evolution_{country}.png"
    plt.savefig(output_name, dpi=300)
    print(f"✅ Saved chart: {output_name}")
    plt.show()