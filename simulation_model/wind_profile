\documentclass{article}
\usepackage{amsmath}

\begin{document}

\title{Wind Speed Distribution Model}
\author{}
\date{}
\maketitle

\section*{Project Overview}

This project models the distribution of wind speed with respect to height, taking into account \textbf{vertical wind shear}---the phenomenon where wind speed changes with altitude. The model is based on the logarithmic wind profile law, which also considers the effect of surface roughness on wind speed distribution.

\section*{Wind Speed Distribution Formula}

The relationship between wind speed at different heights can be described using the following logarithmic formula:

\[
\frac{v(z)}{v_{\text{ref}}} = \frac{\ln\left(\frac{z}{z_0}\right)}{\ln\left(\frac{z_{\text{ref}}}{z_0}\right)}
\]

Where:

\begin{itemize}
    \item \( v(z) \) is the wind speed at height \( z \)
    \item \( v_{\text{ref}} \) is the wind speed at the reference height \( z_{\text{ref}} \)
    \item \( z_0 \) is the surface roughness length
\end{itemize}

\section*{Surface Roughness Length Values \( z_0 \)}

The surface roughness length \( z_0 \) varies depending on the type of terrain:

\begin{table}[h!]
\centering
\begin{tabular}{|c|c|}
\hline
\textbf{Surface Type} & \( \mathbf{z_0} \) \textbf{(meters)} \\
\hline
Open water & 0.0002 \\
Short grass & 0.03 \\
Farmland & 0.1 \\
Urban area & 1.0 \\
Forest & 1.3 \\
\hline
\end{tabular}
\end{table}

By adjusting the surface roughness length \( z_0 \), the model can simulate wind speed distribution in different environments. This model is particularly useful for studies related to wind farm siting and other wind energy applications.

\section*{Usage Example}

You can calculate the wind speed at a certain height using the following Python code:

\begin{verbatim}
import numpy as np

def wind_speed_at_height(z, v_ref, z_ref, z_0):
    return v_ref * np.log(z / z_0) / np.log(z_ref / z_0)

# Example parameters
z = 50  # Target height (meters)
v_ref = 10  # Wind speed at reference height (m/s)
z_ref = 10  # Reference height (meters)
z_0 = 0.03  # Surface roughness for short grass (meters)

v_z = wind_speed_at_height(z, v_ref, z_ref, z_0)
print(f"Wind speed at {z} meters: {v_z:.2f} m/s")
\end{verbatim}

\end{document}
