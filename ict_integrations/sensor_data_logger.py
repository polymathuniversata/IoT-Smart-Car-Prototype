# ICT Integration: Sensor Data Logging Demo
# This example demonstrates data collection and logging for educational purposes
# Can be adapted for VEX robotics sensor data

import csv
import time
import random  # For simulation

def simulate_sensor_reading():
    """Simulate a sensor reading (e.g., distance in mm)"""
    return random.randint(50, 500)

def log_data(filename, data):
    """Log data to CSV file"""
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def main():
    filename = 'sensor_data.csv'

    # Create CSV header if file doesn't exist
    try:
        with open(filename, 'r') as file:
            pass
    except FileNotFoundError:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'Sensor_Value', 'Unit'])

    print("Starting sensor data logging demo...")
    print("Press Ctrl+C to stop")

    try:
        while True:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            value = simulate_sensor_reading()
            unit = 'mm'

            # Log to console
            print(f"{timestamp}: Sensor reading = {value} {unit}")

            # Log to CSV
            log_data(filename, [timestamp, value, unit])

            time.sleep(1)  # Log every second

    except KeyboardInterrupt:
        print("\nData logging stopped.")
        print(f"Data saved to {filename}")

if __name__ == "__main__":
    main()