import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TurtleSquare(Node):
    def __init__(self):
        super().__init__('turtle_square')
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(2.0, self.timer_callback)
        self.step = 0

    def timer_callback(self):
        msg = Twist()
        
        if self.step < 8:
            if self.step % 2 == 0:
                msg.linear.x = 2.0
                msg.angular.z = 0.0
            else:
                msg.linear.x = 0.0
                msg.angular.z = 1.5708
            
            self.publisher.publish(msg)
            self.step += 1
        else:
            # SHUTDOWN SEQUENCE
            self.publisher.publish(Twist()) # Send empty twist to stop turtle
            self.get_logger().info('Square Finished! Shutting down...')
            
            # Clean exit
            self.timer.cancel()
            self.destroy_node()
            rclpy.shutdown()

def main():
    rclpy.init()
    node = TurtleSquare()
    try:
        rclpy.spin(node)
    except rclpy.executors.ExternalShutdownException:
        pass

if __name__ == '__main__':
    main()
