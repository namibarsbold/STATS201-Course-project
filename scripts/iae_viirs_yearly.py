import pandas as pd
import matplotlib.pyplot as plt

# Load data 
df = pd.read_csv("viirs_country_panel_v22.csv")

print("Head:")
print(df.head())
print("\nInfo:")
print(df.info())

# slecting only some collumns 
df = df[["country", "year", "mean_rad", "sd_rad", "sum_rad"]]

# Drop missing values in key variables
before = df.shape[0]
df = df.dropna(subset=["mean_rad", "sd_rad"])
after = df.shape[0]
print(f"\nDropped {before-after} rows with missing mean_rad/sd_rad. Remaining: {after}")

# Coverage check
print("\nYears in dataset:", sorted(df["year"].unique()))
print("Number of countries:", df["country"].nunique())

# Summary statistics (IAE A1)
print("\nSummary stats:")
print(df[["mean_rad", "sd_rad", "sum_rad"]].describe())

# Figure 1: Histogram of mean radiance (IAE A2)
plt.figure(figsize=(7,5))
plt.hist(df["mean_rad"], bins=40)
plt.xlabel("Mean Nighttime Radiance (mean_rad)")
plt.ylabel("Number of country-year observations")
plt.title("Distribution of Mean Nighttime Lights (VIIRS)")
plt.tight_layout()
plt.savefig("fig_hist_mean_rad.png", dpi=300)
plt.show()

# Figure 2: Scatter mean vs sd (IAE A3)
plt.figure(figsize=(6,5))
plt.scatter(df["mean_rad"], df["sd_rad"], alpha=0.4)
plt.xlabel("Mean Radiance (mean_rad)")
plt.ylabel("Spatial variability (sd_rad)")
plt.title("Mean vs Variability of Nighttime Lights")
plt.tight_layout()
plt.savefig("fig_scatter_mean_vs_sd.png", dpi=300)
plt.show()

# Extremes (good for interpretation)
top = df.sort_values("mean_rad", ascending=False).head(10)
bottom = df.sort_values("mean_rad", ascending=True).head(10)

print("\nTop 10 brightest country-years:")
print(top[["country", "year", "mean_rad"]])

print("\nTop 10 darkest country-years:")
print(bottom[["country", "year", "mean_rad"]])

# Boxplot of mean_rad by year (log scale)
plt.figure(figsize=(7,5))
df.boxplot(column="mean_rad", by="year")
plt.yscale("log")
plt.title("Mean Nighttime Radiance by Year (log scale)")
plt.suptitle("")  # remove automatic subtitle
plt.xlabel("Year")
plt.ylabel("Mean Radiance")
plt.tight_layout()
plt.savefig("figures/fig_mean_rad_by_year.png", dpi=300)
plt.show()
