import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import os

# ==========================================
# 1. SETUP
# ==========================================
# Finds the folder relative to where this script is saved
current_dir = os.getcwd()
BASE_PATH = os.path.join(current_dir, 'figures', 'week6_outputs')

print(f"📂 Looking for data in: {BASE_PATH}")

# ==========================================
# 2. THE REGRESSION LOOP (Baseline Model)
# ==========================================
# Make sure capitalization matches your files (e.g., "Brazil" or "brazil")
COUNTRIES = ["Brazil", "China", "Morocco"] 
YEARS = range(2014, 2024) 

results_log = []

for country in COUNTRIES:
    for year in YEARS:
        filename = f"tiles_{country}_{year}.csv"
        file_path = os.path.join(BASE_PATH, filename)
        
        # Skip if file doesn't exist
        if not os.path.exists(file_path):
            continue 
            
        # Load Data
        df = pd.read_csv(file_path)
        
        # --- CLEANING ---
        # Handle 'sum_pop' vs 'mean_pop'
        if 'sum_pop' in df.columns:
            pop_col = 'sum_pop'
        elif 'mean_pop' in df.columns:
            pop_col = 'mean_pop'
        else:
            print(f"⚠️ Skipping {country} {year}: No population column found.")
            continue

        # Log Transforms (Crucial)
        df['log_pop'] = np.log1p(df[pop_col])
        df['log_light'] = np.log1p(df['mean_light'])
        
        # Ensure Region is Categorical
        if 'region_type' in df.columns:
            df['region_type'] = df['region_type'].astype('category')
        else:
            print(f"⚠️ Skipping {country} {year}: No region_type column found.")
            continue

        # --- RUN BASELINE MODEL (No Roads) ---
        # Formula: Light ~ Pop + Region + (Pop * Region)
        formula = "log_light ~ log_pop + C(region_type) + log_pop:C(region_type)"
        
        try:
            model = smf.ols(formula=formula, data=df).fit()
            
            # Save Results
            results_log.append({
                'Country': country,
                'Year': year,
                'R2': model.rsquared,
                'Beta (Pop)': model.params['log_pop'],
                # We removed Theta (Roads) for now
                'Intercept': model.params['Intercept']
            })
            print(f"✅ {country} {year}: R²={model.rsquared:.3f}")
            
        except Exception as e:
            print(f"❌ Error on {country} {year}: {e}")

# ==========================================
# 3. SAVE RESULTS
# ==========================================
if results_log:
    results_df = pd.DataFrame(results_log)
    results_df.to_csv("regression_results_baseline.csv", index=False)
    print("\n💾 Saved baseline results to 'regression_results_baseline.csv'")
    print(results_df.head())
else:
    print("\n⚠️ No results were generated. Check your file paths/names!")