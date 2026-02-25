import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

# =====================================================
# 1. HARD-CODED EXPORT DIRECTORY (as requested)
# =====================================================
OUTPUT_PATH = r"C:\Users\amimi\OneDrive - Duke University\SCHOOL\SPRING 2026\STATS201\Week 6 Files\STATS201-Course-project\figures\week7_outputs"
INPUT_PATH  = r"C:\Users\amimi\OneDrive - Duke University\SCHOOL\SPRING 2026\STATS201\Week 6 Files\STATS201-Course-project\figures\week6_outputs"

os.makedirs(OUTPUT_PATH, exist_ok=True)

COUNTRIES = ["Brazil", "China", "Morocco"]
TARGET_YEAR = 2023

REGIME_ORDER = ["empty_or_rural", "mixed", "bright_sparse", "dense_dim", "urban_core"]

REGIME_PALETTE = {
    "empty_or_rural": "#7f7f7f",  # gray
    "mixed":          "#bcbd22",  # olive
    "bright_sparse":  "#ff7f0e",  # orange
    "dense_dim":      "#1f77b4",  # blue
    "urban_core":     "#d62728",  # red
}

print(f"🚀 Generating 2023 Scatter Plots...\n")

for country in COUNTRIES:

    file_path = os.path.join(INPUT_PATH, f"tiles_{country}_{TARGET_YEAR}.csv")

    if not os.path.exists(file_path):
        print(f"⚠️ Missing file for {country}")
        continue

    df = pd.read_csv(file_path)

    pop_col = "sum_pop" if "sum_pop" in df.columns else "mean_pop"
    df["log_pop"] = np.log1p(df[pop_col])
    df["log_light"] = np.log1p(df["mean_light"])
    df["region_type"] = df["region_type"].astype(str)

    df = df[df["region_type"].isin(REGIME_ORDER)].copy()

    plt.figure(figsize=(11.5, 8))

    # More saturated, high-contrast colors
    REGIME_PALETTE = {
        "empty_or_rural": "#4d4d4d",   # darker gray
        "mixed":          "#8c6bb1",   # purple
        "bright_sparse":  "#ff8c00",   # strong orange
        "dense_dim":      "#0072b2",   # vivid blue
        "urban_core":     "#d40000",   # intense red
    }

    sns.scatterplot(
        data=df,
        x="log_pop",
        y="log_light",
        hue="region_type",
        hue_order=REGIME_ORDER,
        palette=REGIME_PALETTE,
        alpha=0.60,          # MUCH less transparency
        s=28,                # Larger points
        edgecolor="white",   # Slight border to separate dense areas
        linewidth=0.2
    )

    sns.regplot(
        data=df,
        x="log_pop",
        y="log_light",
        scatter=False,
        color="black",
        line_kws={"linestyle": "--", "linewidth": 2.5}
    )

    plt.title(
        f"Population vs. Nighttime Lights\n{country} ({TARGET_YEAR})",
        fontsize=15,
        pad=12
    )
    plt.xlabel("Log(1 + Population)", fontsize=13)
    plt.ylabel("Log(1 + Nighttime Lights)", fontsize=13)

    # Cleaner legend labels
    label_map = {
        "empty_or_rural": "Empty / Rural",
        "mixed": "Mixed",
        "bright_sparse": "Bright Sparse",
        "dense_dim": "Dense-Intermediate",
        "urban_core": "Urban Core",
    }

    handles, labels = plt.gca().get_legend_handles_labels()
    if labels and labels[0] == "region_type":
        handles = handles[1:]
        labels = labels[1:]
    labels = [label_map.get(l, l) for l in labels]

    plt.legend(
        handles,
        labels,
        title="Development Regime",
        title_fontsize=13,
        fontsize=12,              # Larger legend text
        markerscale=1.5,          # Larger legend markers
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
        frameon=True
    )

    plt.grid(False)  # cleaner publication style
    plt.tight_layout()

    output_file = os.path.join(
        OUTPUT_PATH,
        f"scatter_{country}_{TARGET_YEAR}.png"
    )

    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"✅ Saved to: {output_file}")

print("\n✔ All 2023 scatterplots exported to week7_outputs.")