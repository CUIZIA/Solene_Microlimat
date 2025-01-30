# Convective Heat Transfer Models in Urban Environments

## Overview
The convective heat flux exchanged between an urban surface and the air is calculated using:

$$ q_c = h_c (T_{surf} - T_{air}) $$

where:
- $q_c$: Heat convection flux $[W.m^{-2}]$
- $h_c$: Convective heat transfer coefficient $[W.m^{-2}K^{-1}]$
- $T_{surf}$: Surface temperature $[K]$
- $T_{air}$: Air temperature $[K]$

The convective heat transfer coefficient $h_c$ is a crucial parameter in urban heat flux simulations. It depends on both wind speed $U$ and surface roughness. Higher wind speeds increase $h_c$, which enhances convective cooling, reducing surface and near-surface air temperatures in summer.

## Convection Models
Currently, **SOLENE-Microclimat** supports four convection models, each differing in input parameters and complexity. These models are categorized as follows:

### 1. **Wind Speed-Based Model (ASHRAE Model, Default model in SOLENE-Microclimat.)**
- **Equation:**

$$ h_c = 5.7 + 3.8U $$

- **Source:** ASHRAE (1985)
- **Parameters:**
  - $U$: Wind speed $[m.s^{-1}]$.

### 2. **Empirical Correlations Model**
- **Equation:** **Ground Surface (Verhencamp Model, Gui et al., 2007):**

$$ h_c = 698.24 a_c \left[ 0.00144|T_{m}|^{0.3} U^{d_c} + 0.00097 |(T_{surf} - T_{air})|^{0.3} \right] $$

- **Parameters:**
  - Constants: $a_c = 1.4$, $d_c = 0.5$ for the ground.
  - $T_m$: Mean temperature of air and surface $[K]$.

### 3. **Horizontal Flat Plate model (Nusselt number)**
- **Equation:**

<p align="center">
  <img src="/fig/Nusselt model.png" width="250px" style="vertical-align:middle;">
</p>

- **Approach:**
  - Accounts for different convection modes: Free, mixed, and forced convection.
  - Considers laminar and turbulent flow regimes.
  - Applied to ground, walls, and roofs.

### 4. **Aerodynamic Resistance Model (Denby Model, Denby et al., 2013)**
- **Equation:**

$$ h_c = \frac{\rho_a C_p}{r_T} $$

- **Parameters:**
  - $\rho_a$: Air density $[kg.m^{-3}]$
  - $C_p$: Heat capacity of dry air $[J.kg^{-1}.K^{-1}]$
  - $r_T$: Aerodynamic resistance $[s.m^{-1})]$

## Model Comparison Table

| Model Category               | Equation | Parameters Considered | Application |
|-----------------------------|----------|----------------------|-------------|
| **Wind Speed-Based Model** (ASHRAE, 1985) | \( h_c = 5.7 + 3.8U \) | Wind speed \(U\) | Default in SOLENE-Microclimat |
| **Empirical Correlations Model** (Gui et al., 2007; Montazeri & Blocken, 2017) | Multiple equations | Temperature difference, wind speed, surface type, building dimensions | Ground (Verhencamp), Walls & Roofs (Montazeri & Blocken) |
| **Dimensionless Number-Based Model** (Cengel, 2002; Morille, 2012) | Uses dimensionless numbers | Convection mode (free, mixed, forced), flow regime (laminar, turbulent) | Applied to all urban surfaces |
| **Aerodynamic Resistance Model** (Denby et al., 2013) | \( h_c = \frac{\rho_a C_p}{r_T} \) | Air density, heat capacity, aerodynamic resistance | Applied to all urban surfaces |

This selection of models ensures comprehensive coverage of convective heat transfer mechanisms for different urban surfaces, enabling accurate urban microclimate simulations.
