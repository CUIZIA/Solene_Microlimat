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
