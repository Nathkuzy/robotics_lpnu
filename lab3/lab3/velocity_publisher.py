"""Publish constant velocity for testing. Prints wheel speeds from diff_drive_math."""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped

from .diff_drive_math import twist_to_wheel_speeds, curve_radius


class VelocityPublisher(Node):
    def __init__(self):
        super().__init__("velocity_publisher")

        self.declare_parameter("linear_x", 0.20)
        self.declare_parameter("angular_z", 0.00)
        self.declare_parameter("rate_hz", 10.0)
        self.declare_parameter("wheel_radius", 0.15)
        self.declare_parameter("wheel_separation", 0.7)

        self.pub = self.create_publisher(TwistStamped, "/cmd_vel", 10)
        period = 1.0 / max(float(self.get_parameter("rate_hz").value), 1.0)
        self.timer = self.create_timer(period, self.on_timer)

        self.get_logger().info("velocity_publisher: publishing to /cmd_vel")

    def on_timer(self):
        v = float(self.get_parameter("linear_x").value)
        w = float(self.get_parameter("angular_z").value)

        msg = TwistStamped()
        msg.header.frame_id = 'base_link'
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.twist.linear.x = v
        msg.twist.angular.z = w
        self.pub.publish(msg)

        r = curve_radius(v, w)
        wheel_radius = float(self.get_parameter("wheel_radius").value)
        wheel_sep = float(self.get_parameter("wheel_separation").value)
        wl, wr = twist_to_wheel_speeds(v, w, wheel_radius, wheel_sep)

        r_txt = "inf" if r == float("inf") else f"{r:.3f} m"
        self.get_logger().info(
            f"v={v:.2f} m/s, w={w:.2f} rad/s | radius={r_txt} | wheel ω: L={wl:.2f}, R={wr:.2f} rad/s"
        )


def main(args=None):
    rclpy.init(args=args)
    node = VelocityPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()
