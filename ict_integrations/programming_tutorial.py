# ICT Integration: Programming Tutorial - Variables and Loops
# Educational example for teaching basic programming concepts in ICT

# This tutorial demonstrates fundamental programming concepts
# that can be taught alongside robotics

def variables_demo():
    """Demonstrate variables and data types"""
    print("=== Variables Demo ===")

    # Integer
    robot_speed = 50
    print(f"Robot speed: {robot_speed} units")

    # Float
    sensor_distance = 23.5
    print(f"Sensor distance: {sensor_distance} cm")

    # String
    robot_status = "Ready"
    print(f"Robot status: {robot_status}")

    # Boolean
    obstacle_detected = False
    print(f"Obstacle detected: {obstacle_detected}")

def loops_demo():
    """Demonstrate loops for repetitive tasks"""
    print("\n=== Loops Demo ===")

    # For loop - counting robot movements
    print("Robot movement sequence:")
    for step in range(1, 6):
        print(f"Step {step}: Move forward")

    # While loop - sensor monitoring
    print("\nMonitoring sensor (simulated):")
    readings = 0
    while readings < 5:
        distance = 100 + readings * 10  # Simulated decreasing distance
        print(f"Reading {readings + 1}: Distance = {distance}mm")
        readings += 1

        if distance < 120:
            print("Obstacle getting close!")
            break

def conditions_demo():
    """Demonstrate conditional statements"""
    print("\n=== Conditions Demo ===")

    battery_level = 75

    if battery_level > 80:
        print("Battery level: Excellent")
    elif battery_level > 50:
        print("Battery level: Good")
    elif battery_level > 20:
        print("Battery level: Low - Consider charging")
    else:
        print("Battery level: Critical - Stop operations")

def main():
    print("ICT Programming Tutorial")
    print("========================")

    variables_demo()
    loops_demo()
    conditions_demo()

    print("\nTutorial complete! These concepts can be applied to robotics programming.")

if __name__ == "__main__":
    main()