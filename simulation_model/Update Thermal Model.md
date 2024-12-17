# How to Replace the Built-in SOLENE Thermal Model Executable File

This document provides step-by-step instructions for updating and replacing the **thermal model** executable file in SOLENE. The process includes changing the environment configuration, and replacing the `.exe` file within the SOLENE directory.

## 1. Update the Simulation Environment

If you replace the entire `pySolene` directory, open **terminal** in the folder and run the following commands:

```bash
sudo cp -r pySolene /opt/solene/
sudo chmod -R a+rwx /opt/solene/pySolene
```

## 2. Copy the Executable File

The core executable file (e.g. `simulation_Ts_EnergieBatBB.exe`) is responsible for the thermal model's calculations.

   ```bash
   sudo cp simulation_Ts_EnergieBatBB.exe /opt/solene/solene.core/bin/
   sudo chmod a+rwx /opt/solene/solene.core/bin/simulation_Ts_EnergieBatBB.exe
   ```
