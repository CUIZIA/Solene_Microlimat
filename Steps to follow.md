# Steps to Follow - How Convection and Conduction Influence the Temporal Variation of Surface Temperatures

Each of us continues working on his geometry and data.

## Reference Simulation with Solene

- Use the default model for the conduction transfer through urban surfaces (`simulation_Ts_EnergieBat.exe`) and no airflow.
- Use the Jayamaha correlation (5.7 + 3.8 * v) [link](https://cerema.app.box.com/file/1592730894436) + wind taken at 10m.
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

- **2.1** Replace `simulation_Ts_EnergieBat.exe` with `simulation_Ts_EnergieBatBB4.exe` (which is a model of Baptiste; don't forget to replace the py codes, access given here: [link](https://cerema.app.box.com/folder/250767419663)) and no airflow.
- **2.2** Replace `simulation_Ts_EnergieBat.exe` with `simulation_Ts_EnergieBatBB5.exe` (which is a model of Baptiste, access here: [link](https://cerema.app.box.com/folder/250767419663)) and no airflow.
- **2.3** Replace `simulation_Ts_EnergieBat.exe` with `simulation_Ts_EnergieBat_new.exe` (which is the model of MH Azam, modified version available here: [link](https://cerema.app.box.com/folder/275394700098)) and no airflow. It is also necessary to change the `pySolene` directory. To use MH Azam's soil model, you need to change the soil class from `sol` to `sol_new` in the file `famille`.

**Note:**

- Documents describing Baptiste's model: [link](https://cerema.app.box.com/file/1454813073067).
- Documents describing MH Azam's model: [link](https://hal.science/hal-01629430v1/file/urban-soil-model_V1.pdf).

