# IoT Smart Car - Sensor Control Module
# Handles ultrasonic sensor readings for obstacle detection

import RPi.GPIO as GPIO
import time

class UltrasonicSensor:
    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin

        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

        # Initialize trigger pin to low
        GPIO.output(self.trig_pin, GPIO.LOW)

    def get_distance(self):
        """Get distance in centimeters"""
        # Send trigger pulse
        GPIO.output(self.trig_pin, GPIO.HIGH)
        time.sleep(0.00001)  # 10 microsecond pulse
        GPIO.output(self.trig_pin, GPIO.LOW)

        # Wait for echo start
        while GPIO.input(self.echo_pin) == 0:
            pulse_start = time.time()

        # Wait for echo end
        while GPIO.input(self.echo_pin) == 1:
            pulse_end = time.time()

        # Calculate distance
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150  # Speed of sound = 343 m/s = 34300 cm/s
        distance = round(distance, 2)

        return distance

class SensorArray:
    def __init__(self):
        # GPIO pins for ultrasonic sensors
        self.front_sensor = UltrasonicSensor(5, 6)   # Front
        self.left_sensor = UltrasonicSensor(19, 26)  # Left
        self.right_sensor = UltrasonicSensor(20, 21) # Right

    def get_front_distance(self):
        """Get front sensor distance"""
        return self.front_sensor.get_distance()

    def get_left_distance(self):
        """Get left sensor distance"""
        return self.left_sensor.get_distance()

    def get_right_distance(self):
        """Get right sensor distance"""
        return self.right_sensor.get_distance()

    def get_all_distances(self):
        """Get all sensor distances"""
        return {
            'front': self.get_front_distance(),
            'left': self.get_left_distance(),
            'right': self.get_right_distance()
        }

    def check_obstacle(self, threshold=30):
        """Check if any obstacle is within threshold distance"""
        distances = self.get_all_distances()
        obstacles = {}

        for direction, distance in distances.items():
            if distance < threshold and distance > 0:  # 0 means no echo received
                obstacles[direction] = distance

        return obstacles

    def get_clear_directions(self, threshold=30):
        """Get directions that are clear of obstacles"""
        obstacles = self.check_obstacle(threshold)
        all_directions = ['front', 'left', 'right']
        clear_directions = [d for d in all_directions if d not in obstacles]
        return clear_directions

# Test function
if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BCM)
        sensors = SensorArray()

        print("Testing ultrasonic sensors...")
        print("Press Ctrl+C to stop")

        while True:
            distances = sensors.get_all_distances()
            obstacles = sensors.check_obstacle()
            clear = sensors.get_clear_directions()

            print(f"Distances: {distances}")
            print(f"Obstacles: {obstacles}")
            print(f"Clear directions: {clear}")
            print("-" * 40)

            time.sleep(1)

    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        GPIO.cleanup()