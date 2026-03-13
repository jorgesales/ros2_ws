import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute, SetPen

class OlympicRingsExercise(Node):
    def __init__(self):
        super().__init__('olympic_rings_exercise')
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.tele_cli = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        self.pen_cli = self.create_client(SetPen, '/turtle1/set_pen')

        # EXERCISE 0: Complete the ring coordinates and colors!
        # Format: [X, Y, Red, Green, Blue]
        # Hint: Turtlesim screen is 11x11. Blue is (0, 129, 255).
        self.rings = [
            [3.5, 7.0, 0, 129, 255],   # 1. Blue (EXAMPLE)
            [0.0, 0.0, 0, 0, 0],       # 2. Black (STUDENT: Set X, Y)
            [0.0, 0.0, 0, 0, 0],       # 3. Red (STUDENT: Set X, Y, R, G, B)
            [0.0, 0.0, 0, 0, 0],       # 4. Yellow (STUDENT: Set X, Y, R, G, B)
            [0.0, 0.0, 0, 0, 0]        # 5. Green (STUDENT: Set X, Y, R, G, B)
        ]
        
        self.ring_index = 0
        self.state = "TELEPORT" 
        self.circle_counter = 0
        self.timer = self.create_timer(0.1, self.control_loop)

    def call_service(self, client, request):
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')
        client.call_async(request)

    def control_loop(self):
        # 0. CHECK IF ALL RINGS ARE FINISHED
        if self.ring_index >= len(self.rings):
            if self.state != "FINISHED":
                self.get_logger().info('All rings done! Parking...')
                # EXERCISE 1: Park the turtle at (x=5.5, y=2.0)
                self.call_service(self.pen_cli, SetPen.Request(off=1))
                x_park = None  # <--- STUDENT
                y_park = None  # <--- STUDENT
                self.call_service(self.tele_cli, TeleportAbsolute.Request(x=x_park, y=y_park, theta=0.0))
                self.state = "FINISHED"
                return 
            else:
                self.get_logger().info('Exercise Complete!')
                raise SystemExit

        data = self.rings[self.ring_index]

        if self.state == "TELEPORT":
            self.get_logger().info(f'Moving to ring {self.ring_index + 1}...')
            # EXERCISE 2: Lift the pen (off=1)
            self.call_service(self.pen_cli, SetPen.Request(off=1))
            
            # EXERCISE 3: Teleport to the ring center
            x_pos = data[0] # EXAMPLE: x is at index 0
            y_pos = None    # STUDENT: y index?
            self.call_service(self.tele_cli, TeleportAbsolute.Request(x=x_pos, y=y_pos, theta=0.0))
            self.state = "PEN_ON"

        elif self.state == "PEN_ON":
            self.get_logger().info('Setting pen color...')
            # EXERCISE 4: Get RGB values from the 'data' list
            r_val = data[2] # EXAMPLE: Red is at index 2
            g_val = None    # STUDENT: Green index?
            b_val = None    # STUDENT: Blue index?
            
            req_color = SetPen.Request(r=r_val, g=g_val, b=b_val, width=5, off=0)
            self.call_service(self.pen_cli, req_color)
            self.state = "DRAWING"
            self.circle_counter = 0

        elif self.state == "DRAWING":
            # EXERCISE 5: Set velocities (Try linear.x=1.5 and angular.z=1.0)
            msg = Twist()
            msg.linear.x = 0.0  # <--- STUDENT
            msg.angular.z = 0.0 # <--- STUDENT
            self.publisher.publish(msg)
            
            self.circle_counter += 1
            # EXERCISE 6: Close the circle (Try 68 steps)
            if self.circle_counter > 0: # <--- STUDENT
                self.publisher.publish(Twist()) 
                self.state = "TELEPORT"
                self.ring_index += 1

def main(args=None):
    rclpy.init(args=args)
    node = OlympicRingsExercise()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
