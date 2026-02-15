import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import numpy as np
import os
import re # Added regex for safer text extraction

# ==========================================
# 1. SETUP
# ==========================================
BASE_PATH = r"C:\Users\amimi\OneDrive - Duke University\SCHOOL\SPRING 2026\STATS201\Week 6 Files\STATS201-Course-project\figures\week6_outputs"
COUNTRIES = ["Brazil", "China", "Morocco"]
YEAR = 2023

print(f"🚀 Calculating Regional Slopes for {YEAR}...\n")

slope_data = []

for country in COUNTRIES:
    filename = f"tiles_{country}_{YEAR}.csv"
    file_path = os.path.join(BASE_PATH, filename)
    
    if not os.path.exists(file_path):
        print(f"⚠️ Skipping {country}: File not found.")
        continue

    # Load & Prep
    df = pd.read_csv(file_path)
    pop_col = 'sum_pop' if 'sum_pop' in df.columns else 'mean_pop'
    df['log_pop'] = np.log1p(df[pop_col])
    df['log_light'] = np.log1p(df['mean_light'])
    
    # Run Model (No Intercept to isolate slopes)
    formula = "log_light ~ log_pop:C(region_type) + C(region_type) - 1"
    
    try:
        model = smf.ols(formula=formula, data=df).fit()
        
        # Extract Coefficients safely
        for term in model.params.index:
            # We only care about the interaction terms (the "Slope" of population)
            if "log_pop:C(region_type)" in term:
                
                # --- ROBUST NAME EXTRACTION ---
                # Pattern: Looks for text inside square brackets []
                # Works for "C(region_type)[T.urban]" AND "C(region_type)[urban]"
                match = re.search(r"\[(.*?)\]", term)
                
                if match:
                    region_raw = match.group(1)
                    # Remove "T." if it exists, otherwise keep the name as is
                    region_name = region_raw.replace("T.", "")
                else:
                    # Fallback if no brackets found
                    region_name = term 
                
                slope_value = model.params[term]
                
                slope_data.append({
                    'Country': country,
                    'Region': region_name,
                    'Elasticity (Slope)': slope_value
                })
        print(f"✅ Processed {country}")
        
    except Exception as e:
        print(f"❌ Error on {country}: {e}")

# ==========================================
# 2. VISUALIZE
# ==========================================
if slope_data:
    slope_df = pd.DataFrame(slope_data)

    plt.figure(figsize=(12, 6))
    
    # Bar Chart of Slopes
    sns.barplot(
        data=slope_df, 
        x='Region', 
        y='Elasticity (Slope)', 
        hue='Country', 
        palette='viridis'
    )

    plt.title(f"Regional Efficiency: Population Elasticity by Region ({YEAR})")
    plt.ylabel("Elasticity (% Light increase per 1% Pop increase)")
    plt.xlabel("Region Type")
    plt.axhline(0, color='black', linewidth=1) 
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.legend(title="Country")
    plt.tight_layout()

    # Save
    output_file = "interaction_slopes_2023.png"
    plt.savefig(output_file, dpi=300)
    print(f"\n🎉 Success! Chart saved to: {output_file}")
    plt.show()
else:
    print("\n⚠️ No data collected. Check if your CSV files are empty or missing columns.")