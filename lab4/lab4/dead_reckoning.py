"""Dead reckoning - STUDENT TASK.

Integrate /cmd_vel to estimate pose; compare with Gazebo ground truth (/odom).

Reference: https://www.roboticsbook.org/S52_diffdrive_actions.html
"""
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import PoseStamped


class DeadReckoningNode(Node):
    def __init__(self):
        super().__init__("dead_reckoning")

        self.declare_parameter("cmd_vel_topic", "/cmd_vel")
        self.declare_parameter("ground_truth_topic", "/odom")
        self.declare_parameter("path_dr_topic", "/path_dr")
        self.declare_parameter("frame_id", "odom")
        self.declare_parameter("max_poses", 2000)

        cmd_topic = self.get_parameter("cmd_vel_topic").value
        gt_topic = self.get_parameter("ground_truth_topic").value
        path_topic = self.get_parameter("path_dr_topic").value
        self.frame_id = self.get_parameter("frame_id").value
        self.max_poses = int(self.get_parameter("max_poses").value)

        self.create_subscription(TwistStamped, cmd_topic, self.cmd_callback, 10)
        self.create_subscription(Odometry, gt_topic, self.gt_callback, 10)
        self.pub_path = self.create_publisher(Path, path_topic, 10)

        # TODO: add state variables (pose, time, ground truth)
        self.path_msg = Path()
        self.path_msg.header.frame_id = self.frame_id

    def cmd_callback(self, msg: TwistStamped):
        # TODO: integrate v, w to update pose; publish path
        pass

    def gt_callback(self, msg: Odometry):
        # TODO: store ground truth for comparison
        pass


def main(args=None):
    rclpy.init(args=args)
    node = DeadReckoningNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
