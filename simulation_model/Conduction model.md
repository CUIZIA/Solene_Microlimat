# Conduction Model - SOLENE THERMAL MODEL

The SOLENE-Microclimat model integrates the radiation and thermal modules of SOLENE with the fluid dynamics module of Code_Saturne. It employs different thermal radiation balance schemes depending on the type of surface: impermeable ground surfaces, vegetated ground surfaces, and building walls. This explanation focuses on the impermeable ground surface case, where only heat transfer is considered, neglecting moisture transfer. The SOLENE code is structured into four main components (as **Figure 1**): (1) updating surface temperatures using the relaxation factor; (2) solar radiation computation; (3) conduction model methodology; and (4) convergence assessment. The following sections provide a detailed explanation of the model and its implementation.

<p align="center">
  <img src="/fig/workflow.png" alt="Code Flowchart of SOLENE" width="90%">
</p>

<p align="center"><b>Figure 1: Code Flowchart of SOLENE.</b></p>

## Conduction model methodology
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

### Nomenclature
- $C_s$ is the surface layer heat capacity $[J/m^2K]$.
- $T_s$ is the surface temperature $[K]$.
- $T_1$ is the temperature at the first node beneath the surface $[K]$.
- $T_a$ is the air temperature $[K]$.
- $R_c$ is defined as $R_c = \frac{1}{h_c}$, where $h_c$ is the convective heat transfer coefficient.
- $R_1$ is the heat resistance between the surface and the first node $[K/W]$.
- $R_{\text{net}}$ is the net radiation $[W/m^2]$.
- $LE$ is the latent heat flux $[W/m^2]$.
- $C_i$ is the heat capacity of the layer at the node $i$ $[J/m^2K]$.
- $T_i$ is the temperature of the node $i$ $[K]$.
- $R_i$ is the heat resistance of the layer between the node $i-1$ and $i$ $[K/W]$.
- $T_{\infty}$ is the deep soil temperature $[K]$.

### Implicit Finite Element Discretization for the Soil Model

We consider the soil model divided into \(n\) layers, and we solve the heat conduction problem using the implicit finite element method (FEM). The model consists of three parts:

1. Surface boundary condition (soil-air interface),
2. Internal nodes,
3. Deep soil boundary condition.

#### (1) Surface Boundary Condition (Soil-Air Interface)

At the surface node ($i = 0$), the energy balance equation accounts for latent heat, radiation, and conduction between the surface and the first layer beneath it:

$$
C_s \frac{dT_s}{dt} + \frac{T_s - T_a}{R_c} + \frac{T_s - T_1}{R_1} = R_{\text{net}} - L E
$$

In matrix form, this equation can be discretized using the implicit time-stepping method. Assuming $T_s^t$ is the temperature at the current time step and $T_s^{t+1}$ is at the next time step:

$$
C_s \frac{T_s^{t+1} - T_s^t}{\Delta t} + \frac{T_s^{t+1} - T_a^{t+1}}{R_c} + \frac{T_s^{t+1} - T_1^{t+1}}{R_1} = R_{\text{net}} - L E
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

### Assembling the Matrix System

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
\frac{C_s}{\Delta t} + \frac{1}{R_c} + \frac{1}{R_1} & -\frac{1}{R_1} & 0 & \cdots & 0 \\\\
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
\frac{C_s}{\Delta t} T_s^t + R_{\text{net}} - LE + \frac{T_a}{R_c} \\\\
\frac{C_1}{\Delta t} T_1^t \\\\
\frac{C_2}{\Delta t} T_2^t \\\\
\vdots \\\\
\frac{C_i}{\Delta t} T_i^t - \frac{T_{\infty}}{R_{\text{i+1}}} \\\\
\end{matrix}
\right]
$$

### Deep boundary condition
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


## Convergence Validation
This section of the code implements a convergence test for surface temperatures (`fc_Tsext`) over multiple iterations. It evaluates both individual and global discrepancies between current and previous values of surface temperatures. The algorithm determines whether the simulation has converged based on defined thresholds (`eps1` for individual errors and `eps2` for average global error). If convergence criteria are not met, the process iterates until a maximum of 50 iterations.

### Principles of the Algorithm
- **Iterative Testing**: Evaluates the temperature deviations for each surface element in an iterative manner.
- **Threshold-Based Evaluation**: Compares individual and global deviations against predefined thresholds (`eps1` and `eps2`).
- **Dynamic Updates**: Tracks and updates the number of non-converged elements across iterations.
- **Final Convergence Check**: Determines if the simulation can stop based on the percentage of non-converged elements (`ratio_face_non_cv`).
- **Maximum Iterations**: Caps the number of iterations at 50 to avoid infinite loops and reduce computational cost.

### Code Variables
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

<p align="center"><b>Figure 3: Convergence Validation Process.</b></p>

## Update surface temperature

## Long-wave radiation calculation (Net)
After obtain the new surface temperature, we need to also update the long-wave radiation emitting from the surface and again calculate the net long-wave radiation for each surface.

SOLENE introduces a `calc_GLO` function for calculating the net long-wave radiation. As describe in the follow equation, the net long-wave radiation equals to the radiation you recieve minus the radiation you emit:

$$
GLO_net = GLO_resu - GLO_emi
$$

where $GLO$ is the long-wave radiation (Grande Longueur d’Onde).
The long-wave radiation for each surface recieve from the atmosphere $GLO_atm$ and the surrounding surfaces $GLO_env$, which are calculated as follow:

$$
GLO_atm = SVF \cdot \Sigma \cdot \Epsilon \cdot T_air^4
$$

where $\Sigma$ is steph constant value, equals to $5.67e-8$;
$\Epsilon$ is the emissivity of the surface;
$SVF$ is the sky view factor;
$T_air$ is the air temperature.
