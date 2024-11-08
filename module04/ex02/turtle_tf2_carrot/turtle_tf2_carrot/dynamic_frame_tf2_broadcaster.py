import math
from geometry_msgs.msg import TransformStamped
import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster, Buffer, TransformListener

class DynamicFrameBroadcaster(Node):
    def __init__(self):
        super().__init__('dynamic_frame_tf2_broadcaster')

        self.declare_parameter('radius', 1.0)
        self.declare_parameter('direction_of_rotation', 1)
        self.radius = self.get_parameter('radius').value
        self.direction_of_rotation = self.get_parameter('direction_of_rotation').value

        self.tf_broadcaster = TransformBroadcaster(self)
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.timer = self.create_timer(0.1, self.broadcast_timer_callback)
        self.angle = 0.0

    def broadcast_timer_callback(self):
        try:
            now = rclpy.time.Time()
            transform = self.tf_buffer.lookup_transform(
                'world', 'turtle1', now, timeout=rclpy.duration.Duration(seconds=1.0)
            )

            radius = self.radius
            angular_speed = 0.1

            self.angle += self.direction_of_rotation * angular_speed
            if self.angle >= 2 * math.pi:
                self.angle -= 2 * math.pi

            x_offset = radius * math.cos(self.angle)
            y_offset = radius * math.sin(self.angle)

            t = TransformStamped()
            t.header.stamp = self.get_clock().now().to_msg()
            t.header.frame_id = 'turtle1'
            t.child_frame_id = 'carrot1'
            t.transform.translation.x = x_offset
            t.transform.translation.y = y_offset
            t.transform.translation.z = 0.0

            t.transform.rotation.x = 0.0
            t.transform.rotation.y = 0.0
            t.transform.rotation.z = 0.0
            t.transform.rotation.w = 1.0

            self.tf_broadcaster.sendTransform(t)

        except Exception as e:
            self.get_logger().warn(f'Could not transform: {e}')

def main():
    rclpy.init()
    node = DynamicFrameBroadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()
