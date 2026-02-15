import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

# ==========================================
# 1. SETUP
# ==========================================
# Update this path if needed, just like the previous script
BASE_PATH = r"C:\Users\amimi\OneDrive - Duke University\SCHOOL\SPRING 2026\STATS201\Week 6 Files\STATS201-Course-project\figures\week6_outputs"

COUNTRIES = ["Brazil", "China", "Morocco"]
TARGET_YEAR = 2023  # The plan specifies 2023 as the main result

# ==========================================
# 2. GENERATE SCATTER PLOTS (Step 4 of Plan)
# ==========================================
print(f"🚀 Generating Baseline Scatter Plots for {TARGET_YEAR}...\n")

for country in COUNTRIES:
    filename = f"tiles_{country}_{TARGET_YEAR}.csv"
    file_path = os.path.join(BASE_PATH, filename)
    
    if not os.path.exists(file_path):
        print(f"⚠️ Skipping {country}: File not found for {TARGET_YEAR}")
        continue

    # Load & Transform
    df = pd.read_csv(file_path)
    
    # Handle pop column name difference
    pop_col = 'sum_pop' if 'sum_pop' in df.columns else 'mean_pop'
    
    df['log_pop'] = np.log1p(df[pop_col])
    df['log_light'] = np.log1p(df['mean_light'])
    
    # Create the Plot
    plt.figure(figsize=(10, 7))
    
    # We use a scatter plot with transparency (alpha) so we can see density
    sns.scatterplot(
        data=df, 
        x='log_pop', 
        y='log_light', 
        hue='region_type',  # Color by Region (Urban/Rural)
        alpha=0.3,          # Make dots transparent
        palette='viridis',  # Color scheme
        s=15                # Dot size
    )
    
    # Add a global regression line (The "Baseline Fit")
    sns.regplot(
        data=df, 
        x='log_pop', 
        y='log_light', 
        scatter=False, 
        color='red', 
        line_kws={"linestyle": "--", "label": "Global Trend"}
    )

    plt.title(f"Baseline Relationship: Population vs. Light\n{country} ({TARGET_YEAR})")
    plt.xlabel("Log(Population)")
    plt.ylabel("Log(Nighttime Lights)")
    plt.legend(title="Region Type", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the file for your presentation
    output_name = f"scatter_{country}_{TARGET_YEAR}.png"
    plt.savefig(output_name, dpi=300)
    print(f"✅ Saved chart: {output_name}")
    plt.show()