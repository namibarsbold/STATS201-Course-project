import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# ==========================================
# 1. SETUP
# ==========================================
# Use the results file you just created in the previous step
csv_path = "regression_results_baseline.csv"

if not os.path.exists(csv_path):
    print("❌ ERROR: Could not find 'regression_results_baseline.csv'. Run the baseline regression first!")
else:
    df = pd.read_csv(csv_path)

    # Filter for the most recent year (2023) for the "Snapshot" comparison
    df_2023 = df[df['Year'] == 2023]

    # ==========================================
    # 2. CREATE COMPARISON BAR CHARTS
    # ==========================================
    sns.set_theme(style="whitegrid")
    
    # FIGURE 1: R-SQUARED COMPARISON (How well does Pop explain Light?)
    plt.figure(figsize=(8, 6))
    sns.barplot(data=df_2023, x='Country', y='R2', palette='viridis')
    plt.title("Model Fit by Country (2023)\n(How much of Nighttime Light is explained by Population?)")
    plt.ylabel("R-Squared (0 to 1)")
    plt.ylim(0, 1) # R2 is always between 0 and 1
    
    for index, row in df_2023.iterrows():
        # Add text labels on the bars
        plt.text(row.name, row.R2 + 0.02, f"{row.R2:.2f}", color='black', ha="center")

    plt.savefig("comparison_r2_2023.png", dpi=300)
    plt.show()

    # FIGURE 2: ELASTICITY COMPARISON (The 'Beta' Coefficient)
    plt.figure(figsize=(8, 6))
    sns.barplot(data=df_2023, x='Country', y='Beta (Pop Elasticity)', palette='magma')
    plt.title("Population Elasticity of Light (2023)\n(1% Pop Increase = X% Light Increase)")
    plt.ylabel("Elasticity Coefficient (Beta)")
    
    plt.savefig("comparison_beta_2023.png", dpi=300)
    plt.show()
    
    print("✅ comparison_r2_2023.png saved!")
    print("✅ comparison_beta_2023.png saved!")