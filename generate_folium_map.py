"""
Generate Interactive Folium Map for SpaceX Launch Sites
Saves the map as an HTML file that can be embedded in the webapp
"""

import folium
import pandas as pd
from folium.plugins import MarkerCluster, MousePosition
from folium.features import DivIcon
from math import sin, cos, sqrt, atan2, radians
import os

# Create output directory
output_dir = 'webapp'
os.makedirs(output_dir, exist_ok=True)

# Load the dataset (use local file if available)
try:
    spacex_df = pd.read_csv('Datasets/spacex_launch_geo.csv')
    print(f"Loaded local dataset with {len(spacex_df)} records")
except:
    spacex_df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv')
    print("Loaded dataset from URL")

# Select relevant columns
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]

# Get unique launch sites
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]

print("\nLaunch Sites:")
print(launch_sites_df)

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula"""
    R = 6373.0  # Earth radius in km

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

# Custom dark tile layer for space theme
dark_tiles = 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png'
attr = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>'

# Create the main map centered on Florida
florida_center = [28.5, -80.6]
site_map = folium.Map(
    location=florida_center,
    zoom_start=6,
    tiles=dark_tiles,
    attr=attr
)

# Add alternate tile layers
folium.TileLayer(
    tiles='cartodbdark_matter',
    attr='CartoDB',
    name='Dark Matter'
).add_to(site_map)

folium.TileLayer(
    tiles='openstreetmap',
    name='OpenStreetMap'
).add_to(site_map)

# Add marker cluster
marker_cluster = MarkerCluster(name='Launch Markers')
site_map.add_child(marker_cluster)

# Color coding for success/failure
spacex_df['marker_color'] = spacex_df['class'].map({0: 'red', 1: 'green'})

# Add launch site circles and labels
site_colors = {
    'KSC LC-39A': '#00D4AA',    # Success - teal
    'CCAFS SLC-40': '#0066FF',  # Primary - blue
    'CCAFS LC-40': '#A855F7',   # Secondary - purple
    'VAFB SLC-4E': '#FF6B35'    # Accent - orange
}

for _, row in launch_sites_df.iterrows():
    site = row['Launch Site']
    lat, lon = row['Lat'], row['Long']
    color = site_colors.get(site, '#0066FF')

    # Calculate success rate for this site
    site_data = spacex_df[spacex_df['Launch Site'] == site]
    success_rate = site_data['class'].mean() * 100
    total_launches = len(site_data)
    successful = site_data['class'].sum()

    # Add circle
    folium.Circle(
        [lat, lon],
        radius=3000,
        color=color,
        fill=True,
        fillColor=color,
        fillOpacity=0.3,
        popup=folium.Popup(
            f"""<div style="width: 200px;">
                <h4 style="margin: 0; color: {color};">{site}</h4>
                <hr style="margin: 5px 0;">
                <b>Success Rate:</b> {success_rate:.1f}%<br>
                <b>Total Launches:</b> {total_launches}<br>
                <b>Successful:</b> {successful}<br>
                <b>Failed:</b> {total_launches - successful}<br>
                <b>Coordinates:</b> {lat:.4f}, {lon:.4f}
            </div>""",
            max_width=250
        )
    ).add_to(site_map)

    # Add label
    folium.map.Marker(
        [lat, lon],
        icon=DivIcon(
            icon_size=(150, 36),
            icon_anchor=(0, 0),
            html=f'<div style="font-size: 11px; color: {color}; font-weight: bold; text-shadow: 1px 1px 2px black;">{site}</div>'
        )
    ).add_to(site_map)

# Add individual launch markers to cluster
for _, row in spacex_df.iterrows():
    lat, lon = row['Lat'], row['Long']
    color = row['marker_color']
    site = row['Launch Site']
    outcome = 'Success' if row['class'] == 1 else 'Failure'

    folium.Marker(
        [lat, lon],
        icon=folium.Icon(
            color='white',
            icon_color=color,
            icon='rocket' if color == 'green' else 'times',
            prefix='fa'
        ),
        popup=f"{site}<br>Outcome: {outcome}"
    ).add_to(marker_cluster)

# Add KSC LC-39A proximity measurements
ksc_coord = [28.573255, -80.646895]
coastline_coord = [28.56871, -80.60739]
city_coord = [28.61261, -80.80797]  # Titusville
railway_coord = [28.55752, -80.80155]
highway_coord = [28.54134, -80.85154]

# Calculate distances
distances = {
    'Coastline': (coastline_coord, calculate_distance(ksc_coord[0], ksc_coord[1], coastline_coord[0], coastline_coord[1]), '#00D4AA'),
    'Railway': (railway_coord, calculate_distance(ksc_coord[0], ksc_coord[1], railway_coord[0], railway_coord[1]), '#FF6B35'),
    'Highway': (highway_coord, calculate_distance(ksc_coord[0], ksc_coord[1], highway_coord[0], highway_coord[1]), '#0066FF'),
    'Titusville': (city_coord, calculate_distance(ksc_coord[0], ksc_coord[1], city_coord[0], city_coord[1]), '#EF4444')
}

# Add distance markers and lines
for name, (coord, dist, color) in distances.items():
    # Add marker
    folium.map.Marker(
        coord,
        icon=DivIcon(
            icon_size=(100, 20),
            icon_anchor=(0, 0),
            html=f'<div style="font-size: 10px; color: {color}; font-weight: bold; text-shadow: 1px 1px 2px black;">{name}: {dist:.2f} km</div>'
        )
    ).add_to(site_map)

    # Add line
    folium.PolyLine(
        [ksc_coord, coord],
        color=color,
        weight=2,
        opacity=0.7,
        popup=f'{name}: {dist:.2f} km from KSC LC-39A'
    ).add_to(site_map)

# Add mouse position
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
MousePosition(
    position='topright',
    separator=' | Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat: ',
    lat_formatter=formatter,
    lng_formatter=formatter
).add_to(site_map)

# Add layer control
folium.LayerControl().add_to(site_map)

# Add a legend
legend_html = '''
<div style="position: fixed;
            bottom: 50px; left: 50px; width: 180px; height: auto;
            background-color: rgba(10, 10, 20, 0.9);
            border: 2px solid #0066FF;
            border-radius: 10px;
            padding: 15px;
            z-index: 9999;
            font-family: Arial, sans-serif;
            color: white;
            font-size: 12px;">
    <h4 style="margin: 0 0 10px 0; color: #00D4AA;">SpaceX Launch Sites</h4>
    <div style="display: flex; align-items: center; margin: 5px 0;">
        <span style="display: inline-block; width: 12px; height: 12px; background: #10B981; border-radius: 50%; margin-right: 8px;"></span>
        Successful Landing
    </div>
    <div style="display: flex; align-items: center; margin: 5px 0;">
        <span style="display: inline-block; width: 12px; height: 12px; background: #EF4444; border-radius: 50%; margin-right: 8px;"></span>
        Failed Landing
    </div>
    <hr style="border-color: #333; margin: 10px 0;">
    <div style="font-size: 10px; color: #888;">
        Click clusters to expand.<br>
        Click circles for details.
    </div>
</div>
'''
site_map.get_root().html.add_child(folium.Element(legend_html))

# Add title overlay
title_html = '''
<div style="position: fixed;
            top: 10px; left: 50%; transform: translateX(-50%);
            background-color: rgba(10, 10, 20, 0.85);
            border: 1px solid #0066FF;
            border-radius: 8px;
            padding: 10px 20px;
            z-index: 9999;
            font-family: Arial, sans-serif;
            color: white;
            text-align: center;">
    <h3 style="margin: 0; color: #00D4AA;">SpaceX Falcon 9 Launch Sites</h3>
    <p style="margin: 5px 0 0 0; font-size: 11px; color: #888;">Interactive Geospatial Analysis</p>
</div>
'''
site_map.get_root().html.add_child(folium.Element(title_html))

# Save the map
output_path = f'{output_dir}/folium_map.html'
site_map.save(output_path)
print(f"\nMap saved to: {output_path}")

# Print summary
print("\n=== Launch Site Summary ===")
for site in launch_sites_df['Launch Site']:
    site_data = spacex_df[spacex_df['Launch Site'] == site]
    print(f"{site}: {site_data['class'].sum()}/{len(site_data)} successful ({site_data['class'].mean()*100:.1f}%)")

print("\n=== Distance from KSC LC-39A ===")
for name, (coord, dist, color) in distances.items():
    print(f"  {name}: {dist:.2f} km")

print("\nFolium map generated successfully!")
