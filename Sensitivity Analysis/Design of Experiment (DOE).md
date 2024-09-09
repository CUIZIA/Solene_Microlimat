# Sensitivity Analysis using Design of Experiment (DOE)

This document outlines the steps to perform a sensitivity analysis using the **Design of Experiment (DOE)** method to evaluate the impact of four key input parameters on surface temperature. The four input parameters are:

1. **Thermal Conductivity (Conductivite thermique)**
2. **Heat Capacity (Capacite thermique)**
3. **Density (Masse volumique)**
4. **Albedo (Surface Reflectivity)**

## Objective:
The objective of this sensitivity analysis is to assess the relative importance of the four input parameters on the surface temperature, as well as to identify any potential interactions between them.

---

## Steps:

### 1. **Define the Experimental Objective**
The goal of this experiment is to understand the influence of the input parameters on surface temperature. This includes:
- Quantifying the effect of each input parameter on the output.
- Identifying any significant interactions between the input parameters that affect the surface temperature.

### 2. **Select the Experimental Design**
For this analysis, a **full factorial design** is selected. Given that there are 4 input parameters, each with 2 levels (high and low), a full factorial design will require `2^4 = 16` experiments. This approach allows us to capture both main effects and interaction effects between factors.

### 3. **Set the Factor Levels**
The four input parameters will be varied at two levels: a **low level (-1)** and a **high level (+1)**. The baseline values and their respective high and low levels are as follows:

| Factor                       | Low Level (-1)     | High Level (+1)     |
|------------------------------|--------------------|---------------------|
| **Thermal Conductivity**      | 1.0 W/m·K          | 3.0 W/m·K           |
| **Heat Capacity**             | 450 J/kg·K         | 1350 J/kg·K         |
| **Density**                   | 1000 kg/m³         | 3000 kg/m³          |
| **Albedo**                    | 0.2                | 0.6                 |

### 4. **Construct the Full Factorial Design Matrix**
Using a full factorial design, the experiment matrix is constructed as follows, resulting in 16 combinations of factor levels:

| Experiment | Thermal Conductivity | Heat Capacity | Density | Albedo |
|------------|----------------------|---------------|---------|--------|
| 1          | -1                   | -1            | -1      | -1     |
| 2          | +1                   | -1            | -1      | -1     |
| 3          | -1                   | +1            | -1      | -1     |
| 4          | +1                   | +1            | -1      | -1     |
| 5          | -1                   | -1            | +1      | -1     |
| 6          | +1                   | -1            | +1      | -1     |
| 7          | -1                   | +1            | +1      | -1     |
| 8          | +1                   | +1            | +1      | -1     |
| 9          | -1                   | -1            | -1      | +1     |
| 10         | +1                   | -1            | -1      | +1     |
| 11         | -1                   | +1            | -1      | +1     |
| 12         | +1                   | +1            | -1      | +1     |
| 13         | -1                   | -1            | +1      | +1     |
| 14         | +1                   | -1            | +1      | +1     |
| 15         | -1                   | +1            | +1      | +1     |
| 16         | +1                   | +1            | +1      | +1     |

### 5. **Conduct the Simulation or Experiment**
Perform the simulation or experiment for each of the 16 combinations. For each combination of parameters, record the resulting surface temperature. These results will form the basis of the analysis.

### 6. **Analyze the Results**

#### **Main Effects Analysis**
- **Main Effect Plot**: Analyze the main effects of each factor by examining how changes in the levels of each factor impact the surface temperature. A main effect plot can show how much each factor contributes to the changes in temperature.

#### **Interaction Effects Analysis**
- **Interaction Plot**: Analyze potential interactions between the factors. Interaction effects occur when the effect of one factor depends on the level of another factor.

#### **Analysis of Variance (ANOVA)**
- Perform ANOVA to statistically quantify the contributions of each factor and their interactions. ANOVA helps identify which factors and interactions significantly influence the surface temperature.

### 7. **Optimize and Extend (Optional)**
If the analysis reveals non-linear behavior or if further optimization is required, a **Response Surface Methodology (RSM)** can be employed. This method can help optimize the process by fitting a second-order polynomial model to explore non-linear relationships between factors.

### 8. **Conclusion**
The DOE approach allows for a structured and efficient exploration of the sensitivity of surface temperature to the four input parameters. By evaluating both main effects and interaction effects, you can determine which factors are most critical and whether any combinations of factors create significant changes in temperature.
