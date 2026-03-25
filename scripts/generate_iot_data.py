import polars as pl
from faker import Faker
import random
from datetime import datetime, timedelta
import json

fake = Faker()

# Generate devices
devices = []
device_types = ['temperature_sensor', 'humidity_sensor', 'pressure_sensor', 'motion_sensor', 'light_sensor']
locations = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']

for i in range(5000):
    device = {
        'device_id': f'DEV-{i:05d}',
        'device_type': random.choice(device_types),
        'location': random.choice(locations),
        'install_date': fake.date_between(start_date='-2y', end_date='today').isoformat()
    }
    devices.append(device)

# Save devices to JSON
with open('devices.json', 'w') as f:
    json.dump(devices, f, indent=2)

# Generate sensors
sensors = []
sensor_types = ['temperature', 'humidity', 'pressure', 'motion', 'light']
units = {'temperature': 'Celsius', 'humidity': '%', 'pressure': 'hPa', 'motion': 'boolean', 'light': 'lux'}

for i in range(5000):
    device_id = random.choice(devices)['device_id']
    sensor_type = random.choice(sensor_types)
    sensor = {
        'sensor_id': f'SEN-{i:05d}',
        'device_id': device_id,
        'sensor_type': sensor_type,
        'units': units[sensor_type]
    }
    sensors.append(sensor)

# Save sensors to JSON
with open('sensors.json', 'w') as f:
    json.dump(sensors, f, indent=2)

# Generate readings
readings = []
for i in range(5000):
    sensor = random.choice(sensors)
    sensor_id = sensor['sensor_id']
    sensor_type = sensor['sensor_type']
    if sensor_type == 'temperature':
        value = round(random.uniform(-10, 40), 2)
    elif sensor_type == 'humidity':
        value = round(random.uniform(0, 100), 2)
    elif sensor_type == 'pressure':
        value = round(random.uniform(950, 1050), 2)
    elif sensor_type == 'motion':
        value = random.choice([0, 1])
    elif sensor_type == 'light':
        value = round(random.uniform(0, 10000), 2)
    
    timestamp = fake.date_time_between(start_date='-30d', end_date='now').isoformat()
    reading = {
        'reading_id': f'READ-{i:05d}',
        'sensor_id': sensor_id,
        'timestamp': timestamp,
        'value': value
    }
    readings.append(reading)

# Save readings to JSON
with open('sensor_readings.json', 'w') as f:
    json.dump(readings, f, indent=2)

print("Data generated and saved to JSON files.")