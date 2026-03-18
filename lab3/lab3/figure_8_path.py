"""Figure-8 path using timed motion."""
import time
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped


class Figure8Path(Node):
    def __init__(self):
        super().__init__('figure_8_path')

        self.declare_parameter("linear_speed", 0.3)
        self.declare_parameter("angular_speed", 0.3)
        self.declare_parameter("rate_hz", 20.0)

        self.pub = self.create_publisher(TwistStamped, "/cmd_vel", 10)

        v = float(self.get_parameter("linear_speed").value)
        w = float(self.get_parameter("angular_speed").value)
        dt = 1.0 / max(float(self.get_parameter("rate_hz").value), 1.0)

        duration = 2.0 * math.pi / max(abs(w), 1e-6)

        self.get_logger().info(
            f"Figure-8: v={v:.2f}, |w|={abs(w):.2f}, circle_time={duration:.2f}s"
        )

        msg = TwistStamped()
        msg.header.frame_id = "base_link"
        msg.twist.linear.x = v

        # First circle (counter-clockwise) 
        msg.twist.angular.z = abs(w)
        self.get_logger().info("Starting left circle")

        t_end = time.time() + duration
        while time.time() < t_end:
            msg.header.stamp = self.get_clock().now().to_msg()
            self.pub.publish(msg)
            rclpy.spin_once(self, timeout_sec=0.0)
            time.sleep(dt)

        # Second circle (clockwise)
        msg.twist.angular.z = -abs(w)
        self.get_logger().info("Starting right circle")

        t_end = time.time() + duration
        while time.time() < t_end:
            msg.header.stamp = self.get_clock().now().to_msg()
            self.pub.publish(msg)
            rclpy.spin_once(self, timeout_sec=0.0)
            time.sleep(dt)

        self.pub.publish(TwistStamped())
        self.get_logger().info("Figure-8 complete.")

        self.destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = Figure8Path()
    rclpy.shutdown()