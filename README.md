# STATS201-Course-project
Satellite-derived nighttime lights have become a widely used proxy for electricity access and energy system performance in the Global South, where administrative and survey-based data are often incomplete or unreliable (Pei et al. 2025, Dong et al. 2025). Recent peer-reviewed studies show that brightness levels and temporal changes in nighttime lights are strongly associated with household electrification, grid expansion, and large-scale disruptions to electricity supply (Bhattarai et al. 2023; Zhou et al. 2015). Building on earlier work linking nightlights to economic activity, newer research emphasizes temporal variability in brightness as an indicator of electricity reliability rather than access alone, particularly in low- and middle-income countries (Masud Ali et al. 2024).

Most existing studies focus on estimating electricity access levels or tracking long-run electrification progress. Fewer papers examine whether patterns in nightlight variability over time can be used to distinguish broadly stable from unstable electricity systems in a comparative, cross-country framework. This project builds on the established use of nighttime lights as an energy proxy while addressing this gap. Specifically, we ask whether patterns in nighttime satellite images can distinguish countries with relatively stable versus variable electricity-related lighting over time. We analyze monthly nighttime satellite imagery to construct country-level time series of light intensity and extract summary measures of temporal variability. Using a binary classification framework, we assess whether these patterns differ systematically across countries, without attributing observed differences to specific causes.


WEEK 5 REPORT:

Reformulation of the Prediction Task

For our first objective, we critically reassessed grid instability being modeled as a binary outcome (stable vs. unstable), defined using a median split of next-year volatility and risking capturing persistence effects rather than meaningful structural differences in instability dynamics. To address this, we reformulated the prediction task as a multiclass classification problem, defining instability levels using quintiles of next-year volatility. This approach preserves the forecasting structure, features derived from year t and labels defined by outcomes in year t+1, while requiring the model to distinguish between degrees of instability rather than a single threshold crossing.

By predicting five ordered instability categories (very low to very high), the model is no longer rewarded merely for identifying persistent instability. It must learn patterns that differentiate moderate from extreme volatility, providing a stricter and more informative evaluation of the predictive value of nighttime light features. Interpretation of the updated models:

Table 1. Updated Model Comparison

Table 1 and Figure 1 summarize model performance across feature sets and model classes under the multiclass formulation. Performance is evaluated using accuracy, macro F1, weighted F1, and class-specific F1 for the highest volatility category (class 4), which represents the most policy-relevant outcome. Overall performance is lower than in the binary setting, reflecting the increased difficulty of the task. This confirms that the multiclass formulation imposes a more demanding predictive challenge rather than inflating performance through persistence. 

Model performance varies more meaningfully across feature sets. Logistic Regression performs competitively when limited to minimal temporal features, while Random Forest consistently shows superior performance as spatial heterogeneity features are introduced. This pattern suggests that non-linear interactions between temporal volatility and spatial dispersion are informative for distinguishing higher instability levels. External infrastructure covariates again fail to substantially improve performance, indicating that satellite-derived temporal and spatial patterns already encode much of the predictive signal captured by these coarse indicators.

Figure 1. Model Comparison Heatmap

The strongest performance is achieved by the Random Forest model with spatial heterogeneity features (feature set C), indicating that how nighttime light dynamics are represented is more consequential than the inclusion of external covariates. Feature ablations further show that short-horizon electricity instability remains dominated by temporal persistence in light volatility, with lagged instability measures saturating predictive performance across specifications. The limited marginal contribution of infrastructure and access covariates therefore suggests that such variables primarily explain cross-sectional differences in energy development rather than year-to-year transitions, imposing a structural constraint on one-step-ahead forecasting.

Figure 2. Best Model Confusion Matrix

Figure 2 presents the confusion matrix for the best-performing multiclass model. Predictions are most accurate along the diagonal, particularly for the highest volatility categories (classes 3 and 4). Misclassifications occur predominantly between adjacent classes rather than across distant categories, indicating that the model captures the ordinal structure of instability levels. Even when errors occur, the model typically predicts a nearby volatility state rather than confusing stable and highly unstable regimes, suggesting that it learns a graded notion of instability rather than collapsing predictions toward the mean.

Figure 3. Random Forest Feature Importance

Feature importance analysis for the best RF model shows that temporal volatility measures remain the strongest predictors of future instability. In contrast to the binary formulation, spatial dispersion features contribute meaningfully in the multiclass setting. This shift indicates that spatial heterogeneity plays a substantive role in distinguishing degrees of instability once the prediction task moves beyond a binary threshold.

Pixel-Level Spatial Analysis of Nighttime Lights

Given the dominance of temporal persistence in short-horizon prediction, we next ask whether spatial structure offers complementary insight beyond what country-level forecasting can capture. Earlier results relied primarily on temporal autocorrelation, motivating an exploration of whether spatial patterns extracted from satellite imagery encode interpretable structure relevant to electricity instability.

We exported annual GeoTIFF images (2014–2023) combining VIIRS nighttime lights (avg_rad) with population density from the WorldPop Global Population Density dataset (100 m resolution). Each image contains three aligned bands: nighttime radiance, raw population counts, and a normalized population mask. Key challenges included managing heavy-tailed radiance distributions, ensuring spatial consistency across years, and avoiding circularity when incorporating population information.

To capture within-country structure, each country was partitioned into a fixed grid of subregions. For each region, we computed mean and variance of nighttime lights and population density, along with their within-region association. Regions were classified into interpretable typologies (urban cores, dense but dim regions, bright sparse areas, mixed regions, and rural or empty regions) based on joint thresholds of light intensity and population density. We chose Morocco as our case study because it is our lovely teammate Bouchra’s home.
Spatial Structure in Morocco
 
Figure 4. Regional population–nightlight typology for Morocco (2023). Colors represent urban cores, mixed regions, and rural areas, highlighting spatial inequality in development.

Figure 4 illustrates Morocco’s pronounced spatial inequality in 2023. Urban cores (high population, high luminosity) concentrate the vast majority of nighttime light, while rural and empty regions dominate land area but contribute negligible illumination. This polarized structure indicates a development pattern centered on intensifying existing hubs, with persistent “dense but dim” regions highlighting areas where population growth consistently outpaces infrastructure provision.

Figure 5. Total nighttime light mass in Morocco (2014–2023), showing sustained growth driven by increased illumination intensity.

Figure 6. Total Nighttime Lights.

Figure 5 shows that total nighttime light mass increased steadily from 2014 to 2023, reflecting sustained national growth. Figure 6 reveals that this increase is driven by rising radiance within a largely stable lit area rather than spatial expansion. Together, these patterns indicate that Morocco’s development over the past decade has been characterized by electrical densification of established urban centers rather than broad-based electrification of new rural regions.

Table 2. Morocco country–year feature table

The Morocco country–year feature table shows that image-derived temporal and spatial light features are internally consistent but highly persistent over time, with gradual changes in mean intensity and stable dispersion and inequality measures. This stability indicates that the feature set encodes durable spatial structure rather than transient noise, helping explain why short-horizon prediction is saturated by lagged volatility and why additional covariates yield limited marginal gains in robustness checks.

Figure 7. Light Inequality by Population Quintile

Quantile-based segmentation shows extreme concentration of nighttime lights, with the top 20% most populous regions capturing the vast majority of total luminosity. The lower population quintiles (0–60%) remain flat and near zero over time, statistically confirming that large segments of the population persist in relative “light poverty” despite aggregate national growth.

Figure 9. Fixed-Threshold Population Nightlight Typology Over Time

Longitudinal tracking of regional typologies from 2014 to 2023 reveals the structural rigidity of Morocco’s development. The share of regions classified as urban cores remains stable relative to total area, reinforcing the conclusion that growth is vertical (intensification) rather than horizontal (sprawl). The persistence of dense but dim regions provides a concrete metric of structural instability, highlighting areas where demographic pressure consistently exceeds infrastructure capacity.


Authors: Nami, Bouchra, Amanda 
