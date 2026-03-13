import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute, SetPen

class OlympicRingsSolution(Node):
    def __init__(self):
        super().__init__('olympic_rings_solution')
        # Publisher to control turtle movement
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        # Service clients to jump and change colors
        self.tele_cli = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        self.pen_cli = self.create_client(SetPen, '/turtle1/set_pen')

        # SOLUTION 0: Complete ring coordinates and colors
        # Format: [X, Y, Red, Green, Blue]
        self.rings = [
            [3.5, 7.0, 0, 129, 255],   # 1. Blue
            [5.5, 7.0, 0, 0, 0],       # 2. Black
            [7.5, 7.0, 255, 0, 0],     # 3. Red
            [4.5, 5.5, 255, 255, 0],   # 4. Yellow
            [6.5, 5.5, 0, 255, 0]      # 5. Green
        ]
        
        self.ring_index = 0
        self.state = "TELEPORT" 
        self.circle_counter = 0
        
        # Timer: executes the control_loop every 0.1 seconds (10Hz)
        self.timer = self.create_timer(0.1, self.control_loop)

    def call_service(self, client, request):
        """Helper function to call services asynchronously."""
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')
        client.call_async(request)

    def control_loop(self):
        # 0. CHECK IF ALL RINGS ARE FINISHED
        if self.ring_index >= len(self.rings):
            if self.state != "FINISHED":
                self.get_logger().info('All rings done! Parking...')
                # SOLUTION 1: Lift pen and park at center bottom (5.5, 2.0)
                self.call_service(self.pen_cli, SetPen.Request(off=1))
                
                x_park = 5.5
                y_park = 2.0
                
                req_park = TeleportAbsolute.Request(x=x_park, y=y_park, theta=0.0)
                self.call_service(self.tele_cli, req_park)
                
                self.state = "FINISHED"
                return 
            else:
                self.get_logger().info('Mission Complete!')
                raise SystemExit

        # Current ring information: [x, y, r, g, b]
        data = self.rings[self.ring_index]

        if self.state == "TELEPORT":
            self.get_logger().info(f'Moving to ring {self.ring_index + 1}...')
            # SOLUTION 2: Lift the pen
            self.call_service(self.pen_cli, SetPen.Request(off=1))
            
            # SOLUTION 3: Teleport to coordinates from data list
            x_pos = data[0] 
            y_pos = data[1]
            
            req_tele = TeleportAbsolute.Request(x=x_pos, y=y_pos, theta=0.0)
            self.call_service(self.tele_cli, req_tele)
            
            self.state = "PEN_ON"

        elif self.state == "PEN_ON":
            self.get_logger().info('Setting pen color...')
            # SOLUTION 4: Extract RGB values using correct indices
            r_val = data[2]
            g_val = data[3]
            b_val = data[4]
            
            req_color = SetPen.Request(r=r_val, g=g_val, b=b_val, width=5, off=0)
            self.call_service(self.pen_cli, req_color)
            
            self.state = "DRAWING"
            self.circle_counter = 0

        elif self.state == "DRAWING":
            # SOLUTION 5: Set velocities (Radius = 1.5/1.0 = 1.5 units)
            msg = Twist()
            msg.linear.x = 1.5
            msg.angular.z = 1.0
            self.publisher.publish(msg)
            
            self.circle_counter += 1
            # SOLUTION 6: Close the circle (approx 68 steps for 2*PI)
            if self.circle_counter > 68:
                self.publisher.publish(Twist()) # Stop the turtle
                self.state = "TELEPORT"
                self.ring_index += 1

def main(args=None):
    rclpy.init(args=args)
    node = OlympicRingsSolution()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
