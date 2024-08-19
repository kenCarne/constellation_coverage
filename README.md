# TLE to Classical Orbital Elements Converter

This Python script reads a text file containing Two-Line Element (TLE) sets for multiple satellites and converts them to classical orbital elements (COEs). The results are written to an output text file.

## Prerequisites

### Python Libraries

The script requires the following Python library:

- **sgp4**: This library provides functions for the SGP4 satellite propagation model.

You can install the required library using pip:

```bash
pip install sgp4

## Requirements
 NASA GMAT
 
 
##GMAT Script for BlackSky's Constellation of Satellites
This GMAT script sets up and propagates a constellation of BlackSky satellites, incorporating complex force models, custom propagators, and generating visual and textual outputs to analyze satellite behavior.

##Script Overview
This script defines multiple spacecraft representing satellites in the BlackSky constellation, sets up force models for accurate propagation, and generates 3D orbit views, ground tracks, and report files.

##Components:
Spacecraft Configuration: Defines the properties of each satellite in the constellation.
Force Models: Includes atmospheric drag, gravity, solar radiation pressure (SRP), and other physical forces affecting satellite motion.
Propagators: Uses the Runge-Kutta integrator for simulating satellite motion.
Subscribers: Provides visualizations (3D orbit views, 2D ground tracks) and textual reports of satellite data.
Mission Sequence: Propagates all satellites over a defined mission period.

Satellites Defined:
GLOBAL_2
GLOBAL_4
GLOBAL_9
GLOBAL_14
GLOBAL_12
GLOBAL_13
GLOBAL_17
GLOBAL_16
GLOBAL_18
GLOBAL_20
GLOBAL_19
GLOBAL_5
 
 # Satellite Coverage Heatmap

This project visualizes satellite coverage using position data and overlays the coverage heatmap on a world map of the oceans. The map is created using Natural Earth shapefiles.

## Features
- Generates a heatmap of satellite coverage based on position data.
- Overlays the heatmap on a world map of oceans from Natural Earth shapefiles.

## Requirements

Install the required libraries using:
```bash
pip install geopandas pandas numpy matplotlib
