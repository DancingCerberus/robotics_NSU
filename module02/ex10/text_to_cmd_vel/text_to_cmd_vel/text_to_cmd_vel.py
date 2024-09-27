import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Twist, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        cmd = input()
        msg = Twist()
        if cmd == 'turn right':
            msg.angular.z = -1.0
        if cmd == 'turn left':
            msg.angular.z = 1.0
        if cmd == 'move forward':
            msg.linear.x = 1.0
        if cmd == 'move backward':
            msg.linear.x = -1.0

        self.publisher_.publish(msg)
        self.get_logger().info('Movement complete')


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
