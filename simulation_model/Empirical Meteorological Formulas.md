# Solar Radiation

In Solene, you currently have two methods to input solar radiation, which is crucial for the simulation:  
1. Using the default **Perez sky model**.  
2. Using your own **measured radiation data file**, which is more reliable and accurate.  

This document provides a detailed explanation of the code principles. Please refer to another file for a quick guide on how to use it efficiently.  

## Perez sky model

This sky model is parameterized using two coefficients, **ε** and **∆**, where **ε** represents the degree of sky purity and **∆** 
its brightness (**ε** and **∆** are the clarity and brightness indices in the Perez model). These coefficients are used to determine 
the **diffuse irradiance** on a horizontal plane (**De**) and the **direct normal irradiance** (**Se**).  

Perez defines these irradiances using the following expressions:  

$$
D_e = ∆ \cdot E_{0e} \cdot \frac{a'}{m}
$$

$$
S_e = D_e \cdot (ε-1) \cdot (1+1041 \cdot Z^3)
$$

// still under development

## Measured Radiation Data

In solar radiation measurements, instruments somtimes provide only the Global Horizontal Irradiance (GHI), which includes both direct and diffuse components. However, for simulation purposes, it is often necessary to separate GHI into these two components. Below is a summary of commonly used decomposition models. The first model listed is the one implemented in SOLENE.

### (1) Black (1956) + Muneer et al. (2004)

This empirical decoposition model calculates the **clearness index** ($K$) and the **diffuse solar radiation coefficient** (denoted as $k_d$), followed by computing the decomposition of global solar radiation into **direct** and **diffuse** components.  

$$
K = 0.803 - 0.458 \left(\frac{N}{8}\right)^2 - 0.34 \left(\frac{N}{8}\right)
$$

Where,

- $N$ is cloud cover in oktas.

$$
k_d =
\begin{cases}
0.98, & \text{if } K < 0.2 \\
0.962 + 0.779K - 4.375K^2 + 2.716K^3, & \text{if } K \geq 0.2
\end{cases}
$$

So the diffuse horizontal irradiance (DHI) and direct normal irradiance (DNI) are calculated as follow:

$$
I_{\text{DHI}} = k_d \cdot I_{\text{GHI}}
$$

$$
I_{\text{DNI}} = \frac{(1-k_d) \cdot I_{\text{GHI}}}{cos \theta}
$$

Where,

- $\theta$ is solar zenith angle.


### (2) Kasten and Czeplak (1980)
The second one is also depending on the cloud cover $N$

$$
\text{DIFF2} = 1 - \left(1 - \frac{3}{4} \left(\frac{N}{8}\right)^{3.4} \right)
$$

# Atmospheric Calculations

This document summarizes the formulas used to compute **specific humidity** and **downward longwave radiation** from meteorological data.

## Specific Humidity and Moisture Variables

Given:
- $T_{air}$ : Air temperature (K)  
- $P_{atm}$ : Atmospheric pressure (Pa)  
- $RH$ : Relative humidity (%)  
- $R_d = 287.06$ J·kg⁻¹·K⁻¹ : Gas constant for dry air  
- $R_v = 461$ J·kg⁻¹·K⁻¹ : Gas constant for water vapor  
- $L_v = 2.46 \times 10^6$ J·kg⁻¹ : Latent heat of vaporization  

### a) Saturation vapor pressure
$$
e_s = 611 \cdot \exp\left( \frac{L_v}{R_v} \left(\frac{1}{273.16} - \frac{1}{T_{air}} \right) \right)
$$

### b) Actual vapor pressure
$$
e = \frac{RH}{100} \cdot e_s
$$

### c) Specific humidity (kg·kg⁻¹)
$$
q = \frac{0.622 \, e}{P_{atm} - 0.378 \, e}
$$

### d) Air density (g·m⁻³)
$$
\rho = \frac{1}{R_d \, T_{air}} \left( P_{atm} - f(e, RH, T_{air}) \right)
$$

(where $f(\cdot)$ is a correction term accounting for water vapor)

### e) Absolute humidity (kg·m⁻³)
$$
q_a = q \cdot \rho
$$

### f) Saturated specific humidity
$$
q_s = \frac{0.622 \cdot e_s / P_{atm}}{1 + (0.622 - 1) \cdot e_s / P_{atm}}
$$

### g) Final humidity output (g·kg⁻¹)
$$
Q = 1000 \cdot \frac{RH}{100} \cdot q_s
$$

## Downward Longwave Radiation ($L_\downarrow$)

Following **Prata (1996)** and **Diak (2000)** formulations:

### a) Intermediate variable
$$
w = 46.5 \cdot \frac{e}{100 \cdot T_{air}}
$$

### b) Effective emissivity
$$
\varepsilon = 1 - (1 + w) \cdot \exp \left( -\sqrt{1.2 + 3w} \right)
$$

### c) Clear-sky longwave radiation
$$
L = \varepsilon \cdot \sigma \cdot T_{air}^4
$$

where $\sigma = 5.6704 \times 10^{-8}$ W·m⁻²·K⁻⁴ is the Stefan–Boltzmann constant.

### d) Cloud correction (using cloud cover $N$ in oktas, from 0 to 8)
$$
L_\downarrow = \left(1 - \frac{N}{8}\right) L + \frac{N}{8} \cdot \sigma T_{air}^4
$$


## **Outputs**

- $q$ : Specific humidity (kg·kg⁻¹)  
- $q_a$ : Absolute humidity (kg·m⁻³)  
- $Q$ : Humidity in g·kg⁻¹  
- $L_\downarrow$ : Downwelling longwave radiation (W·m⁻²)  


## References
1. Black, J. N. "The distribution of solar radiation over the earth's surface." Archiv für Meteorologie, Geophysik und Bioklimatologie, Serie B 7 (1956): 165-189.
2. Muneer, Tariq. Solar radiation and daylight models. Routledge, 2007. P49
3. Kasten, Fritz, and Gerhard Czeplak. "Solar and terrestrial radiation dependent on the amount and type of cloud." Solar energy 24.2 (1980): 177-189.
