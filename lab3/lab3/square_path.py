"""Square path using odometry feedback. Base code for students."""
import time
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TwistStamped
from nav_msgs.msg import Odometry


class SquarePath(Node):
    def __init__(self):
        super().__init__('square_path')

        self.declare_parameter('side_length', 2.0)
        self.declare_parameter('linear_speed', 0.4)
        self.declare_parameter('angular_speed', 0.8)
        self.declare_parameter('odom_topic', '/model/vehicle_blue/odometry')

        odom_topic = self.get_parameter('odom_topic').value
        self.pub = self.create_publisher(TwistStamped, "/cmd_vel", 10)
        self.odom_sub = self.create_subscription(
            Odometry,
            odom_topic,
            self.odom_callback,
            10
        )

        self.current_x = 0.0
        self.current_y = 0.0
        self.current_theta = 0.0
        self.odom_received = False

        self.get_logger().info("Waiting for odometry...")
        while not self.odom_received:
            rclpy.spin_once(self, timeout_sec=0.1)

        time.sleep(0.5)
        self.get_logger().info("Starting square path")

        side = self.get_parameter('side_length').value

        for i in range(4):
            self.get_logger().info(f"Side {i+1}/4")
            self.move_forward(distance=side)
            time.sleep(0.3)
            self.turn(angle=math.pi / 2.0)
            time.sleep(0.3)

        self.get_logger().info("Square complete!")
        self.pub.publish(TwistStamped())

    def odom_callback(self, msg: Odometry):
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        siny = 2.0 * (q.w * q.z + q.x * q.y)
        cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        self.current_theta = math.atan2(siny, cosy)
        self.odom_received = True

    def move_forward(self, distance):
        start_x = self.current_x
        start_y = self.current_y
        speed = self.get_parameter('linear_speed').value

        cmd = TwistStamped()
        cmd.header.frame_id = 'base_link'
        cmd.twist.linear.x = speed
        cmd.header.stamp = self.get_clock().now().to_msg()

        while True:
            dx = self.current_x - start_x
            dy = self.current_y - start_y
            if math.sqrt(dx*dx + dy*dy) >= distance:
                break
            self.pub.publish(cmd)
            rclpy.spin_once(self, timeout_sec=0.01)

        cmd.twist.linear.x = 0.0
        self.pub.publish(cmd)

    def turn(self, angle):
        start_theta = self.current_theta
        speed = self.get_parameter('angular_speed').value

        cmd = TwistStamped()
        cmd.header.frame_id = 'base_link'
        cmd.twist.angular.z = speed
        cmd.header.stamp = self.get_clock().now().to_msg()

        while True:
            turned = self.current_theta - start_theta
            while turned > math.pi:
                turned -= 2.0 * math.pi
            while turned < -math.pi:
                turned += 2.0 * math.pi
            if abs(turned) >= angle:
                break
            self.pub.publish(cmd)
            rclpy.spin_once(self, timeout_sec=0.01)

        cmd.twist.angular.z = 0.0
        self.pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = SquarePath()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
