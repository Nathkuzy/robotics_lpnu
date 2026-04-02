"""Obstacle avoidance

Implement potential fields (or Bug, Tangent Bug, DWA, RL).
Use /scan (LaserScan) and /odom; publish /cmd_vel.
"""
import rclpy
from rclpy.node import Node


class ObstacleAvoidanceNode(Node):
    def __init__(self):
        super().__init__("obstacle_avoidance")

        self.declare_parameter("scan_topic", "/scan")
        self.declare_parameter("odom_topic", "/odom")
        self.declare_parameter("cmd_vel_topic", "/cmd_vel")
        self.declare_parameter("goal_x", 3.0)
        self.declare_parameter("goal_y", 3.0)

        # TODO: subscribe to scan, odom; publish cmd_vel

    def scan_callback(self, msg):
        # TODO
        pass

    def odom_callback(self, msg):
        # TODO
        pass


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidanceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
