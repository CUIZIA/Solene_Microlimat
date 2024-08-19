# Wind Speed Distribution Model

## Project Overview

This project models the distribution of wind speed with respect to height, taking into account **vertical wind shear**—the phenomenon where wind speed changes with altitude. The model is based on the logarithmic wind profile law, which also considers the effect of surface roughness on wind speed distribution.

## Wind Speed Distribution Formula

The relationship between wind speed at different heights can be described using the following logarithmic formula:

$$
\frac{v(z)}{v_{\text{ref}}} = \frac{\ln\left(\frac{z}{z_0}\right)}{\ln\left(\frac{z_{\text{ref}}}{z_0}\right)}
$$

Where:

- $$\( v(z) \)$$ is the wind speed at height $$\( z \)$$
- $$\( v_{\text{ref}} \)$$ is the wind speed at the reference height $$\( z_{\text{ref}} \)$$
- $$\( z_0 \)$$ is the surface roughness length

## Surface Roughness Length Values $$\( z_0 \)$$

The surface roughness length $$\( z_0 \)$$ varies depending on the type of terrain:

| Roughness Class | Roughness Length $$\( z_0 \)$$ | Land Cover Types                                                                 |
|-----------------|----------------------------|----------------------------------------------------------------------------------|
| 0               | 0.0002 m                   | Water surfaces: seas and lakes                                                   |
| 0.5             | 0.0024 m                   | Open terrain with smooth surface, e.g., concrete, airport runways, mown grass, etc. |
| 1               | 0.03 m                     | Open agricultural land without fences and hedges; maybe some far-apart buildings and very gentle hills |
| 1.5             | 0.055 m                    | Agricultural land with a few buildings and 8 m high hedges separated by more than 1 km |
| 2               | 0.1 m                      | Agricultural land with a few buildings and 8 m high hedges separated by approx. 500 m |
| 2.5             | 0.2 m                      | Agricultural land with many trees, bushes, and plants, or 8 m high hedges separated by approx. 250 m |
| 3               | 0.4 m                      | Towns, villages, agricultural land with many or high hedges, forests, and very rough and uneven terrain |
| 3.5             | 0.6 m                      | Large towns with high buildings                                                  |
| 4               | 1.6 m                      | Large cities with high buildings and skyscrapers                                  |


By adjusting the surface roughness length $$\( z_0 \)$$, the model can simulate wind speed distribution in different environments. In our case, our study area situated in a village near Paris so I picked 0.4m as the roughness length.
