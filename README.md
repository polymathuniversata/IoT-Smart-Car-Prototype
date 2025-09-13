# IoT Smart Car Prototype

An IoT-enabled autonomous smart car prototype built with Raspberry Pi, featuring remote control, obstacle avoidance, and real-time data transmission.

## Features

- **Remote Control**: Web-based and MQTT-based control interface
- **Autonomous Navigation**: Obstacle detection and avoidance using ultrasonic sensors
- **IoT Connectivity**: MQTT protocol for real-time data transmission and remote monitoring
- **Motor Control**: Precise DC motor control with speed regulation
- **Sensor Integration**: Ultrasonic distance sensing for obstacle detection
- **Safety Features**: Emergency stop button and collision avoidance
- **Data Logging**: Real-time telemetry and status reporting

## Hardware Requirements

- Raspberry Pi 4 (or similar)
- L298N Motor Driver Module
- 4x DC Motors with wheels
- 3x HC-SR04 Ultrasonic Sensors
- Power bank (10000mAh)
- Jumper wires and chassis
- Optional: Camera module, additional sensors

## Software Requirements

- Raspberry Pi OS
- Python 3.7+
- Required Python packages:
  - RPi.GPIO
  - paho-mqtt
  - flask (for web interface)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/IoT-Smart-Car-Prototype.git
   cd IoT-Smart-Car-Prototype
   ```

2. **Install dependencies**:
   ```bash
   pip install paho-mqtt flask
   ```

3. **Hardware setup**:
   - Follow the wiring diagram in `docs/hardware_setup.md`
   - Assemble the chassis and mount components
   - Test power connections

4. **Configuration**:
   - Update MQTT broker settings in `src/iot_client.py` if needed
   - Adjust sensor pins in configuration files

## Usage

### Basic Operation

1. **Run the main control script**:
   ```bash
   python src/car_control.py
   ```

2. **Available commands**:
   - `forward` - Move forward
   - `backward` - Move backward
   - `left` - Turn left
   - `right` - Turn right
   - `stop` - Stop movement
   - `auto` - Start autonomous mode
   - `manual` - Switch to manual mode
   - `status` - Get car status
   - `quit` - Exit program

### IoT Operation

1. **Start IoT client**:
   ```bash
   python src/iot_client.py
   ```

2. **MQTT Topics**:
   - `smartcar/control` - Send control commands
   - `smartcar/status` - Receive car status
   - `smartcar/telemetry` - Receive telemetry data

3. **Example MQTT commands**:
   ```json
   {"command": "move_forward", "params": {"speed": 50}}
   {"command": "set_mode", "params": {"mode": "autonomous"}}
   {"command": "get_status"}
   ```

### Web Interface (Optional)

A Flask-based web interface can be added for browser-based control:

```bash
python src/web_interface.py
```

Visit `http://localhost:5000` for the control interface.

## Project Structure

```
IoT-Smart-Car-Prototype/
├── docs/
│   ├── requirements.md          # Feature specifications
│   └── hardware_setup.md        # Wiring and assembly guide
├── src/
│   ├── car_control.py           # Main car control logic
│   ├── motor_control.py         # Motor driver interface
│   ├── sensor_control.py        # Ultrasonic sensor handling
│   ├── iot_client.py            # MQTT connectivity
│   └── web_interface.py         # Flask web app (optional)
├── tests/
│   └── test_motor.py            # Unit tests
├── README.md                    # This file
└── requirements.txt             # Python dependencies
```

## API Reference

### SmartCar Class

- `move_forward()` - Move car forward
- `move_backward()` - Move car backward
- `turn_left()` - Turn left
- `turn_right()` - Turn right
- `stop()` - Stop all movement
- `set_mode(mode)` - Set to 'manual' or 'autonomous'
- `set_speed(speed)` - Set speed (0-100)
- `get_status()` - Get current car status

### MotorController Class

- `move_forward(speed)` - Move forward at speed
- `move_backward(speed)` - Move backward at speed
- `turn_left(speed)` - Turn left at speed
- `turn_right(speed)` - Turn right at speed
- `stop()` - Stop motors

### SensorArray Class

- `get_front_distance()` - Get front sensor distance
- `get_left_distance()` - Get left sensor distance
- `get_right_distance()` - Get right sensor distance
- `check_obstacle(threshold)` - Check for obstacles within threshold

## Testing

Run unit tests:
```bash
python -m unittest tests/test_motor.py
```

## Safety Notes

- Always test in a safe environment
- Keep emergency stop accessible
- Monitor battery levels
- Supervise autonomous operation

## Troubleshooting

### Common Issues

1. **Motors not moving**:
   - Check L298N connections
   - Verify power supply
   - Test GPIO pins

2. **Inaccurate sensor readings**:
   - Adjust sensor positioning
   - Check voltage levels
   - Calibrate sensors

3. **MQTT connection failed**:
   - Check network connectivity
   - Verify broker settings
   - Check firewall settings

4. **Web interface not loading**:
   - Ensure Flask is installed
   - Check port availability
   - Verify IP address

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Raspberry Pi Foundation
- MQTT community
- Open source robotics community
