import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the ocean map 
shapefile_path = 'C:\\Users\\extre\\Downloads\\ne_110m_ocean//ne_110m_ocean.shp'  
oceans = gpd.read_file(shapefile_path)

# Load the position data
file_path = 'C:\\Users\\extre\\Documents\\GitHub\\constellation_coverage\\docs\\PositionReportFile.txt'  
df = pd.read_csv(file_path, delim_whitespace=True)

# Define coverage parameters
SPATIAL_RESOLUTION = 1  # meters
ALTITUDE = 500  # km
COVERAGE_AREA = 30  # km^2
coverage_radius = np.sqrt(COVERAGE_AREA / np.pi)  # Radius in km

# Create a grid of latitude and longitude values
lat_bins = np.linspace(-90, 90, 180)  # 1-degree bins
lon_bins = np.linspace(-180, 180, 360)  # 1-degree bins
coverage_map = np.zeros((len(lat_bins), len(lon_bins)))

# Iterate over each satellite and each time step
for i, row in df.iterrows():
    for sat_prefix in ['GLOBAL_2', 'GLOBAL_4', 'GLOBAL_9', 'GLOBAL_14','GLOBAL_12', 'GLOBAL_13',
                        'GLOBAL_17', 'GLOBAL_16','GLOBAL_18', 'GLOBAL_20', 'GLOBAL_19', 'GLOBAL_5']:  
        lat, lon = row[f'{sat_prefix}.Earth.Latitude'], row[f'{sat_prefix}.Earth.Longitude']
        
        # Add coverage to the map
        for lat_center in lat_bins:
            for lon_center in lon_bins:
                distance = np.sqrt((lat_center - lat)**2 + (lon_center - lon)**2)
                if distance <= coverage_radius:
                    coverage_map[np.abs(lat_bins - lat_center).argmin(), np.abs(lon_bins - lon_center).argmin()] += 1

# Plotting the heatmap with the ocean shapefile as a background
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the ocean map
oceans.plot(ax=ax, color='lightblue', edgecolor='black', zorder=1)

# Overlay the coverage heatmap with increased transparency
extent = [-180, 180, -90, 90]
heatmap = ax.imshow(coverage_map, extent=extent, origin='lower', cmap='hot', alpha=0.7, zorder=2)

# Add a colorbar
plt.colorbar(heatmap, label="Number of Passes")

# Add title and labels
plt.title("BlackSky Constellation Coverage")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

# Show the plot
plt.show()