import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute, SetPen

class OlympicRings(Node):
    def __init__(self):
        super().__init__('olympic_rings')
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        # Service clients
        self.tele_cli = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        self.pen_cli = self.create_client(SetPen, '/turtle1/set_pen')

        # Ring config: [x, y, r, g, b] 
        # Radius set to 1.5 units. Positions adjusted for nice overlap.
        self.rings = [
            [3.5, 7.0, 0, 129, 255],   # Blue
            [5.5, 7.0, 0, 0, 0],       # Black
            [7.5, 7.0, 255, 0, 0],     # Red
            [4.5, 5.5, 255, 255, 0],   # Yellow
            [6.5, 5.5, 0, 255, 0]      # Green
        ]
        
        self.ring_index = 0
        self.state = "TELEPORT" 
        self.circle_counter = 0
        
        # Main control loop (10Hz)
        self.timer = self.create_timer(0.1, self.control_loop)

    def call_service(self, client, request):
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')
        client.call_async(request)

    def control_loop(self):
        # Check if we finished all rings
        if self.ring_index >= len(self.rings):
            if self.state != "FINISHED":
                self.get_logger().info('All rings done! Parking...')
                self.call_service(self.pen_cli, SetPen.Request(off=1))
                self.call_service(self.tele_cli, TeleportAbsolute.Request(x=5.5, y=2.0, theta=0.0))
                self.state = "FINISHED"
                return # Stop processing this iteration to avoid IndexError
            else:
                self.get_logger().info('Mission complete. Shutting down.')
                raise SystemExit

        # Safe access to current ring data
        data = self.rings[self.ring_index]

        if self.state == "TELEPORT":
            self.call_service(self.pen_cli, SetPen.Request(off=1))
            self.call_service(self.tele_cli, TeleportAbsolute.Request(x=data[0], y=data[1], theta=0.0))
            self.state = "PEN_ON"

        elif self.state == "PEN_ON":
            req = SetPen.Request(r=data[2], g=data[3], b=data[4], width=5, off=0)
            self.call_service(self.pen_cli, req)
            self.state = "DRAWING"
            self.circle_counter = 0
            self.get_logger().info(f'Drawing ring {self.ring_index + 1}/5...')

        elif self.state == "DRAWING":
            # Radius = v/w = 1.6 / 1.0 = 1.6 units
            msg = Twist()
            msg.linear.x = 1.6 
            msg.angular.z = 1.0 
            self.publisher.publish(msg)
            
            self.circle_counter += 1
            # Increased to 68 iterations (~6.8 seconds) to ensure the circle closes 
            # and overlaps slightly for a clean finish.
            if self.circle_counter > 68: 
                self.publisher.publish(Twist()) # Stop the turtle
                self.state = "TELEPORT"
                self.ring_index += 1


def main(args=None):
    rclpy.init(args=args)
    node = OlympicRings()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
