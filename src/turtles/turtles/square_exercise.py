import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TurtleSquare(Node):
    def __init__(self):
        super().__init__('turtle_square')
        
        # 1. Create a publisher for '/turtle1/cmd_vel'
        self.publisher = self.create_publisher(______, '/turtle1/cmd_vel', 10)
        
        # 2. Create a timer that triggers every 2 seconds
        self.timer = self.create_timer(2.0, self.______)
        
        # Step counter (0 to 7)
        self.step = 0

    def timer_callback(self):
        msg = Twist()

        if self.step < 8:
            # Check if step is EVEN (Move forward) or ODD (Turn 90 deg)
            if self.step % 2 == 0:
                # MOVE FORWARD
                msg.linear.x = 2.0
                msg.angular.z = ______  # Go straight
                self.get_logger().info(f'Step {self.step}: Moving forward')
            else:
                # TURN 90 DEGREES
                msg.linear.x = 0.0
                msg.angular.z = ______  # 90 degrees in radians (approx. 1.57)
                self.get_logger().info(f'Step {self.step}: Turning')

            # 3. Publish the message
            self.______.publish(msg)
            self.step += 1
        
        else:
            # SHUTDOWN SEQUENCE
            self.get_logger().info('Square Finished! Shutting down...')
            
            # Stop the turtle before leaving
            self.publisher.publish(Twist())
            
            # 4. Cleanup and exit
            self.timer.______  # Stop the timer
            self.destroy_node()
            rclpy.______  # Stop the ROS 2 process

def main(args=None):
    rclpy.init(args=args)
    square_node = TurtleSquare()
    
    try:
        rclpy.spin(square_node)
    except (rclpy.executors.ExternalShutdownException, KeyboardInterrupt):
        pass

if __name__ == '__main__':
    main()
