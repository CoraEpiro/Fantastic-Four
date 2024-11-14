import pandas as pd
import folium
import googlemaps
import polyline
from folium.plugins import HeatMap
from shiny import App, ui, render, run_app

# Load data from Excel files
bus_stops_df = pd.read_excel('data/FLEXI_bus_stops.xls')
trip_data_df = pd.read_excel('data/FLEXI_trip_data.xls')

# Merge and process data
df = trip_data_df.merge(bus_stops_df, how='left', left_on='Pickup ID', right_on='index', suffixes=('_pickup', '_dropoff'))
df.rename(columns={'latitude': 'Pickup Latitude', 'longitude': 'Pickup Longitude'}, inplace=True)
df = df.merge(bus_stops_df, how='left', left_on='Dropoff ID', right_on='index', suffixes=('', '_dropoff'))
df.rename(columns={'latitude': 'Dropoff Latitude', 'longitude': 'Dropoff Longitude'}, inplace=True)
df.drop(columns=['index', 'index_dropoff'], inplace=True)
df.dropna(inplace=True)

# Ensure date columns are in datetime format
df['Actual Pickup Time'] = pd.to_datetime(df['Actual Pickup Time'])

center_lat, center_lon = 48.99763353708334, 11.47434937975292

df['Actual Dropoff Time'] = pd.to_datetime(df['Actual Dropoff Time'])

# Create 'Is Canceled' column based on 'Status'
df['Is Canceled'] = df['Status'].str.contains('Cancelled')

# Calculate additional features
df['Hour'] = df['Actual Pickup Time'].dt.hour
df['Route'] = df['Pickup ID'].astype(str) + '-' + df['Dropoff ID'].astype(str)
df['Trip Duration'] = (df['Actual Dropoff Time'] - df['Actual Pickup Time']).dt.total_seconds() / 60

# Calculate popular routes
most_popular_routes_by_hour = df.groupby('Hour')['Route'].agg(lambda x: x.value_counts().idxmax())

# Initialize Google Maps client with your API key
gmaps = googlemaps.Client(key='AIzaSyCql1sz_qlUWL_9q1BEfuxBP3yHKN2wI1c')

# Define function to create map
def create_map(hour, view_type="Popular Routes"):
    if view_type == "Popular Routes":
        route = most_popular_routes_by_hour[hour]
        pickup_id, dropoff_id = map(int, route.split('-'))
        pickup_location = df[df['Pickup ID'] == pickup_id][['Pickup Latitude', 'Pickup Longitude']].iloc[0]
        dropoff_location = df[df['Dropoff ID'] == dropoff_id][['Dropoff Latitude', 'Dropoff Longitude']].iloc[0]
        
        directions_result = gmaps.directions(
            (pickup_location['Pickup Latitude'], pickup_location['Pickup Longitude']),
            (dropoff_location['Dropoff Latitude'], dropoff_location['Dropoff Longitude']),
            mode="driving"
        )
        route_polyline = directions_result[0]['overview_polyline']['points']
        route_coords = polyline.decode(route_polyline)
        
        m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

        station_name_pickup = df[df['Pickup ID'] == pickup_id]['name'].iloc[0]
        station_name_dropoff = df[df['Dropoff ID'] == dropoff_id]['name_dropoff'].iloc[0]
              
        # Add pickup and dropoff markers with specific colors
        folium.Marker(
            [pickup_location['Pickup Latitude'], pickup_location['Pickup Longitude']],
            popup=(f'Station Name: {station_name_pickup}<br><br>'
                         f'Pickup ID: {pickup_id}<br><br>'
                         f'3 rides this hour'),
            icon=folium.Icon(color='green')
        ).add_to(m)
        
        folium.Marker(
            [dropoff_location['Dropoff Latitude'], dropoff_location['Dropoff Longitude']],
            popup=(f'Station Name: {station_name_dropoff}<br><br>'
                         f'Dropoff ID: {dropoff_id}<br><br>'
                         f'4 rides this hour'),
            icon=folium.Icon(color='blue')
        ).add_to(m)
        
        # Add polyline for route with specific color
        folium.PolyLine(route_coords, color='#ad579d', weight=5).add_to(m)
        
    elif view_type == "Cancellation Rates":
        stations = df[df['Hour'] == hour].groupby('Pickup ID').agg(
            cancellation_percentage=('Is Canceled', 'mean')).reset_index()
        
        if not stations.empty:
            first_station = stations.iloc[0]
            pickup_location = df[df['Pickup ID'] == first_station['Pickup ID']][['Pickup Latitude', 'Pickup Longitude']].iloc[0]
            m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
            
            # Add markers for cancellation rates
            for _, station in stations.iterrows():
                pickup_id = station['Pickup ID']
                hourly_cancellation_rate = station['cancellation_percentage'] * 100
                pickup_location = df[df['Pickup ID'] == pickup_id][['Pickup Latitude', 'Pickup Longitude']].iloc[0]
                
                folium.Marker(
                    [pickup_location['Pickup Latitude'], pickup_location['Pickup Longitude']],
                    popup=(f'Pickup ID: {pickup_id}<br>'
                           f'Hourly Cancellation Rate: {hourly_cancellation_rate:.2f}%'),
                    icon=folium.Icon(color='red')
                ).add_to(m)

    # Add heatmap for the selected hour
    heatmap_data = df[df['Hour'] == hour][['Pickup Latitude', 'Pickup Longitude']].values.tolist()
    HeatMap(heatmap_data).add_to(m)
    return m._repr_html_()

app_ui = ui.page_fluid(
    ui.tags.style("""
        #map { height: 100vh; width: 100vw; position: absolute; top: 0; left: 0; overflow: hidden; }
        .popup-container {
            position: absolute; top: 20px; left: 20px;
            background-color: rgba(255, 255, 255, 0.9); padding: 15px; border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); max-width: 300px; z-index: 1000;
        }
    """),
    ui.div(ui.output_ui("map"), id="map"),
    ui.div(
        ui.div(
            ui.tags.h3("Map Options"),
            ui.input_slider("hour", "Hour:", min=5, max=22, value=5, step=1),
            ui.input_select("view_type", "Select View:", ["Popular Routes", "Cancellation Rates"]),
            ui.output_text("distance_duration"),
            class_="popup-container"
        )
    )
)


def server(input, output, session):
    @output
    @render.text
    def distance_duration():
        view_type = input.view_type()
        
        if view_type == "Popular Routes":
            hour = input.hour()
            route = most_popular_routes_by_hour[hour]
            # Unpack the pickup and dropoff IDs properly
            pickup_id, dropoff_id = [int(x) for x in route.split('-')]  # Convert to integers here

            pickup_location = df[df['Pickup ID'] == pickup_id][['Pickup Latitude', 'Pickup Longitude']].iloc[0]
            dropoff_location = df[df['Dropoff ID'] == dropoff_id][['Dropoff Latitude', 'Dropoff Longitude']].iloc[0]

            directions_result = gmaps.directions(
                (pickup_location['Pickup Latitude'], pickup_location['Pickup Longitude']),
                (dropoff_location['Dropoff Latitude'], dropoff_location['Dropoff Longitude']),
                mode="driving"
            )
            distance = directions_result[0]['legs'][0]['distance']['text']
            duration = directions_result[0]['legs'][0]['duration']['text']

            return f"Distance: {distance}, Duration: {duration}"
        else:
            return ""

    @output
    @render.ui
    def map():
        hour = input.hour()
        view_type = input.view_type()
        map_html = create_map(hour, view_type)
        return ui.HTML(map_html)

app = App(app_ui, server)

if __name__ == "__main__":
    run_app(app)