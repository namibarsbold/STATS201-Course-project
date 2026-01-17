# STATS201-Course-project
Question: Can Changes in Nighttime Satellite Images Reveal Energy Insecurity
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

For Week 2, I used only country-level annual summaries (2022–2024) derived in Google Earth Engine.

### Initial Exploratory Analysis
I compute three features per country–year:
- mean nighttime radiance
- within-country spatial variability
- total summed radiance

Exploratory analysis shows strong cross-country heterogeneity and a weakly structured relationship between average brightness and spatial variability, motivating a feature-based machine learning approach.

### Status
Week 2 focuses on data construction, initial exploratory analysis, and ML task definition. 
Monthly country–month csv file data have been generated for use in later stages.


👥 Authors: Nami Barsbold Bouchra Daddaoui Amanda Gonzalez Mejia
