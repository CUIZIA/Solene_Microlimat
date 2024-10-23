# Conduction Model - SOLENE THERMAL MODEL

SOLENE-Microclimat 模型是耦合了基于SOLENE的辐射、热模型以及Code_Saturne的流体力学模型。根据表面的类型分为不同的热辐射平衡方案：不透水地面、植被地面和建筑物墙壁（这里我们只详细解释不透水地面的情况，只考虑热传递而忽略湿气传递）。另外在此模型是一维的，所以
那么
地面热传导模型采用的是Marie-Hélène Azam开发的土壤模型，她提出的土壤模型是为路面涂层等不透水表面设计的。因此，只考虑热传递（忽略水分传递）。土壤模型是一维的，其中每层都有自己的特性。在非稳定状态下，温度波动是根据方程 (1) 计算的，这是热方程在一维问题中的应用。SOLENE中的热传导的核心是使用隐式差分形式来求解。The general heat conduction equation in soil can be written as:

$$
\frac{\partial T}{\partial t} = \alpha_{soil} \frac{\partial^2 T}{\partial x^2} 
$$

Where:

- \( T \) is the temperature [K].
- \( t \) is the time [s].
- \( x \) is the spatial coordinate [m].
- \( \\alpha_{soil} \) is the thermal diffusivity of the soil [m^2/s].

This equation describes the transient heat conduction through a one-dimensional medium (e.g., soil) and is used to model how temperature changes over time and space within the soil.
