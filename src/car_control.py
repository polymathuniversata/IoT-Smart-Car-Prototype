# IoT Smart Car - Main Control Module
# Integrates motor control, sensors, and provides high-level car functions

import time
import threading
from motor_control import MotorController
from sensor_control import SensorArray
import RPi.GPIO as GPIO

class SmartCar:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        # Initialize components
        self.motors = MotorController()
        self.sensors = SensorArray()

        # Car state
        self.mode = "manual"  # manual or autonomous
        self.speed = 50
        self.running = False

        # Status LEDs (optional)
        self.status_led = 4   # Red LED
        self.ready_led = 25   # Green LED
        GPIO.setup([self.status_led, self.ready_led], GPIO.OUT)

        # Emergency stop button
        self.emergency_pin = 16
        GPIO.setup(self.emergency_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.emergency_pin, GPIO.FALLING,
                            callback=self.emergency_stop, bouncetime=300)

        # Status
        self.status = "initialized"

    def set_mode(self, mode):
        """Set car mode: manual or autonomous"""
        if mode in ["manual", "autonomous"]:
            self.mode = mode
            print(f"Mode set to: {mode}")
        else:
            print("Invalid mode. Use 'manual' or 'autonomous'")

    def set_speed(self, speed):
        """Set car speed (0-100)"""
        self.speed = max(0, min(100, speed))
        print(f"Speed set to: {self.speed}%")

    def move_forward(self):
        """Move forward"""
        if self.check_safety():
            self.motors.move_forward(self.speed)
            self.status = "moving_forward"

    def move_backward(self):
        """Move backward"""
        if self.check_safety():
            self.motors.move_backward(self.speed)
            self.status = "moving_backward"

    def turn_left(self):
        """Turn left"""
        if self.check_safety():
            self.motors.turn_left(self.speed)
            self.status = "turning_left"

    def turn_right(self):
        """Turn right"""
        if self.check_safety():
            self.motors.turn_right(self.speed)
            self.status = "turning_right"

    def stop(self):
        """Stop the car"""
        self.motors.stop()
        self.status = "stopped"

    def check_safety(self):
        """Check if it's safe to move"""
        if self.mode == "autonomous":
            obstacles = self.sensors.check_obstacle(threshold=20)
            if obstacles:
                print(f"Safety check failed: Obstacles detected: {obstacles}")
                self.stop()
                return False
        return True

    def emergency_stop(self, channel):
        """Emergency stop callback"""
        print("EMERGENCY STOP ACTIVATED!")
        self.stop()
        self.status = "emergency_stop"
        GPIO.output(self.status_led, GPIO.HIGH)  # Turn on red LED

    def autonomous_drive(self):
        """Simple autonomous driving logic"""
        while self.running and self.mode == "autonomous":
            obstacles = self.sensors.check_obstacle(threshold=25)

            if not obstacles:
                # Path is clear, move forward
                self.move_forward()
            elif 'front' in obstacles:
                # Obstacle in front, check sides
                if 'left' not in obstacles and 'right' in obstacles:
                    # Turn left
                    self.turn_left()
                    time.sleep(0.5)
                elif 'right' not in obstacles and 'left' in obstacles:
                    # Turn right
                    self.turn_right()
                    time.sleep(0.5)
                elif 'left' not in obstacles and 'right' not in obstacles:
                    # Both sides clear, turn left (arbitrary choice)
                    self.turn_left()
                    time.sleep(0.5)
                else:
                    # All directions blocked, stop
                    self.stop()
                    print("All directions blocked!")
                    break
            else:
                # No front obstacle, continue forward
                self.move_forward()

            time.sleep(0.1)  # Small delay for sensor reading

    def start_autonomous(self):
        """Start autonomous mode"""
        if self.mode == "autonomous":
            self.running = True
            GPIO.output(self.ready_led, GPIO.HIGH)  # Turn on green LED
            self.autonomous_thread = threading.Thread(target=self.autonomous_drive)
            self.autonomous_thread.start()
            print("Autonomous mode started")

    def stop_autonomous(self):
        """Stop autonomous mode"""
        self.running = False
        GPIO.output(self.ready_led, GPIO.LOW)
        self.stop()
        print("Autonomous mode stopped")

    def get_status(self):
        """Get car status"""
        distances = self.sensors.get_all_distances()
        return {
            'status': self.status,
            'mode': self.mode,
            'speed': self.speed,
            'distances': distances,
            'obstacles': self.sensors.check_obstacle()
        }

    def cleanup(self):
        """Clean up resources"""
        self.stop()
        self.running = False
        GPIO.output([self.status_led, self.ready_led], GPIO.LOW)
        self.motors.cleanup()
        GPIO.cleanup()

# Test function
if __name__ == "__main__":
    try:
        car = SmartCar()
        print("Smart Car initialized. Commands: forward, backward, left, right, stop, auto, manual, status, quit")

        while True:
            cmd = input("Command: ").strip().lower()

            if cmd == "forward":
                car.move_forward()
            elif cmd == "backward":
                car.move_backward()
            elif cmd == "left":
                car.turn_left()
            elif cmd == "right":
                car.turn_right()
            elif cmd == "stop":
                car.stop()
            elif cmd == "auto":
                car.set_mode("autonomous")
                car.start_autonomous()
            elif cmd == "manual":
                car.set_mode("manual")
                car.stop_autonomous()
            elif cmd == "status":
                print(car.get_status())
            elif cmd == "quit":
                break
            else:
                print("Unknown command")

    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        car.cleanup()