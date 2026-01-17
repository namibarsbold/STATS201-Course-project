# STATS201-Course-project
Satellite-derived nighttime lights have become a widely used proxy for electricity access and energy system performance in the Global South, where administrative and survey-based data are often incomplete or unreliable. Recent peer-reviewed studies show that brightness levels and temporal changes in nighttime lights are strongly associated with household electrification, grid expansion, and large-scale disruptions to electricity supply (Zhao et al. 2021; Chen et al. 2022). Building on earlier work that linked nightlights to economic activity, newer research increasingly emphasizes temporal variability in brightness as a signal of electricity reliability rather than access alone, particularly in low- and middle-income countries (Gibson et al. 2023).


Project Question: Can Changes in Nighttime Satellite Images Reveal Energy Insecurity?

Tasks:
Clearly stated research question and ML task

Dataset description and feasibility assessment

Initial exploratory analysis

Explicit division of responsibilities within the group

GitHub repository with a clear README and early commits

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
validate feature construction
inspect distributions and outliers
confirm feasibility for classification

In later stages, monthly country–month VIIRS data will be used to construct country-level time-series features capturing temporal variability and persistence. These features will be used in a supervised binary classification framework, with a secondary regression task used for robustness.

### Status
Week 2 focuses on data construction, exploratory analysis, and ML task definition.  
Monthly country–month data have been generated and will be used in subsequent weeks.


Authors: Nami, Bouchra, Amanda 
