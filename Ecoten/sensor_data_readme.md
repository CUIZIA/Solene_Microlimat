# Creating the .md content with the relevant table and important information in markdown format

md_content = """
# README for Sensor Data at Pražská Holešovická Tržnice

## Overview

This file contains environmental sensor data from **Pražská Holešovická Tržnice**, specifically from the sensor located at the public lighting system. The location is described as an **area without greenery (areál bez zeleně)**, with a **surface of asphalt/concrete (asfalt/beton)**, and the **orientation is east-west (východ-západ)**. The geographic coordinates of the location are:

- **Latitude**: 50.0989344
- **Longitude**: 14.4450222

The sensor records several environmental parameters at two different heights: 200 cm and 50 cm above ground level. The measurements include air humidity, air temperature, atmospheric pressure, and more.

## Location Information
- **Point Name**: Pražská tržnice osvětlení
- **Location**: Pražská Holešovická tržnice
- **Description**: Area without greenery (areál bez zeleně)
- **Surface**: Asphalt/Concrete (asfalt/beton)
- **Orientation**: East-West (východ-západ)
- **Coordinates**: 
  - Latitude: 50.0989344
  - Longitude: 14.4450222
- **Sensor Position**: Public lighting (veřejné osvětlení)
- **Sensor Detail**: Located at public lighting in the center of the market area (veřejné osvětlení ve středu Tržnice)

## Measurements

The following measurements are recorded by the sensor:

| Measure         | Description (Czech)                   | Unit  | Measurement Height |
|-----------------|---------------------------------------|-------|--------------------|
| air_hum200      | Air humidity, 200 cm (Vlhkost vzduchu, 200 cm) | %     | 200 cm             |
| air_hum50       | Air humidity, 50 cm (Vlhkost vzduchu, 50 cm)  | %     | 50 cm              |
| air_temp200     | Air temperature, 200 cm (Teplota vzduchu, 200 cm) | °C    | 200 cm             |
| air_temp50      | Air temperature, 50 cm (Teplota vzduchu, 50 cm)  | °C    | 50 cm              |
| precip300       | Precipitation, 300 cm (Úhrn srážek, 300 cm)     | mm    | 300 cm             |
| pressure200     | Atmospheric pressure, 200 cm (Atmosférický tlak, 200 cm) | Pa    | 200 cm             |
| pressure50      | Atmospheric pressure, 50 cm (Atmosférický tlak, 50 cm)  | Pa    | 50 cm              |
| sun_irr200      | Solar radiation, 200 cm (Sluneční záření, 200 cm)  | lux   | 200 cm             |
| wind_dir300     | Wind direction, 300 cm (Směr větru, 300 cm)      | °     | 300 cm             |
| wind_impact300  | Wind gust, 300 cm (Náraz větru, 300 cm)          | km/h  | 300 cm             |
| wind_speed300   | Wind speed, 300 cm (Rychlost větru, 300 cm)      | km/h  | 300 cm             |

## Data Format

Each measurement contains a unique identifier (`measure`), a Czech description (`measure_cz`), and the respective unit (`unit`). Measurements are made at different heights, as indicated in the table above.

## Usage

This dataset can be used for studying environmental conditions such as humidity, temperature, wind speed, and solar radiation in urban environments. It can also be used in microclimate analysis, especially in locations with limited greenery and mostly asphalt/concrete surfaces.

## License

Specify the applicable license for this dataset (if any).
"""

# Saving the content to a markdown file
file_path = '/mnt/data/sensor_data_readme.md'
with open(file_path, 'w') as md_file:
    md_file.write(md_content)

file_path
