<div align="center">

<!-- logo -->
<p align="center">
  <img src="/fig/logo.png" width="250px" style="vertical-align:middle;">
</p>

<!-- language -->

[English](README.md) | [Français](README_fr-FR.md)

</div>

# Changelog

- 20/01/2025 [SOLENE-Microlimat Mixture](https://cerema.app.box.com/folder/303647315869) released. In my BPE colleague's research, it was observed that the
  3R4C model for simulating urban building surface temperatures appears to be a good compromise between
  accuracy and complexity. Therefore, we combined the finite differences conductive model for the ground
  with the 3R4C model for building surfaces. We refer to the integrated model as ‘simulation_Ts_EnergieBat_mixture’,
  which has been shared on Box for download and review, including the source code.
  
<!-- Table of content -->

<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li><a href="#Introduction">Introduction</a></li>
    <li><a href="#Key Features">Key Features</a></li>
    <li><a href="#Installation">Installation</a></li>
    <li>
      <a href="#Quick Start">Quick Start</a>
      <ul>
        <li><a href="#input files">Input Files</a></li>
        <li><a href="#solar radiation">Solar Radiation</a></li>
        <li><a href="#thermal model">Thermal Model</a></li>
        <li><a href="#couplage">Coupling with Saturne</a></li>
        <li><a href="#output files">Output Files</a></li>
      </ul>
    </li>
    <li><a href="#acknowledgments">Acknowledgements</a></li>
  </ol>
</details>

&nbsp;

# SOLENE-Microclimat

## Introduction

Welcome to the Solene-Microclimat Code Repository! This repository is dedicated to storing, organizing, 
and managing various code snippets and projects designed for the Solene-Microclimat simulation tool. 
Solene-Microclimat enables the calculation of thermal balances for urban surfaces and buildings using 
digital models and simulates urban climates at the neighborhood scale. Additionally, this repository 
provides guidance on downloading, using, and improving Solene-Microclimat. Special thanks to the CEREMA BPE 
team for their collaborative efforts.

## Key Features

- Includes sub-models for:  
  - Radiation transfer  
  - Conduction and storage in walls and floors  
  - Airflow and convective exchanges  
  - Evapotranspiration of natural surfaces such as vegetation and water bodies  
  - Energy simulations of buildings within the modeled area (energy demand or indoor temperature)  
- Simulates surface temperatures of urban blocks  
- Coupling with FLUENT software (CFD)  
- Evaluation of outdoor comfort  

## Installation

All the installation steps you might need are summarized in the [Install.md](Install.md) file.

> [!WARNING]
> **Pre-installation Notice—Hardware and Software Environment Support**
> 
> To ensure the stability and reliability of the project, we have optimized and tested it only for specific software and hardware environments during development. Due to legacy issues, we are working on migrating our development language to a newer version. Hopefully, in the near future 🤞.
> 
> Due to the diversity of hardware and software configurations, as well as compatibility issues with third-party dependencies, we cannot guarantee full functionality of the project with 100% certainty. Therefore, for users who wish to use this project in non-recommended environments, we suggest thoroughly reviewing the documentation beforehand. Additionally, we encourage users to report any issues they encounter, allowing us to gradually expand the range of supported environments.

<div align="center">
  
| Operating System | Ubuntu 20.04+   | Windows 10 Pro   |
|----------------|-----------------|------------------|
| CPU            | Intel i5 4 cores+ | Intel i5 4 cores+ |
| Memory         | 8GB+            | 8GB+            |
| Storage        | 100GB+ SSD       | 100GB+ SSD       |
| Python Version | 2.7      | 2.7       |

</div>
