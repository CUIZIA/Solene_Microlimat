# SOLENE Microclimat - Weather Data Automation

This section provides practical solutions for automating the weather data conversion process required by SOLENE Microclimat. 
It introduces two scripts `generate_meteo.py` and `csv2meteo.py` to help users quickly format large meteorological datasets into the required format compatible with SOLENE simulations.

&nbsp;

## Important Note

All weather files must be provided in the **local time** of the study area, specifically in **True Solar Time (TST)**.
SOLENE currently does not have an automatic time conversion feature. Additionally, please ensure that the weather data timestep is **greater than 5 minutes**. 
If the timestep is less than 5 minutes, SOLENE will not run the simulation. To shorten the weather data timestep, you can adjust the `HMAX_METEO` parameter to **>288**.

&nbsp;

## 1. Example Weather File Format for SOLENE
Below is an example of a correctly formatted weather file:

```
jour heure vitesse_vent direction_vent global infrarouge Tair HR Patm qs Pluvio te
"2010/01/01 01:00:00" 3.51313040649298 23.0829021489665 0 329.434833333333 4.09516166666667 88.882 989.241833333333 4.59006787323852 0 8.32
"2010/01/01 02:00:00" 3.88484845773298 25.6666643289665 0 329.434833333333 5.87384782223467 90.842 989.241833333333 4.59006787323852 0 8.32
"2010/01/01 03:00:00" 3.47462728239498 24.0544903489665 0 329.434833333333 4.09483320666667 89.222 989.241833333333 4.59006787323852 0 8.32
```

### Column Descriptions:

<div align="center">

| Column         | Description                  |
|----------------|------------------------------|
| `jour`         | Date (YYYY/MM/DD)            |
| `heure`        | Time (HH:MM:SS)              |
| `vitesse_vent` | Wind speed (m/s)             |
| `direction_vent` | Wind direction (degrees)   |
| `global`       | Global Horizontal Irradiation (GHI) |
| `infrarouge`   | Infrared radiation           |
| `Tair`         | Air temperature (°C)         |
| `HR`           | Relative Humidity (%)        |
| `Patm`         | Atmospheric pressure (hPa)   |
| `qs`           | Specific humidity (%)        |
| `Pluvio`       | Precipitation (mm?)           |
| `te`           | Set to `0`                    |

</div>

&nbsp;

## 2. Weather File Formats in SOLENE

The weather input files in SOLENE must follow a **unified format**. However, large meteorological datasets often require automated processing methods.
Here are **two recommended approaches** for quickly converting your weather data into the required format:

- **Using `generate_meteo.py`**:  
   If your weather data comes from **Météo France** (accessible from [Météo France Open Data](https://meteo.data.gouv.fr/datasets?topic=6571f26dc009674feb726be9)), you can use the **`generate_meteo.py`** script developed by Alexandre.

- **Using `csv2meteo.py`**:  
   If you prefer to work with **Excel/CSV data**, you can use the **`csv2meteo.py`** script that I developed.
  This method allows you to quickly convert your CSV weather files into the required format for SOLENE.

### 2.1 Using `generate_meteo.py`

If you download weather data from [Météo France Open Data](https://meteo.data.gouv.fr/datasets?topic=6571f26dc009674feb726be9), 
it is recommended to choose the **“Données climatologiques de base – horaires”** dataset (the times are expressed in UTC for mainland France and in FU for overseas territories).
Below is a table explaining the key variables and their meanings:

<div align="center">

| Variable       | Description                                                  |
|----------------|--------------------------------------------------------------|
| `AAAAMMJJHH`   | Date of the measurement (Year, Month, Day, Hour)             |
| `FF`           | Wind speed averaged over 10 minutes, measured at 10 m height (in m/s, scaled by 1/10) |
| `DD`           | Wind direction corresponding to `FF` (on a 360° rose scale)   |
| `GLO`          | Global hourly solar radiation in UTC time (in J/cm²)          |
| `GLO2`         | Global hourly solar radiation in True Solar Time (in J/cm²)   |
| `T`            | Instantaneous air temperature (in °C, scaled by 1/10)         |
| `U`            | Relative humidity (in %)                                      |
| `PSTAT`        | Station pressure (in hPa, scaled by 1/10)                     |
| `qs`           | Set to `0`                                                    |
| `Pluvio`       | Set to `0`                                                    |
| `te`           | Set to `0`                                                    |

</div>
