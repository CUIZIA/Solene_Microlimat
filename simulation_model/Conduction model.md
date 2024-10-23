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

将土壤分解为n层，我们可以分3种情况考虑，包括：（1）土壤与空气接触的边界条件；（2）土壤内部节点 \(i\)；（3）深层土壤的边界条件。

（1）能量平衡方程在表面节点 \(i = 0\) 处计算，需要考虑潜热和辐射。

$$
C_s \frac{dT_s}{dt} + \frac{T_s - T_a}/R_c + \frac{T_s - T_1}{R_1} = R_{\text{net}}  - L E
$$

Where:

- $C_s$ is the surface layer heat capacity $[J/m^2K]$.
- $T_s$ is the surface temperature $[K]$.
- $T_1$ is the temperature at the first node beneath the surface $[K]$.
- $T_a$ is the air temperature $[K]$.
- $R_c$ is defined as $R_c = \frac{1}{h_c}$, where $h_c$ is the convective heat transfer coefficient $[W/m²K]$.
- $R_1$ is the thermal resistance between the surface and the first node $[K/W]$.
- $R_{\text{net}}$ is the net radiation $[W/m^2]$.
- $LE$ is the latent heat flux $[W/m^2]$.
