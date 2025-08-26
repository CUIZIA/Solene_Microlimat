# Case Khalid

This project investigates the thermal and microclimatic performance of permeable pavements under summer weather conditions. The study focuses on **two innovative porous concrete materials** (Hydromedia and Sponge Concrete) and evaluates their capacity to mitigate urban heat through **evaporation-driven cooling** and altered surface energy balance.

&nbsp;

## Simulation Setup

- **Geographical coordinates:** 45°26'34.1"N 4°23'44.9"E
- **3D model:** (illustration will be inserted here)  

The study investigates two types of surface conditions:  
1. An open area with longer solar exposure.  
2. A shaded area located near vegetation with shorter solar exposure.  

<p align="center">
  <img src="/fig/3D Khalid.png" alt="3D model of simlation area" width="50%">
</p>

<p align="center"><b>Figure 1: 3D model of simlation area.</b></p>

&nbsp;

## Simulation Period
- From **2024/08/07 01:00** to **2024/08/11 23:30**  
- **Time step:** 30 minutes

&nbsp;

## Field Measurements
- **Surface temperature / central temperature**: measured in situ (data to be included).  

Two permeable pavement materials are compared:  
- **Hydromedia**  
- **Sponge concrete**

### Hydromedia pavement structure

| Layer       | Thickness (cm) | Thermal conductivity (W/m·K) | Density (kg/m³) | Specific heat (J/kg·K) | Emissivity | Albedo |
|-------------|----------------|------------------------------|-----------------|------------------------|------------|--------|
| Hydromedia  | 13             | 1.172                        | 2530            | 1111                   | 0.88       | 0.31   |
| Gravel      | 5              | 0.8                          | 1700            | 900                    | -          | -      |
| Soil        | 100            | 1.05                         | 2000            | 1000                   | -          | -      |

### Sponge concrete pavement structure

| Layer          | Thickness (cm) | Thermal conductivity (W/m·K) | Density (kg/m³) | Specific heat (J/kg·K) | Emissivity | Albedo |
|----------------|----------------|------------------------------|-----------------|------------------------|------------|--------|
| Sponge concrete| 13             | 1.164                        | 2220            | 1129                   | 0.88       | 0.31   |
| Gravel         | 5              | 0.8                          | 1700            | 900                    | -          | -      |
| Soil           | 100            | 1.05                         | 2000            | 1000                   | -          | -      |

&nbsp;

## Meteorological Forcing (Input Data)
Meteorological data were collected from two stations:  

- **Station de la Purinière**: air temperature (Tair), wind speed, wind direction, relative humidity (HR), precipitation. 45°26'07.0"N 4°22'05.0"E
- **Station de l’aéroport**: atmospheric pressure, global horizontal irradiance (GHI), cloudiness.  

Using these datasets, solar radiation was decomposed into direct and diffuse components following **Black (1956)** and **Muneer et al. (2004)** (details available [here](https://github.com/CUIZIA/Solene_Microlimat/blob/main/simulation_model/Solar%20Radiation.md)).  
Longwave atmospheric radiation was estimated using the **Prata (1996)** formulation.  

&nbsp;

## Evaporation Model (Integrated in `main.py`)
Evaporation removes latent heat and modifies the surface energy balance. Latent heat flux is expressed as:  

$$
R_{latent} = L \cdot E_s
$$  

Where:  
- $L$: Latent heat of vaporization of water (assumed constant, **2260 $kJ \cdot kg^{-1}$**)  
- $E_s$: Surface evapotranspiration rate ( $kg \cdot m^{-2} \cdot s^{-1}$ ), estimated using Khalid’s empirical model.  

### Empirical Formulation of $E_s$
The model relates $E_s$ to the **saturation degree** $S$:  

- If $S \leq S_2$: $E_s(t) = 0$ 
- If $S_2 < S < S_1$: $E_s(t)$ increases linearly with **Slope**  
- If $S \geq S_1$: $E_s(t) = E_1$ (maximum evapotranspiration rate)  

Thus, once **$E_1$**, **Slope**, and **$S_1$** are known, the transition threshold $S_2$ can be derived.  

The following empirical polynomial regressions were obtained (using regression fitting from experimental/DOE data):  

&nbsp;

### Parameter Normalization
Before regression, meteorological inputs are rescaled as:  

$$
T = \frac{T_{air} - 30}{10}, \quad
R = \text{clip}\left(\frac{R_{global} - 146}{135}, -1, 1\right), \quad
HR = \frac{HR - 50}{20}, \quad
V = v_{10m} \cdot \frac{\ln(0.3/0.2)}{\ln(10/0.2)} - 0.8
$$  

Where:  
- $T_{air}$: Air temperature (°C)  
- $R_{global}$: Global solar radiation (W/m²)  
- $HR$: Relative humidity (%)  
- $v_{10m}$: Wind speed measured at 10 m height (adjusted to 0.3 m using logarithmic wind profile, with roughness length = 0.2 m)  

&nbsp;

### Quadratic (Plafonnée) Formulation

#### 1. Formula for $E_1$

$$
\begin{aligned}
E_1(T, R, V, HR) &= 6.164 + 1.664T + 0.381R + 3.383V - 1.995HR \\
&+ 0.234T^2 - 0.148TR + 0.601TV - 0.635THR \\
&+ 0.272R^2 + 0.073RV + 0.577RHR \\
&+ 0.339V^2 - 1.502VHR - 0.068HR^2
\end{aligned}
$$

#### 2. Formula for $S_1$

$$
\begin{aligned}
S_1(T, R, V, HR) &= 0.347 - 0.001T - 0.037R + 0.033V + 0.015HR \\
&+ 0.001T^2 + 0.004TR + 0.020TV + 0.009THR \\
&+ 0.038R^2 + 0.046RV - 0.008RHR \\
&+ 0.010V^2 - 0.007VHR + 0.024HR^2
\end{aligned}
$$

#### 3. Formula for Slope

$$
\begin{aligned}
Slope(T, R, V, HR) &= 18.331 + 3.117T + 4.027R + 9.137V - 7.222HR \\
&+ 3.204T^2 + 0.420TR + 0.220TV - 0.742THR \\
&+ 3.724R^2 - 0.891RV - 0.479RHR \\
&+ 1.733V^2 - 3.379VHR + 1.238HR^2
\end{aligned}
$$

&nbsp;

### Linear Formulation

#### 1. Formula for $E_1$

$$
\begin{aligned}
E_1(T, R, V, HR) &= 6.548 + 1.664T + 3.383V - 1.995HR \\
&+ 0.058T^2 + 0.601TV - 0.635THR \\
&+ 0.163V^2 - 1.502VHR - 0.244HR^2 \\
&+ 0.381R
\end{aligned}
$$

#### 2. Formula for $S_1$

$$
\begin{aligned}
S_1(T, R, V, HR) &= 0.401 - 0.001T + 0.033V + 0.015HR \\
&- 0.024T^2 + 0.020TV + 0.009THR \\
&- 0.015V^2 - 0.007VHR - 0.001HR^2 \\
&- 0.037R
\end{aligned}
$$

#### 3. Formula for Slope

$$
\begin{aligned}
Slope(T, R, V, HR) &= 23.589 + 3.117T + 9.137V - 7.222HR \\
&+ 0.795T^2 + 0.220TV - 0.742THR \\
&- 0.677V^2 - 3.379VHR - 1.172HR^2 \\
&+ 4.027R
\end{aligned}
$$

&nbsp;

### Notes on Units
- $E(t)$ is expressed in **kg·m⁻²·day⁻¹**.  
- To convert to **kg·m⁻²·s⁻¹**, divide by $24 \times 3600$.  

The **saturation ratio** is defined as:  

$$
S(t) = \frac{\text{Current water content}}{\text{Maximum water content}}
$$

At each time step, the current water content is updated as:  

$$
S(t+\Delta t) = S(t) - \frac{E(t)\cdot \Delta t}{24 \times 3600}
$$

&nbsp;

## Conduction Model
The conductive heat transfer module (integrated in `simulation_Ts_EnergieBat_Khalid.exe`) combines:  

- **3R4C network** for walls,  
- **Finite differences** for ground and MHA.  

In `famille.xml`, surfaces that include latent heat flux (`lE`) must be set as **`sol_new`**.  
- This implementation currently applies only to ground surfaces.  
- If `evaporation` > 0 in `famille.xml`, the latent heat flux is activated (independent of the numeric value).  

