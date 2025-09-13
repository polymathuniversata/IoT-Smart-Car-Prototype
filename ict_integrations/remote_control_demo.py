# ICT Integration: Simple Remote Control Simulation
# Demonstrates basic remote control concepts for robotics education
# This is a simplified example - real implementation would use actual communication protocols

import socket
import threading
import time

class SimpleRobotController:
    def __init__(self):
        self.position = [0, 0]  # x, y coordinates
        self.direction = 0  # 0-360 degrees

    def move_forward(self, distance):
        """Simulate moving forward"""
        self.position[1] += distance
        print(f"Robot moved forward. New position: {self.position}")

    def turn_left(self, angle):
        """Simulate turning left"""
        self.direction = (self.direction - angle) % 360
        print(f"Robot turned left {angle}°. New direction: {self.direction}°")

    def get_status(self):
        """Get robot status"""
        return f"Position: {self.position}, Direction: {self.direction}°"

def handle_client(client_socket, robot):
    """Handle client commands"""
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            command = data.strip().lower()
            if command == 'forward':
                robot.move_forward(10)
                response = "Moved forward"
            elif command == 'left':
                robot.turn_left(90)
                response = "Turned left"
            elif command == 'status':
                response = robot.get_status()
            else:
                response = "Unknown command"

            client_socket.send(response.encode())

        except:
            break

    client_socket.close()

def main():
    robot = SimpleRobotController()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen(5)

    print("Remote control server started on localhost:12345")
    print("Available commands: 'forward', 'left', 'status'")

    try:
        while True:
            client_socket, addr = server.accept()
            print(f"Connection from {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket, robot))
            client_handler.start()

    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.close()

if __name__ == "__main__":
    main()