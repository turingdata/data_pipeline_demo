#%%
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

#%%
#Constants
total_distance_miles = 2000
speeds_mph = [100, 150, 200]
record_interval_min = 5
fuel_consumptions_mpg = [100, 150, 300]
num_vehicles = 5
fuel_capacities = [10, 30, 50]
start_time = datetime.now()
start_lat = 39.8283
start_lon = -98.5795

#%%
#initialize the dataframe
columns = ['vehicle_id', 'trip_id', 'measurement_sequence', 'measurement_time', 'latitude', 'longitude', 'fuel_capacity', 'distance_traveled', 'fuel_remaining_percent', 'fuel_remaining_gallon']
df = pd.DataFrame(columns=columns)

#%%
#Simulate the data
for vehicle_id in range(1, num_vehicles+1):

    fuel_capacity = np.random.choice(fuel_capacities)
    fuel_consumption_mpg = np.random.choice(fuel_consumptions_mpg)
    speed_mph = np.random.choice(speeds_mph)
    total_fuel = fuel_capacity #start with a full tank
    distance_traveled = 0
    measurement_sequence = 0
    measurement_time = start_time
    bearing = np.random.uniform(0,360) #random bearing in degrees
    lat, lon = start_lat, start_lon

    while distance_traveled < total_distance_miles and total_fuel > 0:

        measurement_sequence += 1
        measurement_time = measurement_time + timedelta(minutes = record_interval_min)

        #calculate new distance and measurement
        distance_increment = (speed_mph / 60) * record_interval_min
        distance_traveled += distance_increment
        fuel_used = distance_increment / fuel_consumption_mpg
        total_fuel -= fuel_used

        #Calculate new position
        delta_lat = (distance_increment / 69) * np.cos(np.radians(bearing)) #miles per degree latitude
        delta_lon = (distance_increment / (69.172 * np.cos(np.radians(lat)))) * np.sin(np.radians(bearing)) #miles per degree longitude

        lat += delta_lat
        lon += delta_lon

        #Check for the end conditions
        if distance_traveled > total_distance_miles :
            distance_traveled = total_distance_miles

        if total_fuel < 0:
            total_fuel = 0

        percentage_of_fuel_remaining = (total_fuel /fuel_capacity) * 100

        #Append the data to the df
        df = pd.concat([df, pd.DataFrame({
                            'vehicle_id':[vehicle_id],
                            'trip_id':[1],
                            'measurement_sequence':[measurement_sequence],
                            'measurement_time':[measurement_time.strftime("%Y-%m-%d %H:%M:%S")], 
                            'latitude': lat,
                            'longitude': lon,
                            'fuel_capacity': [fuel_capacity], 
                            'distance_traveled':[int(distance_traveled)], 
                            'fuel_remaining_percent': [int(percentage_of_fuel_remaining)], 
                            'fuel_remaining_gallon':[round(total_fuel,1)]
                            })
                        ]
        )

# Function to assign color based on fuel remaining
def assign_color(fuel_remaining):
    if fuel_remaining >= 75:
        return 'green'
    elif 50 <= fuel_remaining < 75:
        return 'yellow'
    elif 25 <= fuel_remaining < 50:
        return 'orange'
    else:
        return 'red'

df['color'] = df['fuel_remaining_percent'].apply(assign_color)
#%%
df
#%%
df.to_csv('trips.csv', index=False)

# %%
