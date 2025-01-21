<div align="center">

<!-- logo -->
<p align="center">
  <img src="/fig/logo.png" width="300px" style="vertical-align:middle;">
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
    <li><a href="#KeyFeatures">Key Features</a></li>
    <li><a href="#QuickStart">Quick Start</a></li>
    <li><a href="#input files">Input Files</a></li>
    <li><a href="#solar radiation">Solar Radiation</a></li>
    <li>
      <a href="#thermal model">Thermal Model</a>
      <ul>
        <li><a href="#3R4C">3R4C</a></li>
        <li><a href="#MHA">MHA</a></li>
        <li><a href="#hybrid model">Hybrid Model</a></li>
      </ul>
    </li>
    <li><a href="#couplage">Coupling with Saturne</a></li>
    <li><a href="#output files">Output Files</a></li>
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

## Quick Start

> [!WARNING]
> **Pre-installation Notice—Hardware and Software Environment Support**
> 
> 为了确保项目的稳定性和可靠性，我们在开发过程中仅对特定的软硬件环境进行优化和测试。这样当用户在推荐的系统配置上部署和运行项目时，能够获得最佳的性能表现和最少的兼容性问题。
>
> 通过集中资源和精力于主线环境，我们团队能够更高效地解决潜在的BUG，及时开发新功能。
>
