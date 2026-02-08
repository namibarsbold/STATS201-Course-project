# STATS201-Course-project
Satellite-derived nighttime lights have become a widely used proxy for electricity access and energy system performance in the Global South, where administrative and survey-based data are often incomplete or unreliable (Pei et al. 2025, Dong et al. 2025). Recent peer-reviewed studies show that brightness levels and temporal changes in nighttime lights are strongly associated with household electrification, grid expansion, and large-scale disruptions to electricity supply (Bhattarai et al. 2023; Zhou et al. 2015). Building on earlier work linking nightlights to economic activity, newer research emphasizes temporal variability in brightness as an indicator of electricity reliability rather than access alone, particularly in low- and middle-income countries (Masud Ali et al. 2024).

Most existing studies focus on estimating electricity access levels or tracking long-run electrification progress. Fewer papers examine whether patterns in nightlight variability over time can be used to distinguish broadly stable from unstable electricity systems in a comparative, cross-country framework. This project builds on the established use of nighttime lights as an energy proxy while addressing this gap. Specifically, we ask whether patterns in nighttime satellite images can distinguish countries with relatively stable versus variable electricity-related lighting over time. We analyze monthly nighttime satellite imagery to construct country-level time series of light intensity and extract summary measures of temporal variability. Using a binary classification framework, we assess whether these patterns differ systematically across countries, without attributing observed differences to specific causes.


## Week 5 :  Robustness and sensitivity checks

Image-Based Feature Engineering

This week focuses on incorporating satellite image data as a robustness check and diagnostic tool for the project. Using VIIRS nighttime light imagery, we construct a set of image-based features at the country level and evaluate their behavior relative to existing instability measures.

The notebook in scripts/ processes nighttime light images for Three different Countries: 

Morocco (small–medium country with concentrated nightlight patterns), Brazil (large country with strong regional heterogeneity), China (very large country with high-density and saturated nightlight cores)

Applying country masks to isolate national boundaries

Computing average and total light intensity measures

Normalizing intensity by country size to improve comparability

Visualizing nighttime light distributions and spatial patterns

This analysis serves as a robustness and diagnostic check, testing whether image-derived features add information beyond autoregressive instability measures. The workflow is fully reproducible, with all cells executed and outputs displayed, and is designed to be easily extended to additional countries.

## Week 4: Temporal Features, Forecasting, and Model Comparison

### Objective

Week 4 extends the baseline analysis by addressing key limitations identified in Week 3, particularly label circularity and the lack of temporal structure. The goal is to reformulate the task as a forecasting problem and to evaluate whether richer temporal representations of nighttime lights improve predictive performance.

### Data and Feature Engineering

We construct a monthly country-level panel using VIIRS nighttime lights data accessed through Google Earth Engine. Monthly radiance values are aggregated into yearly country-level features, including mean, standard deviation, minimum, maximum, and range of monthly brightness. These features summarize both average illumination levels and temporal volatility within a year.

To avoid circularity, labels are defined using *next-year* volatility: features are computed from Year *t*, while the binary outcome indicates whether volatility in Year *t+1* exceeds the sample median. This transforms the task from descriptive classification into a genuine one-year-ahead forecasting problem.

### Model Comparison and Controlled Experiments

We compare Logistic Regression and Random Forest classifiers to evaluate the role of model flexibility in capturing instability patterns. Logistic Regression serves as a linear baseline, while Random Forest allows for non-linear interactions and threshold effects.

Controlled experiments are conducted using incrementally expanded feature sets:
- Minimal temporal summaries (mean and standard deviation)
- Temporal summaries plus extrema and range
- Optional spatial heterogeneity measures
- Optional external infrastructure covariates

All models are evaluated using a stratified 70/30 train–test split, with performance assessed via accuracy and class-specific F1 scores, focusing on the unstable class.

### Key Findings

Random Forest models consistently outperform Logistic Regression, particularly when extreme and range-based temporal features are included. Performance gains are driven primarily by volatility-related features rather than average brightness levels. External infrastructure covariates do not materially improve performance beyond satellite-derived features. These results suggest that fluctuations in nighttime illumination provide a meaningful early-warning signal for future electricity grid instability.

### Status

Weeks 4 establish a complete modeling pipeline for forecasting electricity grid instability using satellite-derived nighttime lights. The project now includes monthly data aggregation, temporally informed feature engineering, a non-circular label definition based on next-year volatility, and systematic model comparison through controlled experiments. Results indicate that temporal variability and extreme fluctuations in nighttime lights are more informative than static brightness levels, providing a strong foundation for further validation and extension.


Authors: Nami, Bouchra, Amanda 
