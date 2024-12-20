# SOLENE Microclimat - THERMAL MODEL

The SOLENE-Microclimat model integrates the radiation and thermal modules of SOLENE with the fluid dynamics module of Code_Saturne. It employs different thermal radiation balance schemes depending on the type of surface: impermeable ground surfaces, vegetated ground surfaces, and building walls. This explanation focuses on the impermeable ground surface case, where only heat transfer is considered, neglecting moisture transfer. The SOLENE code is structured into four main components (as **Figure 1**):
- updating surface temperatures using the relaxation factor;
- solar radiation computation;
- conduction model methodology;
- convergence assessment.

<p align="center">
  <img src="/fig/workflow.png" alt="Code Flowchart of SOLENE" width="90%">
</p>

<p align="center"><b>Figure 1: Code Flowchart of SOLENE.</b></p>

&nbsp;

## 1. Conduction Modeling (Ground)

The ground conduction model in SOLENE is based on the soil model developed by Marie-Hélène Azam. This model is specifically designed for impermeable surfaces such as pavement coatings, considering only heat transfer (while ignoring moisture transfer). The soil model is one-dimensional, with each layer characterized by its unique properties. Under transient conditions, temperature fluctuations are calculated using **Equation 1**, which represents the heat conduction equation applied to a one-dimensional problem.

The core of the conduction model in SOLENE is solved using an implicit finite difference formulation inspired by electrical analogy. Thermal resistance represents the resistance to heat transfer through the ground layers, and thermal capacitance represents the ability of the ground layers to store heat, as illustrated in **Figure 2**. The soil model consists of $n$ nodes, with each node representing a specific layer of the ground.

The general heat conduction equation in soil can be written as:

$$
\frac{\partial T}{\partial t} = \alpha_{\text{soil}} \frac{\partial^2 T}{\partial x^2}
$$

Where:

- $T$ is the temperature $[K]$.
- $t$ is the time $[s]$.
- $x$ is the spatial coordinate $[m]$.
- $\alpha_{\text{soil}}$ is the thermal diffusivity of the soil $[m^2/s]$.

The soil is divided into $n$ layers, and we can consider three scenarios, including: (1) Surface Boundary Condition (Soil-Air Interface); (2) Internal Nodes of the soil $i$; (3) Deep Soil Boundary Condition.

<p align="center">
  <img src="/fig/Conduction_MHA.png" alt="Schematic representation of the soil model." width="25%">
</p>

<p align="center"><b>Figure 2: Schematic representation of the soil model.</b></p>

### 1.1 Nomenclature

- $C_s$ is the surface layer heat capacity $[J/m^2K]$.
- $T_s$ is the surface temperature $[K]$.
- $T_1$ is the temperature at the first node beneath the surface $[K]$.
- $T_a$ is the air temperature $[K]$.
- $h_c$ is the convective heat transfer coefficient.
- $R_1$ is the heat resistance between the surface and the first node $[K/W]$.
- $R_{\text{net}}$ is the net radiation $[W/m^2]$.
- $LE$ is the latent heat flux $[W/m^2]$.
- $C_i$ is the heat capacity of the layer at the node $i$ $[J/m^2K]$.
- $T_i$ is the temperature of the node $i$ $[K]$.
- $R_i$ is the heat resistance of the layer between the node $i-1$ and $i$ $[K/W]$.
- $T_{\infty}$ is the deep soil temperature $[K]$.

### 1.2 Implicit Finite Element Discretization for the Soil Model

We consider the soil model divided into \(n\) layers, and we solve the heat conduction problem using the implicit finite element method (FEM). The model consists of three parts:

1. Surface boundary condition (soil-air interface),
2. Internal nodes,
3. Deep soil boundary condition.

#### (1) Surface Boundary Condition (Soil-Air Interface)

At the surface node ($i = 0$), the energy balance equation accounts for latent heat, radiation, and conduction between the surface and the first layer beneath it:

$$
C_s \frac{dT_s}{dt} + h_c(T_s - T_a) + \frac{T_s - T_1}{R_1} = R_{\text{net}} - L E
$$

In matrix form, this equation can be discretized using the implicit time-stepping method. Assuming $T_s^t$ is the temperature at the current time step and $T_s^{t+1}$ is at the next time step:

$$
C_s \frac{T_s^{t+1} - T_s^t}{\Delta t} + h_c(T_s^{t+1} - T_a^{t+1}) + \frac{T_s^{t+1} - T_1^{t+1}}{R_1} = R_{\text{net}} - L E
$$

This forms part of the matrix system where $T_s^{t+1}$ depends on the surface and the first internal node.

#### (2) Internal Nodes

For internal nodes $i$, the energy balance equation is:

$$
C_i \frac{dT_i}{dt} + \frac{T_i - T_{\text{i+1}}}{R_{\text{i+1}}} - \frac{T_{\text{i-1}} - T_i}{R_i} = 0
$$

Using the implicit method, this can be written as:

$$
C_i \frac{T_i^{t+1} - T_i^t}{\Delta t} + \frac{T_i^{t+1} - T_{\text{i+1}}^{t+1}}{R_{\text{i+1}}} - \frac{T_{\text{i-1}}^{t+1} - T_i^{t+1}}{R_i} = 0
$$

#### (3) Deep Soil Boundary Condition

At the deep soil boundary, the temperature is assumed to approach a constant $T_{\infty}$. The energy balance equation at the bottom node is:

$$
C_i \frac{dT_i}{dt} + \frac{T_i - T_{\infty}}{R_{\text{i+1}}} - \frac{T_{\text{i-1}} - T_i}{R_i} = 0
$$

In implicit form:

$$
C_i \frac{T_i^{t+1} - T_i^t}{\Delta t} + \frac{T_i^{t+1} - T_{\infty}}{R_{\text{i+1}}} - \frac{T_{\text{i-1}}^{t+1} - T_i^{t+1}}{R_i} = 0
$$

### 1.3 Assembling the Matrix System

The soil model with $n$ layers forms a system of equations that can be written in matrix form as:

$$
\mathbf{A} \mathbf{T}^{t+1} = \mathbf{B}
$$

Where:

- $\mathbf{A}$ represents the system's coefficient matrix,
- $\mathbf{T}^{t+1}$ is the unknown temperature vector at the next time step $t+1$,
- $\mathbf{B}$ is a combination of known values, including constant terms and contributions from the previous time step $n$.

For impermeable soil, between the time steps $[t]$ and $[t+1]$ the matrix system is written:

$$
\left[
\begin{matrix}
\frac{C_s}{\Delta t} + h_c + \frac{1}{R_1} & -\frac{1}{R_1} & 0 & \cdots & 0 \\\\
-\frac{1}{R_1} & \frac{C_1}{\Delta t} + \frac{1}{R_1} + \frac{1}{R_2} & -\frac{1}{R_2} & \cdots & 0 \\\\
0 & -\frac{1}{R_2} & \frac{C_2}{\Delta t}+ \frac{1}{R_2} + \frac{1}{R_3} & \cdots & 0 \\\\
\vdots & \vdots & \vdots & \ddots & \vdots \\\\
0 & \cdots & 0 & -\frac{1}{R_n} & \frac{C_n}{\Delta t} + \frac{1}{R_n} \\\\
\end{matrix}
\right]
\times
\left[
\begin{matrix}
T_s^{t+1} \\\\
T_1^{t+1} \\\\
T_2^{t+1} \\\\
\vdots \\\\
T_n^{t+1} \\\\
\end{matrix}
\right]
\quad \text{=} \quad
\left[
\begin{matrix}
\frac{C_s}{\Delta t} T_s^t + R_{\text{net}} - LE + h_c T_{a} \\\\
\frac{C_1}{\Delta t} T_1^t \\\\
\frac{C_2}{\Delta t} T_2^t \\\\
\vdots \\\\
\frac{C_i}{\Delta t} T_i^t - \frac{T_{\infty}}{R_{\text{i+1}}} \\\\
\end{matrix}
\right]
$$

### 1.4 Deep Boundary Condition

In deep soil, the temperature is assumed to remain constant over the course of a day. For homogeneous soil, an analytical solution can be used to calculate the temperature at any depth if the surface temperature is considered to be sinusoidal. The parameters $T_{\text{ma}}$, $A_a$ and $t_0$ are respectively the mean, the amplitude, and the phase of a day surface temperature signal:

$$
T(z,t) = T_{\text{ma}} + A_a \cdot exp\left[-\frac{z}{zd_a}\right]sin\left[w_a(t-t_0)-\frac{z}{zd_a}\right]
$$

Where,
- $T_{\text{ma}}$ is mean annual temperature $[°C]$.
- $A_a$ is annual half amplitude of the climatic thermal wave at the surface $[°C]$, $A_a = \frac{T_{\text{air,max}} - T_{\text{air,min}}}{2}$.
- $zd_a$ is damping depth with an annual beat, $z_d = \sqrt{\frac{2 \alpha_{\text{sol}}}{w_a}}$ $[m]$.
- $w_a$ is annual beat $w_a = 2 \cdot \pi / 365$ $[rad \cdot day^-1]$.
- $t$ is day of year number (1 to 365).
- $t_0$ is day of the year where the surface temperature was the coldest.
- $\alpha_{\text{sol}}$ is thermal diffusivity of the sol $[m^2/s]$

The thermal diffusivity is calculated using the following formula:

$$
\alpha_{\text{sol}} = \frac{\lambda_{\text{sol}}}{\rho_{\text{sol}} \cdot C_{p_{\text{sol}}}} \cdot 24 \cdot 3600
$$

Where:
- $\lambda_{\text{sol}}$ is the equivalent thermal conductivity.
- $\rho_{\text{sol}}$ is the equivalent soil density.
- $C_{p_{\text{sol}}}$ is the equivalent specific heat capacity.
- The multiplication by $24 \cdot 3600$ converts the thermal diffusivity into units of square meters per second $[m^2/s]$.

&nbsp;

## 2. Conduction Modeling (Wall)

The **wall conduction model** was initially developed as the **1R2C model** by Julien Bouyer, and later evolved into the **3R4C model** proposed by Fraisse et al. (2002). The core principle of this method involves transforming a multi-layered wall into a simplified **3R2C model** through mathematical operations, which is then further refined into the **3R4C model** using the **5% method**. Below are the principles and implementation details of the algorithm:

### 2.1 Principles of the Algorithm

Two new nodes, $T_{p1}$ and $T_{p2}$, are created within the wall and are associated with thermal capacitances $C_1$ and $C_2$, respectively. The thermal resistance of the wall, originally denoted as $R$, is divided into **three resistances**: $R_1$, $R_2$, and $R_3$. These resistances are positioned:
- Between $T_{se}$ (external surface) and $T_{p1}$,
- Between $T_{p1}$ and $T_{p2}$,
- Between $T_{p2}$ and $T_{n1}$ (internal surface).

The **3R2C** and **3R4C** models are illustrated in the figure below.

<p align="center">
  <img src="/fig/3R2C.png" alt="3R2C" width="40%">
</p>

<p align="center">
  <img src="/fig/3R4C.png" alt="3R4C" width="40%">
</p>

<p align="center"><b>Figure 3: Model 3R2C and 3R4C.</b></p>

#### (1) Resistance and Capacitance Calculation

Both models compute thermal resistance in the same way, where the total wall resistance $R_t$ is the sum of individual resistances $R_i$, with $\alpha_i$ satisfying the condition $\sum \alpha_i = 1$. In the **3R2C model**, the total thermal capacitance $C_t$ is similarly represented. The values $\beta_1$ and $\beta_2$ are used to determine the capacitance distribution in the **3R2C** model.

$$
\begin{cases}
    R_1 = \alpha_1 \cdot R_t \\
    R_2 = \alpha_2 \cdot R_t \\
    R_3 = \alpha_3 \cdot R_t \\
    \sum \alpha_i = 1 \\
    C_1 = \beta_1 \cdot C_t \\
    C_2 = \beta_2 \cdot C_t \\
    \sum \beta_i = 1
\end{cases}
$$

When the simulation time step is short (approximately 10 minutes), it is necessary to account for the thin layers of the wall to consider high-frequency effects [10]. Conversely, since the model’s thermal capacity is concentrated within the wall, the internal temperature node $T_{\text{int}}$ immediately accounts for the heat flux reaching the inner surfaces of the **3R2C** model. Our approach systematically transfers 5% of the two internal capacities to each surface of the wall. As a result, we define the **3R4C model**. The advantage of this method lies in its simplicity and sufficient accuracy. According to the following equation, the 5% method is applied to redistribute 5% of the capacitance from the **3R2C model** to the nearest surfaces, creating two additional capacitances:
- $C_e$: Associated with the external surface,
- $C_i$: Associated with the internal surface.

$$
\begin{cases}
    C_e = 0,05 \cdot \beta_1 \cdot C_t \\
    C_1 = 0,95 \cdot \beta_1 \cdot C_t \\
    C_2 = 0,95 \cdot \beta_2 \cdot C_t \\
    C_e = 0,05 \cdot \beta_2 \cdot C_t
\end{cases}
$$

#### (2) Parameter Calculation in 3R2C Transfer Matrix (αi, βi)

The specific method can be referenced in **Fraisse et al., 2002**, where the approach is described in great detail. In short, it involves constructing a **multi-layer transfer matrix** (by calculating the product of matrices), followed by the construction of a **3R2C transfer matrix**. Using a **second-order expansion**, an equivalence between these two matrices is established, and the coefficients $\alpha_i$ and $\beta_i$ can then be calculated. The matrix multiplication is not particularly complex, and the corresponding code can be found in the file [3R2C coefficient calculation](3R2C%20coefficient%20calculation.md) for reference (calculating the coefficients $m_1$, $m_2$, $o_2$, and $p_2$).

The resulting transfer matrix for the multi-layer system is as follows:

$$
\left[
\begin{matrix}
A_1(p) & B_1(p) \\\\
C_1(p) & D_1(p)
\end{matrix}
\right]
\cdot \cdot \cdot
\left[
\begin{matrix}
A_{\text{Nc}}(p) & B_{\text{Nc}}(p) \\\\
C_{\text{Nc}}(p) & D_{\text{Nc}}(p)
\end{matrix}
\right]
= H(p)_{\text{ref}}
$$

**After the second-order expansion:**

$$
H(p)_{\text{ref}} =
\left[
\begin{matrix}
1+pm_1+p^2m_2 & R+pn_1+p^2n_2 \\\\
pC+p^2o_2 & 1+pp_1+p^2p_2 \\\\
\end{matrix}
\right]
$$

However, the resulting transfer matrix for the **3R2C model** is as follows:

$$
H(p)_{\text{3R2C}} =
\left[
\begin{matrix}
1 & R_1 \\
0 & 1
\end{matrix}
\right]
\times
\left[
\begin{matrix}
1 & 0 \\\\
pC_1 & 1 \\\\
\end{matrix}
\right]
\times
\left[
\begin{matrix}
1 & R_2 \\
0 & 1
\end{matrix}
\right]
\times
\left[
\begin{matrix}
1 & 0 \\\\
pC_2 & 1 \\\\
\end{matrix}
\right]
\times
\left[
\begin{matrix}
1 & R_3 \\
0 & 1
\end{matrix}
\right]
$$

$$
H(p)_{\text{3R2C}} =
\left[
\begin{matrix}
1+pR_tC_tx_1+(pR_tC_t)^2x_2 & R+p R_t^2 C_tx_3+p^2 R_t^3 C_t^2 x_4 \\
pC + p^2 R_t C_t^2 x_5 & 1+p R_t C_t x_6+(p R_t C_t)^2x_7
\end{matrix}
\right]
$$

Where,

$$
\begin{cases}
    x_1 = \alpha_2 \beta_1 + \alpha_1 \\
    x_2 = \alpha_1 \alpha_2 \beta_1 \beta_2 \\
    x_3 = \alpha_1 \alpha_2 \beta_1 + \alpha_3(\alpha_2 \beta_2 + \alpha_1) \\
    x_4 = \alpha_1 \alpha_2 \alpha_3 \beta_1 \beta_2 \\
    x_5 = \alpha_2 \beta_1 \beta_2 \\
    x_6 = \alpha_3 + \alpha_2 \beta_1 \\
    x_7 = \alpha_2 \alpha_3 \beta_1 \beta_2
\end{cases}
$$

By correlating the coefficients of these two matrices $H(p)$, you can calculate $\alpha_i$ and $\beta_i$. The coefficients required for this calculation include $m_1$, $m_2$, $o_2$, and $p_2$.

$$
\begin{cases}
  \beta_1 = \frac{-o_2(1 + \frac{p_2}{m_2}) + R_t C_t^2 + \sqrt[2]{\Delta}}{2R_t C_t^2 \zeta} \\
  \beta_2 = 1 - \beta_1 \\
  \alpha_2 = \frac{o_2}{R_t C_t^2 \beta_1 \beta_2} \\
  \alpha_1 = \frac{m_1}{R_t C_t} - \alpha_2 \beta_2 \\
  \alpha_3 = 1 - \alpha_1 - \alpha_2 \\
  where, \\
  \zeta = 1 - \frac{m_1}{R_t C_t}(1 + \frac{p_2}{m_2}) \\
  \Delta = [o_2(1+\frac{p_2}{m_2}) - R_t C_t^2\zeta]^2 + 4 R_t C_t^2 \zeta o_2 \frac{p_2}{m_2} \\
\end{cases}
$$

#### (3) Assembling the Matrix System

As the as what we did with the sol, the matrix system between the time steps $[t]$ and $[t+1]$ is for the wall written as:

$$
\left[
\begin{matrix}
 \frac{C_e}{\Delta t} + \frac{1}{R_1} + h_c & -\frac{1}{R_1} & 0 & 0 \\\\
-\frac{1}{R_1} & \frac{C_1}{\Delta t} + \frac{1}{R_1} + \frac{1}{R_2} & -\frac{1}{R_2} & 0 \\\\
0 & -\frac{1}{R_2} & \frac{C_2}{\Delta t}+ \frac{1}{R_2} + \frac{1}{R_3} & -\frac{1}{R_3} \\\\
0 & 0 & -\frac{1}{R_3} & \frac{1}{R_3} + \frac{C_i}{\Delta t} + h_{int} \\\\
\end{matrix}
\right]
\times
\left[
\begin{matrix}
T_{se}^{t+1} \\\\
T_{p1}^{t+1} \\\\
T_{p2}^{t+1} \\\\
T_{si}^{t+1} \\\\
\end{matrix}
\right]
\quad \text{=} \quad
\left[
\begin{matrix}
\frac{C_e}{\Delta t} T_{se}^t + h_c T_{a} + R_{\text{net}} \\\\
\frac{C_1}{\Delta t} T_{p1}^t \\\\
\frac{C_2}{\Delta t} T_{p2}^t \\\\
\frac{C_i}{\Delta t} T_{si}^t + h_{int}T_{int}\\\\
\end{matrix}
\right]
$$

&nbsp;

## 3. Convergence Validation

This section of the code implements a convergence test for surface temperatures (`fc_Tsext`) over multiple iterations. It evaluates both individual and global discrepancies between current and previous values of surface temperatures. The algorithm determines whether the simulation has converged based on defined thresholds (`eps1` for individual errors and `eps2` for average global error). If convergence criteria are not met, the process iterates until a maximum of 50 iterations. The flowchart of the convergence process is shown in **Figure 4**.

### 3.1 Principles of the Algorithm

- **Iterative Testing**: Evaluates the temperature deviations for each surface element in an iterative manner.
- **Threshold-Based Evaluation**: Compares individual and global deviations against predefined thresholds (`eps1` and `eps2`).
- **Dynamic Updates**: Tracks and updates the number of non-converged elements across iterations.
- **Final Convergence Check**: Determines if the simulation can stop based on the percentage of non-converged elements (`ratio_face_non_cv`).
- **Maximum Iterations**: Caps the number of iterations at 50 to avoid infinite loops and reduce computational cost.

### 3.2 Code Variables

| Variable                  | Role                                                                 |
|---------------------------|----------------------------------------------------------------------|
| `test_Ts`                 | Tracks the number of non-converged elements in the current iteration.|
| `somme_deltaT`            | Accumulates the total deviation for computing the global average.    |
| `deltaT`                  | Absolute difference between the current and previous surface temperatures. |
| `eps1`                    | Threshold for individual element deviation.                         |
| `eps2`                    | Threshold for global average deviation.                             |
| `n_face_non_cv_old_1`     | Number of non-converged elements in the current iteration.           |
| `n_face_non_cv_old_2`     | Number of non-converged elements in the previous iteration.          |
| `ratio_face_non_cv`       | Percentage of non-converged elements for acceptable convergence. |
| `iter`                    | Iteration counter to enforce maximum iteration limits.              |

<p align="center">
  <img src="/fig/convergence.png" alt="Code Flowchart of convergence" width="100%">
</p>

<p align="center"><b>Figure 4: Convergence Validation Process.</b></p>

&nbsp;

## 4. Update Surface Temperature

Before convergence verification is successful, the calculated surface temperature must be continuously updated. This is primarily done to improve **numerical stability** and **convergence speed**. By introducing a **relaxation factor** $\omega$ (where $0 < \omega \leq 1$), the update process can be smoothed, avoiding abrupt oscillations and gradually approaching the converged solution. The update formula is as follows:

$$
T_{t+1} = \omega \cdot T_{\text{computed}} + (1 - \omega) \cdot T_{t}
$$

Where,
- $T_{\text{computed}}$ is the temperature value calculated at the current iteration step based on the numerical method being used.

### 4.1 Piecewise Relaxation Method in Solene

In Solene, a **piecewise relaxation method** is implemented to adjust the relaxation factor dynamically during iterations:

$$
\begin{cases}
  iter > 10, \omega = 0.8 \\
  iter > 20, \omega = 0.7 \\
  iter > 30, \omega = 0.6 \\
  iter > 40, \omega = 0.5 \\
\end{cases}
$$

&nbsp;

## 5. Long-wave Irradiance Calculation (Net)
After obtaining the updated surface temperatures, it is essential to recalculate the **long-wave irradiance** ($GLO, \text{Grande Longueur d’Onde}$) emitted by each surface. The net long-wave irradiance for each surface can then be determined. It includs tow part: net long-wave irradiance exchange with the sky $GLO_{\text{ciel,net}}$ and net long-wave irradiance within the scene $GLO_{\text{scene, net}}$ as shown in **Figure 5**. In SOLENE, while the reflection of atmospheric long-wave radiation within the study area is considered, the reflection of long-wave radiation emitted by the surfaces themselves is currently neglected. This decision is based on a prior sensitivity analysis, which concluded that its impact is negligible.

To handle long-wave irradiance calculations, SOLENE introduces a `calc_GLO` function. The net long-wave irradiance $GLO_{\text{net,i}}$ for surface $i$ is given by:

$$
GLO_{\text{net,i}} = GLO_{\text{ciel,net,i}} + GLO_{\text{scene,net,i}}
$$

$$
GLO_{\text{net}} = GLO_{\text{emis}} - GLO_{\text{recu}}
$$

<p align="center">
  <img src="/fig/GLO_net.png" alt="GLO_net" width="40%">
</p>

<p align="center"><b>Figure 5: Long-wave irradiance exchange in surface.</b></p>

### 5.1 Net Long-wave Irradiance Exchange with the Sky $GLO_{\text{ciel,net}}$

The atmospheric long-wave irradiance received by surface $i$ ($GLO_{\text{atm,i}}$) is treated as a constant value for a fixed time step. Thus, it is not recalculated during the iterative loop for updating surface temperatures. We can intuitively understand that $GLO_{\text{ciel,net,i}}$ represents the net irradiance received by a surface, which is the sum of the net irradiance received by the surface and the net irradiance emitted from it. 

$$
GLO_{\text{ciel,net}} = GLO_{\text{ciel,net,emis}} + GLO_{\text{ciel,net,recu}}
$$

#### (1) Net Long-Wave Irradiance Emitted by the Surface $GLO_{\text{ciel,net,emis}}$

The calculation of the net irradiance received by surface is more complex than it may initially appear. Its only source is the **longwave radiation from the sky** and the **multiple reflections** of longwave radiation within the study area.

The first and simplest component to calculate is the longwave irradiance emitted by the surface to the sky $GLO_{\text{ciel,net,emis,i}}$, which is expressed using the following formula:

$$
GLO_{\text{ciel,net,emis,i}} = \text{SVF} \cdot \varepsilon_i \cdot \sigma \cdot T_i^4
$$

Where:
- $\sigma$: Stefan-Boltzmann constant, $5.67 \times 10^{-8}, [\text{Wm}^{-2}\text{K}^{-4}]$,
- $\varepsilon$: Emissivity of the surface,
- $\text{SVF}$: Sky View Factor,
- $T_i$: Surface temperature $[K]$.

#### (2) Net Long-Wave Irradiance Received by the Surface $GLO_{\text{ciel,net,recu}}$

The calculation of the net irradiance received by surface is more complex than it may initially appear (see function `calc_flux_atm_intereflexion`). Its only source is the **longwave radiation from the sky** and the **multiple reflections** of longwave radiation within the study area. To account for these reflections, SOLENE employs an **radiosity method** (`radiog` function in code). The method iteratively calculates the reflected longwave radiation within the scene. The iteration process continues until the total reflected longwave radiation from all surfaces in the scene becomes less than **2%** (could be modified) of the initial incoming longwave radiation from the sky. Key steps are as follow:

1. **Calculate the Initial Reflected Irradiance**:  
   - Compute the initial reflected irradiance $GLO_{\text{ref}}$ (`exitance_init`) for each surface.  
   - Sum the total initial reflected radiation from the sky $Q_{\text{ref,total}}$ (`energie_totale`) where $A_i$ is the surface area:
   
$$
Q_{\text{ref,total}} = \sum_{i=1}^n GLO_{\text{ref},i} \cdot A_i
$$

2. **Iteratively Compute Reflected Radiation**:  
   - Calculate the reflected radiation for each surface $GLO_{\text{ref},i} \cdot A_i$ (`delta_exitance[] * surf[]`) within the scene.  
   - Identify the **highest reflected radiation** value (`a_distribuer_max`) among all surfaces.

3. **Distribute the Reflected Radiation**:  
   - Distribute the maximum reflected radiation (`a_distribuer_max`) to nearby surfaces using **view factors** and let the maximum reflected radiation equals to **zero**.
   - Recalculate the reflected radiation $GLO_{\text{ref},i} \cdot A_i$ for the next iteration, updating the values (`delta_exitance`).

4. **Summing Reflected Radiation**:  
   - At each iteration, sum up the reflected radiation from all surfaces into `a_distribuer`.

5. **Check for Convergence**:  
   - Stop the iteration when the total reflected longwave radiation across all surfaces (`a_distribuer`) becomes less than **2%** of the total initial reflected radiation (`energie_totale`).

### 5.2 Net Long-Wave Irradiance Exchange within the Scene $GLO_{\text{scene,net}}$

The net long-wave irradiance exchange between surfaces within the scene is computed directly. For the surface $i$, the radiation exchange is updated using the following formula:

$$
GLO_{\text{scene,net,i}} = \sum_{j=1}^n \sigma \cdot F_{ij} \cdot \left( \varepsilon_i \cdot T_i^4 - \varepsilon_j \cdot T_j^4 \right)
$$

Where:
- $F_{ij}$: Form factor (shape factor) between surfaces $i$ and $j$,
- $\varepsilon_i$, $\varepsilon_j$: Emissivities of surfaces $i$ and $j$,
- $T_i$, $T_j$: Temperatures of surfaces $i$ and $j$.

&nbsp;

## 6. Discussion

This document focuses on explaining the compiled **.exe file** of SOLENE, which forms the core computational structure of the **thermal model**.

#### （1）Surface Temperature Calculation and GPU Optimization
Within each time step, the surface temperature is determined through **matrix operations**. Since the computations for each surface are completely independent, this step can be **fully parallelized** and accelerated using **GPU computation**.  
- **Future Improvement**: Leveraging CUDA or OpenCL for GPU programming can drastically reduce computation time, especially for simulations involving a large number of surfaces.

#### （2）Pre-Calculation of Static Parameters
The parameters used in matrix operations (e.g., $m_1$, $m_2$, $o_2$, $p_1$, and $p_2$ in the **3R4C model**) are **time-independent**. These parameters do not need to be repeatedly computed within the thermal model. Instead, they can be **pre-computed** outside the module and stored for reuse. The computational load for these coefficients is relatively low but highly repetitive, making this optimization simple yet effective.  
- **Future Improvement**: Pre-calculate these coefficients during initialization or as part of a **lookup table**. This will streamline the runtime performance of the SOLENE thermal model.

#### (3) Time Step Limitation and Future Optimization
Currently, due to limitations in the **underlying C code** of SOLENE, the minimum time step is restricted to **30 minutes**. The paper mentions that the choice of time step needs to find a balance between calculation time, shadow dynamics and material response, and is usually 30 minutes to 1 hour.
- **Future Improvement**:
    - Reduce the time step to **10 minutes** to better capture high-frequency thermal dynamics, especially for transient simulations or short-term thermal events;
    - Although reducing the time step will increase the overall simulation time, the aforementioned **GPU acceleration** and **pre-computation of static parameters** can compensate for this increase.

#### (4) Relaxation Factor $\omega$ Improvement in Iterative Updates
The relaxation factor $\omega$ plays a key role in stabilizing the iterative updates of surface temperature. Currently, SOLENE uses a **fixed relaxation factor** according to the iteration number, but there is room for improvement:  
- **Future Improvement**: Implement other relaxaiton algorithms to dynamically tune $\omega$ during runtime.

#### (5) Python Integration and Code Refactoring
While the thermal model core is written in C, other parts of SOLENE involve Python for data handling and I/O operations. The Python codebase uses older versions of libraries, which limits its ability to utilize modern features and performance improvements.  
- **Future Improvement**:
   - Upgrade the Python code to a higher version, ensuring compatibility with **modern packages** like `Pandas`, and GPU-compatible libraries such as `PyTorch`.
   - Refactor Python scripts to leverage GPU acceleration wherever applicable, such as pre-processing large datasets or performing auxiliary calculations.  

#### (6) Additional Potential Improvements
- **Visualization Enhancements**: Improve the post-processing visualization tools to handle larger datasets and provide real-time graphical feedback.
- **Transparent surfaces**: Non-transparent surfaces are considered opaque and obey Lambert's law.

This document primarily focuses on the **C-implemented thermal model** of SOLENE and its potential improvements. The Python components will be described in a separate document, where we will address their role in SOLENE's workflow and explore upgrades for better performance and GPU compatibility. By addressing the above improvements—including GPU acceleration, pre-computation of parameters, time step optimization, dynamic relaxation factors, and Python refactoring—I am confident that SOLENE can achieve **higher efficiency, accuracy, and scalability** in future simulations.

## References
1. Fraisse G, Viardot C, Lafabrie O, et al. Development of a simplified and accurate building model based on electrical analogy[J]. Energy and buildings, 2002, 34(10): 1017-1031. DOI: [Link](https://doi.org/10.1016/S0378-7788(02)00019-1)
2. Baptiste B, Auline R, et al. DIRT : Utilisation de données satellitaires thermiques urbaines dans les outils de simulation microclimatique à l’échelle du quartier dans le cadre de la mission TRISHNA.
3. Azam M H, Morille B, Bernard J, et al. A new urban soil model for SOLENE-microclimat: Review, sensitivity analysis and validation on a car park[J]. Urban climate, 2018, 24: 728-746. DOI: [Link](https://doi.org/10.1016/j.uclim.2017.08.010)
4. Bouyer J. Modélisation et simulation des microclimats urbains-Etude de l'impact de l'aménagement urbain sur les consommations énergétiques des bâtiments[D]. Université de Nantes, 2009. [Link](https://theses.hal.science/tel-00426508/)
