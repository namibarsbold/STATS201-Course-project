# STATS201-Course-project
Satellite-derived nighttime lights have become a widely used proxy for electricity access and energy system performance in the Global South, where administrative and survey-based data are often incomplete or unreliable (Pei et al. 2025, Dong et al. 2025). Recent peer-reviewed studies show that brightness levels and temporal changes in nighttime lights are strongly associated with household electrification, grid expansion, and large-scale disruptions to electricity supply (Bhattarai et al. 2023; Zhou et al. 2015). Building on earlier work linking nightlights to economic activity, newer research emphasizes temporal variability in brightness as an indicator of electricity reliability rather than access alone, particularly in low- and middle-income countries (Masud Ali et al. 2024).

Most existing studies focus on estimating electricity access levels or tracking long-run electrification progress. Fewer papers examine whether patterns in nightlight variability over time can be used to distinguish broadly stable from unstable electricity systems in a comparative, cross-country framework. This project builds on the established use of nighttime lights as an energy proxy while addressing this gap. Specifically, we ask whether patterns in nighttime satellite images can distinguish countries with relatively stable versus variable electricity-related lighting over time. We analyze monthly nighttime satellite imagery to construct country-level time series of light intensity and extract summary measures of temporal variability. Using a binary classification framework, we assess whether these patterns differ systematically across countries, without attributing observed differences to specific causes.

## Week 3: Baseline Model and Initial Results
### Objective

Week 3 focuses on implementing an initial baseline model to evaluate whether simple satellite-derived features from nighttime lights contain informative signals related to electricity system stability. This stage is intended as a diagnostic benchmark rather than a finalized modeling approach.

### Baseline Model

We implement a supervised binary classification model using logistic regression. Each observation corresponds to a country–year and is represented by two features derived from VIIRS nighttime lights:
- Mean radiance, capturing overall brightness levels
- Spatial variability (standard deviation) of radiance, capturing heterogeneity in nighttime illumination
  
Countries are assigned to a baseline “stable” or “variable” class using a median split on spatial variability, which serves as a latent proxy for electricity stability. These labels are used solely for exploratory classification and do not represent observed ground truth.

### Train/Test Split

The dataset is split into training (70%) and test (30%) sets using a stratified random split to preserve class balance across subsets. This hold-out validation framework allows model performance to be evaluated on unseen observations while remaining simple and interpretable for a baseline analysis.

### Evaluation Strategy

Model performance is evaluated using overall classification accuracy as the primary metric, supplemented by a confusion matrix to examine class-specific prediction patterns. This evaluation strategy is appropriate for a binary classification task with balanced classes and provides a transparent reference point for future model comparisons.

### Initial Results

The baseline logistic regression model achieves an accuracy of approximately 86% on the held-out test set. Visualization of the feature space indicates that spatial variability in nighttime radiance provides clearer separation between classes than mean radiance alone. The confusion matrix shows that the model performs better at identifying relatively stable countries, while misclassification occurs more frequently among variable countries.

### Interpretation and Next Steps

These results suggest that even simplified spatial summaries of nighttime lights contain meaningful information related to electricity system stability. At the same time, the asymmetry in classification performance highlights the heterogeneous nature of energy instability and the limitations of static, annual features. In subsequent weeks, the project will incorporate monthly country–month observations and richer temporal features to better capture persistence, volatility, and change in nighttime illumination patterns.

### Status
Week 3 implements an initial baseline classification model and evaluation framework.  
A logistic regression model is used to establish a benchmark for distinguishing energy-stable and energy-variable countries using annual VIIRS-derived features. Results highlight the informativeness of variability-based features and motivate the incorporation of richer temporal representations in subsequent weeks.

Authors: Nami, Bouchra, Amanda 
