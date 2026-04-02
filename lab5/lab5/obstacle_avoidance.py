"""Artificial Potential Field (APF) based obstacle avoidance

Inputs:
    /scan  - LaserScan (obstacle distances)
    /odom  - Odometry (robot pose)

Output:
    /cmd_vel - TwistStamped (velocity commands)
"""

import math
import numpy as np

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TwistStamped
from tf_transformations import euler_from_quaternion


class APFNavigationNode(Node):
    def __init__(self):
        super().__init__("apf_navigation")

        # --- Parameters (topics + goal) ---
        self.scan_topic_name = self.declare_parameter("scan_topic", "/scan").value
        self.odom_topic_name = self.declare_parameter("odom_topic", "/odom").value
        self.cmd_topic_name = self.declare_parameter("cmd_vel_topic", "/cmd_vel").value

        self.target_x = self.declare_parameter("goal_x", -2.5).value
        self.target_y = self.declare_parameter("goal_y", -1.0).value

        # --- Robot state ---
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.yaw = 0.0

        # Latest scan message
        self.laser_msg = None

        # --- APF coefficients ---
        self.k_attraction = 1.0
        self.k_repulsion = 0.4
        self.obstacle_radius = 1.0

        # --- Motion constraints ---
        self.v_max = 0.22
        self.w_max = 1.5

        # --- ROS interfaces ---
        self.create_subscription(LaserScan, self.scan_topic_name, self.lidar_cb, 10)
        self.create_subscription(Odometry, self.odom_topic_name, self.odom_cb, 10)

        self.vel_pub = self.create_publisher(TwistStamped, self.cmd_topic_name, 10)

        # Control loop at 10 Hz
        self.create_timer(0.1, self.update_control)

    def lidar_cb(self, msg):
        """Callback storing latest LIDAR scan"""
        self.laser_msg = msg

    def odom_cb(self, msg):
        """Update robot pose from odometry"""
        self.pos_x = msg.pose.pose.position.x
        self.pos_y = msg.pose.pose.position.y

        q = msg.pose.pose.orientation
        _, _, self.yaw = euler_from_quaternion([q.x, q.y, q.z, q.w])

    def attractive_component(self):
        """Compute vector pulling robot toward goal"""
        dx = self.target_x - self.pos_x
        dy = self.target_y - self.pos_y

        return np.array([self.k_attraction * dx, self.k_attraction * dy])

    def repulsive_component(self):
        """Compute obstacle avoidance vector from scan data"""
        if self.laser_msg is None:
            return np.zeros(2)

        rep_vec = np.zeros(2)
        angle = self.laser_msg.angle_min

        for dist in self.laser_msg.ranges:
            if not (math.isfinite(dist)):
                angle += self.laser_msg.angle_increment
                continue

            # Only consider nearby obstacles
            if 0.05 < dist < self.obstacle_radius:
                strength = self.k_repulsion * (1.0 / dist - 1.0 / self.obstacle_radius) / (dist ** 2)

                rep_vec[0] += -strength * math.cos(angle)
                rep_vec[1] += -strength * math.sin(angle)

            angle += self.laser_msg.angle_increment

        # Rotate vector into global frame
        c = math.cos(self.yaw)
        s = math.sin(self.yaw)

        transform = np.array([[c, -s],
                              [s,  c]])

        return transform @ rep_vec

    def update_control(self):
        """Main control step: compute velocity command"""
        # Combine forces
        f_att = self.attractive_component()
        f_rep = self.repulsive_component()
        resultant = f_att + f_rep

        # Desired orientation from resultant vector
        target_heading = math.atan2(resultant[1], resultant[0])

        # Normalize angular error
        heading_error = math.atan2(
            math.sin(target_heading - self.yaw),
            math.cos(target_heading - self.yaw)
        )

        # Distance to goal
        goal_dist = math.hypot(self.target_x - self.pos_x,
                               self.target_y - self.pos_y)

        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.header.frame_id = "base_link"

        # Stop condition near goal
        if goal_dist < 0.1:
            cmd.twist.linear.x = 0.0
            cmd.twist.angular.z = 0.0

            self.vel_pub.publish(cmd)
            self.get_logger().info(
                f"Reached goal at ({self.pos_x:.2f}, {self.pos_y:.2f})"
            )
            return

        # Angular velocity (proportional control)
        ang_gain = 0.8
        omega = ang_gain * heading_error
        cmd.twist.angular.z = max(-self.w_max, min(self.w_max, omega))

        # Linear velocity depends on alignment
        base_speed = self.v_max * (1 - abs(heading_error) / math.pi)

        # Prevent stalling
        cmd.twist.linear.x = max(0.05, min(self.v_max, base_speed))

        self.vel_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)

    node = APFNavigationNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()