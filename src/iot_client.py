# IoT Smart Car - MQTT Client Module
# Handles IoT connectivity for remote control and data transmission

import paho.mqtt.client as mqtt
import json
import time
import threading
from car_control import SmartCar

class IoTCarClient:
    def __init__(self, car_controller, broker="broker.hivemq.com", port=1883):
        self.car = car_controller
        self.broker = broker
        self.port = port
        self.client_id = "iot_smart_car_001"

        # MQTT topics
        self.control_topic = "smartcar/control"
        self.status_topic = "smartcar/status"
        self.telemetry_topic = "smartcar/telemetry"

        # Setup MQTT client
        self.client = mqtt.Client(client_id=self.client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        # Status reporting
        self.reporting = False
        self.report_interval = 5  # seconds

    def on_connect(self, client, userdata, flags, rc):
        """Callback for when client connects to broker"""
        if rc == 0:
            print("Connected to MQTT broker")
            # Subscribe to control topic
            self.client.subscribe(self.control_topic)
            print(f"Subscribed to {self.control_topic}")
        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        """Callback for when message is received"""
        try:
            payload = json.loads(msg.payload.decode())
            print(f"Received command: {payload}")

            command = payload.get('command', '')
            params = payload.get('params', {})

            self.execute_command(command, params)

        except json.JSONDecodeError:
            print("Invalid JSON received")
        except Exception as e:
            print(f"Error processing message: {e}")

    def on_disconnect(self, client, userdata, rc):
        """Callback for disconnection"""
        print("Disconnected from MQTT broker")
        if rc != 0:
            print("Unexpected disconnection, attempting to reconnect...")
            self.connect()

    def execute_command(self, command, params):
        """Execute received command"""
        if command == "move_forward":
            speed = params.get('speed', self.car.speed)
            self.car.set_speed(speed)
            self.car.move_forward()
            self.publish_status()

        elif command == "move_backward":
            speed = params.get('speed', self.car.speed)
            self.car.set_speed(speed)
            self.car.move_backward()
            self.publish_status()

        elif command == "turn_left":
            speed = params.get('speed', self.car.speed)
            self.car.set_speed(speed)
            self.car.turn_left()
            self.publish_status()

        elif command == "turn_right":
            speed = params.get('speed', self.car.speed)
            self.car.set_speed(speed)
            self.car.turn_right()
            self.publish_status()

        elif command == "stop":
            self.car.stop()
            self.publish_status()

        elif command == "set_speed":
            speed = params.get('speed', 50)
            self.car.set_speed(speed)
            self.publish_status()

        elif command == "set_mode":
            mode = params.get('mode', 'manual')
            self.car.set_mode(mode)
            if mode == "autonomous":
                self.car.start_autonomous()
            else:
                self.car.stop_autonomous()
            self.publish_status()

        elif command == "get_status":
            self.publish_status()

        else:
            print(f"Unknown command: {command}")

    def publish_status(self):
        """Publish car status to MQTT"""
        status = self.car.get_status()
        status_json = json.dumps(status)

        self.client.publish(self.status_topic, status_json)
        print(f"Published status: {status}")

    def publish_telemetry(self):
        """Publish telemetry data periodically"""
        while self.reporting:
            telemetry = {
                'timestamp': time.time(),
                'status': self.car.status,
                'mode': self.car.mode,
                'speed': self.car.speed,
                'distances': self.car.sensors.get_all_distances(),
                'battery_level': 85  # Placeholder - would need actual sensor
            }

            telemetry_json = json.dumps(telemetry)
            self.client.publish(self.telemetry_topic, telemetry_json)
            print(f"Published telemetry: {telemetry}")

            time.sleep(self.report_interval)

    def connect(self):
        """Connect to MQTT broker"""
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
        except Exception as e:
            print(f"Failed to connect to MQTT broker: {e}")

    def start_reporting(self):
        """Start telemetry reporting"""
        if not self.reporting:
            self.reporting = True
            self.telemetry_thread = threading.Thread(target=self.publish_telemetry)
            self.telemetry_thread.start()
            print("Telemetry reporting started")

    def stop_reporting(self):
        """Stop telemetry reporting"""
        self.reporting = False
        print("Telemetry reporting stopped")

    def disconnect(self):
        """Disconnect from MQTT broker"""
        self.stop_reporting()
        self.client.loop_stop()
        self.client.disconnect()

# Example usage
if __name__ == "__main__":
    from car_control import SmartCar

    car = SmartCar()
    iot_client = IoTCarClient(car)

    try:
        iot_client.connect()
        iot_client.start_reporting()

        print("IoT Smart Car connected. Waiting for commands...")
        print("Press Ctrl+C to exit")

        # Keep running
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        iot_client.disconnect()
        car.cleanup()