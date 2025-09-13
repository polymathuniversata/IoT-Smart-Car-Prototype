# VEX V5 Motor Control Example
# This example demonstrates basic motor control for a simple robot drive system

from vex import *

# Initialize brain and motors
brain = Brain()
motor_left = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
motor_right = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)

def drive_forward(speed=50, duration=2):
    """Drive the robot forward at specified speed for given duration"""
    motor_left.spin(FORWARD, speed, PERCENT)
    motor_right.spin(FORWARD, speed, PERCENT)
    wait(duration, SECONDS)
    motor_left.stop()
    motor_right.stop()

def turn_left(speed=30, duration=1):
    """Turn the robot left"""
    motor_left.spin(REVERSE, speed, PERCENT)
    motor_right.spin(FORWARD, speed, PERCENT)
    wait(duration, SECONDS)
    motor_left.stop()
    motor_right.stop()

# Main program
brain.screen.print("Motor Control Demo")
drive_forward()
wait(1, SECONDS)
turn_left()
brain.screen.print("Demo Complete")