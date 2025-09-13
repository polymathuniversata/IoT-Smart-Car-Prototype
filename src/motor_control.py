# IoT Smart Car - Motor Control Module
# Handles DC motor control using L298N driver

import RPi.GPIO as GPIO
import time

class MotorController:
    def __init__(self):
        # GPIO pins for L298N
        self.IN1 = 17  # Motor A forward
        self.IN2 = 18  # Motor A backward
        self.IN3 = 27  # Motor B forward
        self.IN4 = 22  # Motor B backward
        self.ENA = 23  # Motor A speed (PWM)
        self.ENB = 24  # Motor B speed (PWM)

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self.IN1, self.IN2, self.IN3, self.IN4], GPIO.OUT)
        GPIO.setup([self.ENA, self.ENB], GPIO.OUT)

        # Setup PWM
        self.pwm_a = GPIO.PWM(self.ENA, 1000)  # 1kHz frequency
        self.pwm_b = GPIO.PWM(self.ENB, 1000)
        self.pwm_a.start(0)
        self.pwm_b.start(0)

        # Motor states
        self.speed_a = 0
        self.speed_b = 0

    def set_motor_a(self, speed):
        """Set Motor A speed and direction
        speed: -100 to 100 (negative = backward)
        """
        if speed > 0:
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
        elif speed < 0:
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
        else:
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.LOW)

        self.speed_a = abs(speed)
        self.pwm_a.ChangeDutyCycle(self.speed_a)

    def set_motor_b(self, speed):
        """Set Motor B speed and direction
        speed: -100 to 100 (negative = backward)
        """
        if speed > 0:
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
        elif speed < 0:
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
        else:
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.LOW)

        self.speed_b = abs(speed)
        self.pwm_b.ChangeDutyCycle(self.speed_b)

    def move_forward(self, speed=50):
        """Move car forward"""
        self.set_motor_a(speed)
        self.set_motor_b(speed)

    def move_backward(self, speed=50):
        """Move car backward"""
        self.set_motor_a(-speed)
        self.set_motor_b(-speed)

    def turn_left(self, speed=50):
        """Turn left (Motor A backward, Motor B forward)"""
        self.set_motor_a(-speed)
        self.set_motor_b(speed)

    def turn_right(self, speed=50):
        """Turn right (Motor A forward, Motor B backward)"""
        self.set_motor_a(speed)
        self.set_motor_b(-speed)

    def stop(self):
        """Stop all motors"""
        self.set_motor_a(0)
        self.set_motor_b(0)

    def cleanup(self):
        """Clean up GPIO"""
        self.stop()
        self.pwm_a.stop()
        self.pwm_b.stop()
        GPIO.cleanup()

# Test function
if __name__ == "__main__":
    try:
        mc = MotorController()
        print("Testing motor control...")

        # Test sequence
        print("Forward")
        mc.move_forward(30)
        time.sleep(2)

        print("Stop")
        mc.stop()
        time.sleep(1)

        print("Backward")
        mc.move_backward(30)
        time.sleep(2)

        print("Stop")
        mc.stop()
        time.sleep(1)

        print("Left turn")
        mc.turn_left(40)
        time.sleep(1.5)

        print("Right turn")
        mc.turn_right(40)
        time.sleep(1.5)

        print("Stop")
        mc.stop()

    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        mc.cleanup()