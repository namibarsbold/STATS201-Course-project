# STATS201-Course-project
Satellite-derived nighttime lights have become a widely used proxy for electricity access and energy system performance in the Global South, where administrative and survey-based data are often incomplete or unreliable (Pei et al. 2025, Dong et al. 2025). Recent peer-reviewed studies show that brightness levels and temporal changes in nighttime lights are strongly associated with household electrification, grid expansion, and large-scale disruptions to electricity supply (Bhattarai et al. 2023; Zhou et al. 2015). Building on earlier work linking nightlights to economic activity, newer research emphasizes temporal variability in brightness as an indicator of electricity reliability rather than access alone, particularly in low- and middle-income countries (Masud Ali et al. 2024).

Most existing studies focus on estimating electricity access levels or tracking long-run electrification progress. Fewer papers examine whether patterns in nightlight variability over time can be used to distinguish broadly stable from unstable electricity systems in a comparative, cross-country framework. This project builds on the established use of nighttime lights as an energy proxy while addressing this gap. Specifically, we ask whether patterns in nighttime satellite images can distinguish countries with relatively stable versus variable electricity-related lighting over time. We analyze monthly nighttime satellite imagery to construct country-level time series of light intensity and extract summary measures of temporal variability. Using a binary classification framework, we assess whether these patterns differ systematically across countries, without attributing observed differences to specific causes.

###Week 6 Updates 
This week consolidates the core statistical framework and completes the spatial data pipeline required for the final project. We finalized the tile-level panel dataset (2014–2023) across Morocco, Brazil, and China (30,442 tile-year observations) and implemented the interaction log–log OLS specification:

log(light) ~ log(population) + region + region × log(population)

The model confirms strong explanatory power (R² ≈ 0.88–0.94 in 2023) and reveals regime-dependent elasticities, including a consistent “Urban Premium.” We documented cross-country differences in population–light coupling and diagnosed structural patterns such as China’s high urban efficiency masked by weaker rural responsiveness. Figures and regression tables were produced to formalize interpretation and prepare presentation-ready outputs.

In parallel, we extended the model beyond demographics by integrating infrastructure structure at the tile level. We engineered spatial accessibility measures (distance to urban core, local urban density, centrality) and incorporated OpenStreetMap road density (km/km²) through geospatial intersection. Accessibility features significantly improve explanatory power (ΔR² ≈ +0.17 in Morocco and China), validating the infrastructure hypothesis. The project now moves from a demographic benchmark to a full infrastructure-augmented spatial regression framework.

Next Steps

Estimate full model:
log(light) ~ log(pop) + road_density + region + interactions

Compare baseline vs. infrastructure-augmented results (ΔR², coefficient stability)

Track coefficient trends from 2014–2023

Produce final cross-country comparison visuals


Authors: Nami, Bouchra, Amanda 
