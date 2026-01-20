# STATS201-Course-project
Satellite-derived nighttime lights have become a widely used proxy for electricity access and energy system performance in the Global South, where administrative and survey-based data are often incomplete or unreliable (Pei et al. 2025, Dong et al. 2025). Recent peer-reviewed studies show that brightness levels and temporal changes in nighttime lights are strongly associated with household electrification, grid expansion, and large-scale disruptions to electricity supply (Bhattarai et al. 2023; Zhou et al. 2015). Building on earlier work linking nightlights to economic activity, newer research emphasizes temporal variability in brightness as an indicator of electricity reliability rather than access alone, particularly in low- and middle-income countries (Masud Ali et al. 2024).

Most existing studies focus on estimating electricity access levels or tracking long-run electrification progress. Fewer papers examine whether patterns in nightlight variability over time can be used to distinguish broadly stable from unstable electricity systems in a comparative, cross-country framework. This project builds on the established use of nighttime lights as an energy proxy while addressing this gap. Specifically, we ask whether patterns in nighttime satellite images can distinguish countries with relatively stable versus variable electricity-related lighting over time. We analyze monthly nighttime satellite imagery to construct country-level time series of light intensity and extract summary measures of temporal variability. Using a binary classification framework, we assess whether these patterns differ systematically across countries, without attributing observed differences to specific causes.

Project Question: Can Changes in Nighttime Satellite Images Reveal Energy Insecurity?

This project uses VIIRS Day/Night Band nighttime lights data from NOAA/NASA. 
The data capture nighttime radiance associated with artificial lighting and electricity use. 
Monthly cloud-free composites with global coverage since 2012 are used at ~500 m resolution.
## Week 2 

### Research Question
Can nighttime satellite imagery be used to classify countries as energy-stable or energy-insecure?

### Data
This project uses VIIRS Day/Night Band nighttime lights data provided by NOAA/NASA(2012-2023) 

### Exploratory Analysis
Exploratory analysis focuses on the distribution and scale of extracted features.  
Mean radiance is highly right-skewed, with a small number of very bright country–years and a large mass of low-light observations. Spatial variability also varies widely across countries and is not perfectly aligned with mean brightness.
These patterns confirm strong cross-country heterogeneity and motivate the use of variability-based features rather than average brightness alone.

### Machine Learning Task
The machine learning task of this project is to classify countries as energy-stable or energy-insecure using features derived from nighttime satellite imagery.

For Week 2, no models are trained. The annual dataset is used only to:
- validate feature construction
- inspect distributions and outliers
- confirm feasibility for classification

In later stages, monthly country–month VIIRS data will be used to construct country-level time-series features capturing temporal variability and persistence. These features will be used in a supervised binary classification framework, with a secondary regression task used for robustness.

### Status
Week 2 focuses on data construction, exploratory analysis, and ML task definition.  
Monthly country–month data have been generated and will be used in subsequent weeks.


Authors: Nami, Bouchra, Amanda 
