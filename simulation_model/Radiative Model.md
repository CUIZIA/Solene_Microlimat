# SOLENE Microclimat - RADIATIVE MODEL

The radiation model in SOLENE-Microclimat is the first and one of the most critical components of the simulation chain. During runtime, SOLENE separates computations into two categories: time-dependent and time-independent processes.

The radiation simulation is highly time-dependent, as it is directly influenced by the position of the sun at each time step. Solar angles, shadows, and sky conditions all vary with time, making accurate temporal handling essential for reliable radiation results.

In contrast, the thermal model is not directly time-driven in the same way. While it does perform iterative computations at each time step, it is primarily focused on the thermal inertia and energy balance within materials, rather than being influenced by dynamic external conditions like solar position. Thus, it operates within each time iteration, but its behavior is more tied to internal heat transfer dynamics than to external temporal variables.

## Handling Time Offsets in SOLENE: Conversion to True Solar Time (TSV)

In Julien's paper, it is noted that:

> “*Notons que le renseignement des horaires de simulation se fait en Temps Solaire Vrai (TSV)*.”

This means that SOLENE expects simulation times to be provided in **True Solar Time (TSV)**. Therefore, if the time standard used in your weather input file is **not** TSV (e.g., legal time like UTC+1 or UTC+2), it can cause **errors in the shortwave radiation simulation**. Furthermore, the **output timestamps** of the simulation may not align with the **measured time standard**, potentially leading to inconsistencies during validation.

Although SOLENE includes built-in scripts `tsv2tl` and `tl2tsv` in Python to convert between legal time and solar time based on geographic location, the actual simulation relies on **compiled `.exe` binaries** for performance. To ensure that the **output time format remains consistent with the input**, I chose to apply the time offset **within the compiled C code** itself.

### Modified Files

* **`masque_sol.c`**:
  Simulates when each surface in the scene receives **direct sunlight** or is **shaded** by other geometry throughout the day.

* **`luminance_ciel_temps.c`**:
  Simulates the **sky dome's anisotropic luminance distribution** based on geometric and radiative properties, using solar position and solid angles to compute **diffuse radiation**.


| Module                   | Purpose                                                                                   | Output Folder | Filename Format                  |
| ------------------------ | ----------------------------------------------------------------------------------------- | ------------- | -------------------------------- |
| `masque_sol.c`           | Records time intervals when each surface receives or is blocked from **direct sunlight**  | `masque/`     | `masque_<day>_<month>`           |
| `luminance_ciel_temps.c` | Stores **sky luminance data** over a hemisphere using solar position and angular geometry | `ciel/`       | `luminance_<day>_<month>_<time>` |

