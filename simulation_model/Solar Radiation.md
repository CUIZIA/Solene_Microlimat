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

In solar radiation measurements, instruments typically provide only the Global Horizontal Irradiance (GHI), which includes both direct and diffuse components. However, for simulation purposes, it is often necessary to separate GHI into these two components. Below is a summary of commonly used decomposition models. The first model listed is the one implemented in SOLENE.

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

## References
1. Black, J. N. "The distribution of solar radiation over the earth's surface." Archiv für Meteorologie, Geophysik und Bioklimatologie, Serie B 7 (1956): 165-189.
2. Muneer, Tariq. Solar radiation and daylight models. Routledge, 2007. P49
3. Kasten, Fritz, and Gerhard Czeplak. "Solar and terrestrial radiation dependent on the amount and type of cloud." Solar energy 24.2 (1980): 177-189.
