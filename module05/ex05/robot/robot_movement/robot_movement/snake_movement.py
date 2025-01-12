import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MovementsNode(Node):
    def __init__(self):
        super().__init__('movements_node')
        self.publisher_ = self.create_publisher(Twist, '/robot/cmd_vel', 10)
        self.timer_period = 1.0
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        self.state = 0
        self.state_duration = 0
        self.max_half_duration = 5

    def timer_callback(self):
        twist_msg = Twist()

        if self.state == 0:
            self.get_logger().info("First half of movement")
            twist_msg.linear.x = 0.5
            twist_msg.angular.z = 0.5
            self.state_duration += self.timer_period
            if self.state_duration >= self.max_half_duration:
                self.state = 1
                self.state_duration = 0

        elif self.state == 1:
            self.get_logger().info("Second half of movement")
            twist_msg.linear.x = 0.5
            twist_msg.angular.z = -0.5
            self.state_duration += self.timer_period
            if self.state_duration >= self.max_half_duration:
                self.state = 0
                self.state_duration = 0

        self.publisher_.publish(twist_msg)


def main(args=None):
    rclpy.init(args=args)
    node = MovementsNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
