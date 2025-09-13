# IoT Smart Car - Hardware Setup

## Overview
This document provides the hardware architecture and wiring instructions for the IoT Smart Car prototype.

## Hardware Architecture

```
[Raspberry Pi 4]
    ├── GPIO Pins
    │   ├── Motor Control (L298N)
    │   ├── Ultrasonic Sensors
    │   ├── Status LEDs
    │   └── Emergency Stop
    ├── USB Ports
    │   ├── Camera (optional)
    │   └── Additional peripherals
    ├── WiFi/Bluetooth
    │   └── IoT Connectivity
    └── Power Supply
        └── Battery Pack
```

## Component List

### Core Components
- Raspberry Pi 4 Model B
- L298N Motor Driver Module
- DC Motors (4x with wheels)
- HC-SR04 Ultrasonic Sensors (3x)
- Power Bank (10000mAh, 5V/2A output)
- Jumper wires and breadboard
- Chassis kit

### Pin Connections

#### Raspberry Pi GPIO Pinout Reference
```
3V3  (1) (2)  5V
GPIO2  (3) (4)  5V
GPIO3  (5) (6)  GND
GPIO4  (7) (8)  GPIO14
GND  (9) (10) GPIO15
GPIO17 (11) (12) GPIO18
GPIO27 (13) (14) GND
GPIO22 (15) (16) GPIO23
3V3 (17) (18) GPIO24
GPIO10 (19) (20) GND
GPIO9 (21) (22) GPIO25
GPIO11 (23) (24) GPIO8
GND (25) (26) GPIO7
GPIO0 (27) (28) GPIO1
GPIO5 (29) (30) GND
GPIO6 (31) (32) GPIO12
GPIO13 (33) (34) GND
GPIO19 (35) (36) GPIO16
GPIO26 (37) (38) GPIO20
GND (39) (40) GPIO21
```

#### Motor Driver (L298N) Connections
```
L298N Module          Raspberry Pi GPIO
IN1 (Motor A)         GPIO 17 (Pin 11)
IN2 (Motor A)         GPIO 18 (Pin 12)
IN3 (Motor B)         GPIO 27 (Pin 13)
IN4 (Motor B)         GPIO 22 (Pin 15)
ENA (Speed A)         GPIO 23 (Pin 16)
ENB (Speed B)         GPIO 24 (Pin 18)
GND                   GND (Pin 6)
VCC                   5V (Pin 2)
VM (Motor Power)      Battery + (5-12V)
```

#### Ultrasonic Sensors (HC-SR04)
```
Sensor 1 (Front)      Raspberry Pi GPIO
VCC                   5V (Pin 2)
Trig                  GPIO 5 (Pin 29)
Echo                  GPIO 6 (Pin 31)
GND                   GND (Pin 30)

Sensor 2 (Left)       Raspberry Pi GPIO
VCC                   5V (Pin 2)
Trig                  GPIO 19 (Pin 35)
Echo                  GPIO 26 (Pin 37)
GND                   GND (Pin 34)

Sensor 3 (Right)      Raspberry Pi GPIO
VCC                   5V (Pin 2)
Trig                  GPIO 20 (Pin 38)
Echo                  GPIO 21 (Pin 40)
GND                   GND (Pin 39)
```

#### Status LEDs
```
Red LED (Status)      Raspberry Pi GPIO
Anode (+)             GPIO 4 (Pin 7) via 220Ω resistor
Cathode (-)           GND (Pin 25)

Green LED (Ready)     Raspberry Pi GPIO
Anode (+)             GPIO 25 (Pin 22) via 220Ω resistor
Cathode (-)           GND (Pin 20)
```

#### Emergency Stop Button
```
Push Button           Raspberry Pi GPIO
One pin               GPIO 16 (Pin 36)
Other pin             GND (Pin 14)
```

## Assembly Instructions

### Step 1: Prepare the Chassis
1. Mount the DC motors to the chassis
2. Attach wheels to motors
3. Secure the battery pack
4. Mount Raspberry Pi on top plate

### Step 2: Wire the Motor Driver
1. Connect motor driver to Raspberry Pi GPIO pins as specified
2. Wire motors to motor driver output terminals
3. Connect battery to motor driver power input
4. Connect motor driver VCC to Raspberry Pi 5V

### Step 3: Install Ultrasonic Sensors
1. Mount sensors on front, left, and right of chassis
2. Wire each sensor to Raspberry Pi GPIO pins
3. Ensure sensors are angled appropriately for detection

### Step 4: Add Status Indicators
1. Mount LEDs on chassis
2. Wire LEDs with appropriate resistors
3. Connect emergency stop button

### Step 5: Power Connections
1. Connect Raspberry Pi to power bank
2. Ensure all grounds are connected
3. Test power distribution

## Safety Considerations
- Use appropriate wire gauges for motor currents
- Include fuses in power lines
- Secure all connections to prevent shorts
- Test all connections before powering on

## Testing Hardware
1. Power on Raspberry Pi
2. Verify GPIO pin voltages
3. Test motor driver with simple script
4. Calibrate ultrasonic sensors
5. Check LED functionality

## Troubleshooting
- No motor movement: Check L298N connections and power
- Inaccurate distance readings: Adjust sensor positioning
- GPIO errors: Verify pin numbers and wiring
- Overheating: Ensure proper ventilation