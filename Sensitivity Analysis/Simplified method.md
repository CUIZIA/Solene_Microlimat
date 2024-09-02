# Solene_Microclimat

## Objective

The goal of this sensitivity analysis is to evaluate the impact of four input parameters on the simulated surface temperature over time. The parameters are:
- Conductivite thermique (Thermal Conductivity)
- Capacite thermique (Heat Capacity)
- Masse volumique (Density)
- Albedo (Surface Reflectivity)

## Steps

**1** Establish a Baseline Model:
- Select a set of baseline values for the four parameters. These should represent reasonable and typical values for the materials or conditions being simulated.
- Run the simulation with these baseline values to generate the baseline temperature profile over time.

**2** Parameter Variation and Simulation:
- Perform four separate simulations, each time modifying only one of the input parameters, while keeping the other three parameters at their baseline values.
- For each simulation, change the selected parameter by increasing and decreasing its baseline value by 50%. This will help assess the sensitivity of the surface temperature to changes in that parameter.

**3** Simulations:
- Simulation 1: Vary Conductivite thermique by ±50% from the baseline.
- Simulation 2: Vary Capacite thermique by ±50% from the baseline.
- Simulation 3: Vary Masse volumique by ±50% from the baseline.
- Simulation 4: Vary Albedo by ±50% from the baseline.

**4** Results Comparison:
- Compare the temperature profiles from each of the four simulations against the baseline profile.
- Analyze how the changes in each parameter affect the surface temperature over time.

**5** Visualization:
- Plot the temperature profiles from all simulations on a single graph, with the baseline temperature profile as a reference.
- Use additional bar charts or other appropriate visualizations to highlight key differences at specific time points (e.g., maximum temperature or time to reach a certain temperature).

**6** Conclusion:
- Identify which parameters have the most significant impact on the surface temperature.
- Discuss any potential interactions or non-linear effects observed during the analysis.
- Based on the findings, recommend any further analysis or adjustments to the simulation parameters.

## Baseline Model Parameters

The baseline parameters for the model are set as follows:
- Conductivite thermique (Thermal Conductivity): 2.0 W/m·K
- Capacite thermique (Heat Capacity): 900 J/kg·K
- Masse volumique (Density): 2300 kg/m³
- Albedo (Surface Reflectivity): 0.4

**1** Variation Range:
Each parameter will be varied within ±50% of its baseline value. The resulting ranges are:
- Thermal Conductivity: 1.0 W/m·K to 3.0 W/m·K
- Heat Capacity: 450 J/kg·K to 1350 J/kg·K
- Density: 1150 kg/m³ to 3450 kg/m³
- Albedo: 0.2 to 0.6

**2** 16-Step Variation Series
For each parameter, a 16-step series is generated, covering the range from -50% to +50%. The series includes 8 values below the baseline and 8 values above. The reason I set it up this way is that the model itself contains 16 study areas, and I can use the model directly for fast simulation (without considering the occlusion of surrounding buildings, each study area enjoys the same weather conditions).

- Thermal Conductivity: [1.0, 1.13, 1.25, 1.38, 1.5, 1.63, 1.75, 1.88,**2.0**, 2.13, 2.25, 2.38, 2.5, 2.63, 2.75, 2.88, 3.0] W/(m·K)
- Heat Capacity: [450, 506.25, 562.5, 618.75, 675, 731.25, 787.5, 843.75,**900**, 956.25, 1012.5, 1068.75, 1125, 1181.25, 1237.5, 1293.75, 1350] J/(kg·K)
- Density: [1000, 1125, 1250, 1375, 1500, 1625, 1750, 1875, **2000**, 2125, 2250, 2375, 2500, 2625, 2750, 2875, 3000]kg/m³
- Albedo: [0.2, 0.225, 0.25, 0.275, 0.3, 0.325, 0.35, 0.375, **0.4**, 0.425, 0.45, 0.475, 0.5, 0.525, 0.55, 0.575, 0.6]
