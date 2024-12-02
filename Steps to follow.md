# Steps to Follow - How Convection and Conduction Influence the Temporal Variation of Surface Temperatures
*Special thanks to Auline for providing the detailed simulation scenarios and files that made this project possible.*
## Reference Simulation with Solene

- Use the default model for the conduction transfer through urban surfaces (`simulation_Ts_EnergieBat.exe`) and no airflow.
- Use the ASHRAE correlation (5.7 + 3.8 * v) [link](https://cerema.app.box.com/file/1592730894436)[1] + wind taken at 10m.
- In the meteo file, you should use the weather file corresponding to your site (the one you are using currently) but correct the wind intensity: a wind below 0.5m/s should be fixed to 0.5m/s.

You can do this by adding these lines to your Python script:

```python
for i in range(0, len(sim.TimeStep.liste_ts_sol)):
    if sim.meteo_liste[i]['v'] < 0.5:
        sim.meteo_liste[i]['v'] = 0.5
````
**Note:**

Simulation period: 5 days, 1-hour time step, Tinit set to the first temperature in the weather file.
Reference script for piloting Solene simulations: [link](https://cerema.app.box.com/file/1592773849613).

## Simulation Scenario 2: Testing Different Conduction Models Through Soil and Walls (Baptiste Bouyer and Marie Helene Azam)

Change one model at a time:

- **BB4** Replace `simulation_Ts_EnergieBat.exe` with `simulation_Ts_EnergieBatBB4.exe` (which is a model of Baptiste; don't forget to replace the py codes, access given here: [link](https://cerema.app.box.com/folder/250767419663)) and no airflow.
- **BB5** Replace `simulation_Ts_EnergieBat.exe` with `simulation_Ts_EnergieBatBB5.exe` (which is a model of Baptiste, access here: [link](https://cerema.app.box.com/folder/250767419663)) and no airflow.
- **MHA** Replace `simulation_Ts_EnergieBat.exe` with `simulation_Ts_EnergieBat_new.exe` (which is the model of MH Azam, modified version available here: [link](https://cerema.app.box.com/folder/275394700098)) and no airflow. It is also necessary to change the `pySolene` directory. To use MH Azam's soil model, you need to change the soil class from `sol` to `sol_new` in the file `famille`.

**Note:**

- Documents describing Baptiste's model: [link](https://cerema.app.box.com/file/1454813073067).
- Documents describing MH Azam's model: [link](https://hal.science/hal-01629430v1/file/urban-soil-model_V1.pdf)[2].

## Simulation Scenario 3: Testing Different Convective Heat Transfer Coefficients (CHTC) Correlations for Wall and Roof

Change one correlation at a time:

- **"01"** Keep the default model for the conduction transfer through urban surfaces (`simulation_Ts_EnergieBat.exe`) and no airflow + wind taken at 10m. Wind intensity below 0.5m/s should be fixed to 0.5m/s.
- **"02"** Use MH Azam correlation for walls, roofs, and ground, it applies the Nusselt model as shown in follow table(script for calculation of $h_c$ in Python: [link](https://cerema.app.box.com/file/1557148585662)).
### Calcul des nombres caractéristiques
$$ Re = \frac{V_{air} \cdot L}{v}
Ba = \frac{1}{T_{air} + 273}
Gr = \frac{Ba \cdot g \cdot L^3 \cdot |T_{surf} - T_{air}|}{v^2} $$

| Type de convection | Régime de l’écoulement | Condition de validité                | Formule pour \( h \)                               |
|---------------------|------------------------|---------------------------------------|---------------------------------------------------|
| Libre              | Laminaire             | $Re^2 << Gr$ et $Gr < 10^9$ | $h = \frac{\lambda}{L} \cdot 0.49 \cdot Gr^{\frac{1}{4}}$ |
| Libre              | Turbulent             | $Re^2 << Gr$ et $Gr \geq 10^9$ | $h = \frac{\lambda}{L} \cdot 0.13 \cdot Gr^{\frac{1}{3}}$ |
| Forcée             | Laminaire             | $Re^2 >> Gr$ et $Gr < 10^9$ | $h = \frac{\lambda}{L} \cdot 0.56 \cdot Re^{\frac{1}{2}}$ |
| Forcée             | Turbulent             | $Re^2 >> Gr$ et $Gr \geq 10^9$ | $h = \frac{\lambda}{L} \cdot 0.03 \cdot Re^{\frac{4}{5}}$ |
| Mixte              | Laminaire             | $10 \cdot Re^2 \approx Gr$ et $Gr < 10^9$ | $h = \frac{\lambda}{L} \cdot 0.68 \cdot \left( 0.57 \cdot Gr^{\frac{3}{4}} + Re^{\frac{3}{2}} \right)^{\frac{1}{3}}$ |
| Mixte              | Turbulent             | $10 \cdot Re^2 \approx Gr$ et $Gr \geq 10^9$ | $h = \frac{\lambda}{L} \cdot 0.03 \cdot \left( 12.1 \cdot Gr + Re^{\frac{12}{5}} \right)^{\frac{1}{3}}$ |

- **"03"** Use Montazeri [link](https://cerema.app.box.com/file/1557062701832)[3], script for calculation of $h_c$ in Python [link](https://cerema.app.box.com/file/1592767323891) for roofs and walls (differentiating leeward, windward, and side facades according to the main wind direction) and use Vehrencamp model (second version with $a_c = 1.4$ and $d_c = 0.5$, you can find the equation here: [link](https://cerema.app.box.com/file/1593887985213)[4]) for ground.
- **"04"** Use Denby model, which estimates the convection coefficient using the atmospheric density ($\rho_a$), heat capacity of dry air ($c_{pair}$), and aerodynamic resistance for temperature ($r_T$) [link](https://cerema.app.box.com/file/1593887985213)[4], with:

$$
\rho_a = 1.2 \, \text{kg/m}^3, \quad c_{pair} = 1006 \, \text{J/(K·kg)}
$$

$$
r_T = \frac{\log(10/z_0) \cdot \log(10/(z_0/10))}{v \cdot 0.16} \, \text{(s/m)}
$$
  
  as described in [link](https://cerema.app.box.com/file/1601751411797)[5] for wall, roof, and ground.

## Selected Outputs

Please, for each simulation, select the surface temperature of at least 2 walls (e.g., in a canyon), 1 ground, and 1 roof. Show the temporal evolution for these selected surfaces for the 5 days selected for each scenario (7 in total).

References

1. Odunfa, K. M., C. J. Nnakwe, and V. O. Odunfa. "Building energy efficiency in Nigeria major climatic zones." Journal of Building Construction and Planning Research 6.4 (2018): 251-266.
2. Azam, Marie-Hélène, et al. "A new urban soil model for SOLENE-microclimat: Review, sensitivity analysis and validation on a car park." Urban climate 24 (2018): 728-746.
3. Montazeri, Hamid, and Bert Blocken. "New generalized expressions for forced convective heat transfer coefficients at building facades and roofs." Building and Environment 119 (2017): 153-168.
4. Chen, Jiaqi, Hao Wang, and Pengyu Xie. "Pavement temperature prediction: Theoretical models and critical affecting factors." Applied thermal engineering 158 (2019): 113755.
5. Denby, Bruce Rolstad, et al. "A coupled road dust and surface moisture model to predict non-exhaust road traffic induced particle emissions (NORTRIP). Part 2: Surface moisture and salt impact modelling." Atmospheric Environment 81 (2013): 485-503.
