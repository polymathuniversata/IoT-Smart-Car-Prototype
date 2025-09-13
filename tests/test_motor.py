# Test Motor Control Module
# Unit tests for motor control functionality

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Mock RPi.GPIO for testing
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()

from motor_control import MotorController

class TestMotorController(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures"""
        with patch('RPi.GPIO.setmode'), \
             patch('RPi.GPIO.setup'), \
             patch('RPi.GPIO.PWM'), \
             patch('RPi.GPIO.output'):
            self.mc = MotorController()

    def test_initialization(self):
        """Test motor controller initialization"""
        self.assertIsNotNone(self.mc)
        self.assertEqual(self.mc.speed_a, 0)
        self.assertEqual(self.mc.speed_b, 0)

    def test_set_motor_a_forward(self):
        """Test setting motor A forward"""
        with patch('RPi.GPIO.output') as mock_output, \
             patch.object(self.mc.pwm_a, 'ChangeDutyCycle') as mock_duty:
            self.mc.set_motor_a(50)

            # Check GPIO outputs for forward direction
            mock_output.assert_any_call(17, True)   # IN1
            mock_output.assert_any_call(18, False)  # IN2
            mock_duty.assert_called_with(50)

    def test_set_motor_a_backward(self):
        """Test setting motor A backward"""
        with patch('RPi.GPIO.output') as mock_output, \
             patch.object(self.mc.pwm_a, 'ChangeDutyCycle') as mock_duty:
            self.mc.set_motor_a(-30)

            # Check GPIO outputs for backward direction
            mock_output.assert_any_call(17, False)  # IN1
            mock_output.assert_any_call(18, True)   # IN2
            mock_duty.assert_called_with(30)

    def test_set_motor_a_stop(self):
        """Test stopping motor A"""
        with patch('RPi.GPIO.output') as mock_output, \
             patch.object(self.mc.pwm_a, 'ChangeDutyCycle') as mock_duty:
            self.mc.set_motor_a(0)

            # Check GPIO outputs for stop
            mock_output.assert_any_call(17, False)  # IN1
            mock_output.assert_any_call(18, False)  # IN2
            mock_duty.assert_called_with(0)

    def test_move_forward(self):
        """Test moving forward"""
        with patch.object(self.mc, 'set_motor_a') as mock_a, \
             patch.object(self.mc, 'set_motor_b') as mock_b:
            self.mc.move_forward(60)

            mock_a.assert_called_with(60)
            mock_b.assert_called_with(60)

    def test_move_backward(self):
        """Test moving backward"""
        with patch.object(self.mc, 'set_motor_a') as mock_a, \
             patch.object(self.mc, 'set_motor_b') as mock_b:
            self.mc.move_backward(40)

            mock_a.assert_called_with(-40)
            mock_b.assert_called_with(-40)

    def test_turn_left(self):
        """Test turning left"""
        with patch.object(self.mc, 'set_motor_a') as mock_a, \
             patch.object(self.mc, 'set_motor_b') as mock_b:
            self.mc.turn_left(50)

            mock_a.assert_called_with(-50)
            mock_b.assert_called_with(50)

    def test_turn_right(self):
        """Test turning right"""
        with patch.object(self.mc, 'set_motor_a') as mock_a, \
             patch.object(self.mc, 'set_motor_b') as mock_b:
            self.mc.turn_right(50)

            mock_a.assert_called_with(50)
            mock_b.assert_called_with(-50)

    def test_stop(self):
        """Test stopping"""
        with patch.object(self.mc, 'set_motor_a') as mock_a, \
             patch.object(self.mc, 'set_motor_b') as mock_b:
            self.mc.stop()

            mock_a.assert_called_with(0)
            mock_b.assert_called_with(0)

if __name__ == '__main__':
    unittest.main()