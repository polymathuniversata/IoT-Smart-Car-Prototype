# VEX V5 Sensor Integration Example
# Demonstrates reading sensor data and basic decision making

from vex import *

# Initialize brain and sensors
brain = Brain()
sonar = Sonar(brain.three_wire_port.a)  # Ultrasonic sensor
bumper = Bumper(brain.three_wire_port.b)  # Touch sensor

def check_obstacle():
    """Check for obstacles using sonar sensor"""
    distance = sonar.distance(MM)
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Distance: ", distance, "mm")

    if distance < 200:  # If obstacle closer than 20cm
        brain.screen.set_cursor(2, 1)
        brain.screen.print("Obstacle detected!")
        return True
    return False

def bumper_pressed():
    """Check if bumper is pressed"""
    return bumper.pressing()

# Main program loop
brain.screen.print("Sensor Demo Starting...")
wait(2, SECONDS)

while True:
    if check_obstacle() or bumper_pressed():
        # Stop and alert
        brain.screen.set_cursor(3, 1)
        brain.screen.print("STOP!")
        wait(1, SECONDS)
    else:
        brain.screen.set_cursor(3, 1)
        brain.screen.print("Path clear")

    wait(0.5, SECONDS)