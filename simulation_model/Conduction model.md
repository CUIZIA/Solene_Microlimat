# Conduction Model - SOLENE THERMAL MODEL

SOLENE-Microclimat 模型是耦合了基于SOLENE的辐射、热模型以及Code_Saturne的流体力学模型。根据表面的类型分为不同的热辐射平衡方案：不透水地面、植被地面和建筑物墙壁（这里我们只详细解释不透水地面的情况，只考虑热传递而忽略湿气传递）。另外在此模型是一维的，所以

地面热传导模型采用的是Marie-Hélène Azam开发的土壤模型，她提出的土壤模型是为路面涂层等不透水表面设计的。因此，只考虑热传递（忽略水分传递）。土壤模型是一维的，其中每层都有自己的特性。在非稳定状态下，温度波动是根据方程 (1) 计算的，这是热方程在一维问题中的应用。SOLENE中的热传导的核心是使用电类比的隐式差分形式来求解。热阻代表了通过地面层的热传递阻力，热容代表了地面层的热存储能力，如图1所示。土壤模型由n个节点组成。

The general heat conduction equation in soil can be written as:

$$
\frac{\partial T}{\partial t} = \alpha_{\text{soil}} \frac{\partial^2 T}{\partial x^2}
$$

Where:

- $T$ is the temperature $[K]$.
- $t$ is the time $[s]$.
- $x$ is the spatial coordinate $[m]$.
- $\alpha_{\text{soil}}$ is the thermal diffusivity of the soil $[m^2/s]$.

将土壤分解为n层，我们可以分3种情况考虑，包括：（1）土壤与空气接触的边界条件；（2）土壤内部节点 $i$；（3）深层土壤的边界条件。

<p align="center">
  <img src="./Conduction_MHA.png" alt="Figure 1: Schematic representation of the soil model." width="25%">
</p>

<p align="center"><b>Figure 1: Schematic representation of the soil model.</b></p>


（1）能量平衡方程在表面节点 (i = 0) 处计算，需要考虑潜热和辐射。

$$
C_s \frac{dT_s}{dt} + \frac{T_s - T_a}{R_c} + \frac{T_s - T_1}{R_1} = R_{\text{net}}  - L E
$$

Where:

- $C_s$ is the surface layer heat capacity $[J/m^2K]$.
- $T_s$ is the surface temperature $[K]$.
- $T_1$ is the temperature at the first node beneath the surface $[K]$.
- $T_a$ is the air temperature $[K]$.
- $R_c$ is defined as $R_c = \frac{1}{h_c}$, where $h_c$ is the convective heat transfer coefficient.
- $R_1$ is the heat resistance between the surface and the first node $[K/W]$.
- $R_{\text{net}}$ is the net radiation $[W/m^2]$.
- $LE$ is the latent heat flux $[W/m^2]$.

（2）能量平衡方程在内部节点 $i$ 处计算：

$$
C_i\frac{dT_i}{dt} + \frac{T_i-T_{\text{i+1}}}{R_{\text{i+1}}} - \frac{T_{\text{i-1}}-T_i}{R_i} = 0
$$

Where:

- $C_i$ is the heat capacity of the layer at the node $i$ $[J/m^2K]$.
- $T_i$ is the temperature of the node $i$ $[K]$.
- $R_i$ is the heat resistance of the layer between the node $i-1$ and $i$ $[K/W]$.

（3）能量方程在底部边界条件的计算：

$$
C_i\frac{dT_i}{dt} + \frac{T_i-T_{\infty}}{R_{\text{i+1}}} - \frac{T_{\text{i-1}}-T_i}{R_i} = 0
$$

Where:

- $T_{\infty}$ is the deep soil temperature $[K]$.



## test
### Implicit Finite Element Discretization for the Soil Model

We consider the soil model divided into \(n\) layers, and we solve the heat conduction problem using the implicit finite element method (FEM). The model consists of three parts:

1. Surface boundary condition (soil-air interface),
2. Internal nodes,
3. Deep soil boundary condition.

### (1) Surface Boundary Condition (Soil-Air Interface)

At the surface node \(i = 0\), the energy balance equation accounts for latent heat, radiation, and conduction between the surface and the first layer beneath it:

$$
C_s \frac{dT_s}{dt} + \frac{T_s - T_a}{R_c} + \frac{T_s - T_1}{R_1} = R_{\text{net}} - L E
$$

In matrix form, this equation can be discretized using the implicit time-stepping method. Assuming \(T_s^n\) is the temperature at the current time step and \(T_s^{n+1}\) is at the next time step:

$$
C_s \frac{T_s^{n+1} - T_s^n}{\Delta t} + \frac{T_s^{n+1} - T_a}{R_c} + \frac{T_s^{n+1} - T_1^{n+1}}{R_1} = R_{\text{net}} - L E
$$

This forms part of the matrix system where \(T_s^{n+1}\) depends on the surface and the first internal node.

### (2) Internal Nodes

For internal nodes \(i\), the energy balance equation is:

$$
C_i \frac{dT_i}{dt} + \frac{T_i - T_{\text{i+1}}}{R_{\text{i+1}}} - \frac{T_{\text{i-1}} - T_i}{R_i} = 0
$$

Using the implicit method, this can be written as:

$$
C_i \frac{T_i^{n+1} - T_i^n}{\Delta t} + \frac{T_i^{n+1} - T_{\text{i+1}}^{n+1}}{R_{\text{i+1}}} - \frac{T_{\text{i-1}}^{n+1} - T_i^{n+1}}{R_i} = 0
$$

### (3) Deep Soil Boundary Condition

At the deep soil boundary, the temperature is assumed to approach a constant \(T_\infty\). The energy balance equation at the bottom node \(i = n\) is:

$$
C_i \frac{dT_i}{dt} + \frac{T_i - T_{\infty}}{R_{\text{i+1}}} - \frac{T_{\text{i-1}} - T_i}{R_i} = 0
$$

In implicit form:

$$
C_i \frac{T_i^{n+1} - T_i^n}{\Delta t} + \frac{T_i^{n+1} - T_{\infty}}{R_{\text{i+1}}} - \frac{T_{\text{i-1}}^{n+1} - T_i^{n+1}}{R_i} = 0
$$

### Assembling the Matrix System

The soil model with \(n\) layers forms a system of equations that can be written in matrix form as:

$$
\mathbf{C} \frac{\mathbf{T}^{n+1} - \mathbf{T}^n}{\Delta t} + \mathbf{A} \mathbf{T}^{n+1} = \mathbf{b}
$$

Where:

- \(\mathbf{C}\) is the heat capacity matrix (diagonal),
- \(\mathbf{A}\) is the matrix representing thermal resistances between the nodes,
- \(\mathbf{T}^{n+1}\) is the temperature vector at the next time step,
- \(\mathbf{b}\) is the vector containing boundary conditions (radiation, latent heat, etc.).

For a soil model with \(n\) layers, the matrix form can be expressed as:

$$
\left[
\begin{matrix}
C_s + \frac{1}{R_c} + \frac{1}{R_1} & -\frac{1}{R_1} & 0 & \cdots & 0 \\\\
-\frac{1}{R_1} & C_1 + \frac{1}{R_1} + \frac{1}{R_2} & -\frac{1}{R_2} & \cdots & 0 \\\\
0 & -\frac{1}{R_2} & C_2 + \frac{1}{R_2} + \frac{1}{R_3} & \dots & 0 \\\\
\vdots & \vdots & \vdots & \ddots & \vdots \\\\
0 & \dots & 0 & -\frac{1}{R_n} & C_n + \frac{1}{R_n} \\\\
\end{matrix}
\right]
$$

$$
\left[
\begin{matrix}
C_s + \frac{1}{R_c} + \frac{1}{R_1} & -\frac{1}{R_1} & 0 & \cdots & 0 \\\\
-\frac{1}{R_1} & C_1 + \frac{1}{R_1} + \frac{1}{R_2} & -\frac{1}{R_2} & \cdots & 0 \\\\
0 & -\frac{1}{R_2} & C_2 + \frac{1}{R_2} + \frac{1}{R_3} & \cdots & 0 \\\\
\vdots & \vdots & \vdots & \ddots & \vdots \\\\
0 & \cdots & 0 & -\frac{1}{R_n} & C_n + \frac{1}{R_n} \\\\
\end{matrix}
\right]
\left[
\begin{matrix}
T_s^{n+1} \\\\
T_1^{n+1} \\\\
T_2^{n+1} \\\\
\vdots \\\\
T_n^{n+1} \\\\
\end{matrix}
\right]
\left[
\begin{matrix}
R_{\text{net}} - LE + \frac{T_a}{R_c} \\\\
0 \\\\
0 \\\\
\vdots \\\\
\frac{T_{\infty}}{R_{n+1}} \\\\
\end{matrix}
\right]
$$

