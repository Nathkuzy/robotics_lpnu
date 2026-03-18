"""
Dead reckoning node: integrates velocity commands into a pose estimate.
"""

import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped, PoseStamped
from nav_msgs.msg import Odometry, Path


class DeadReckoningNode(Node):
    def __init__(self):
        super().__init__("dead_reckoning")

        self.declare_parameter("cmd_vel_topic", "/cmd_vel")
        self.declare_parameter("ground_truth_topic", "/odom")
        self.declare_parameter("path_dr_topic", "/path_dr")
        self.declare_parameter("frame_id", "odom")
        self.declare_parameter("max_poses", 2000)

        self.cmd_topic = self.get_parameter("cmd_vel_topic").value
        self.gt_topic = self.get_parameter("ground_truth_topic").value
        self.path_topic = self.get_parameter("path_dr_topic").value
        self.frame_id = self.get_parameter("frame_id").value
        self.max_poses = int(self.get_parameter("max_poses").value)

        self.create_subscription(TwistStamped, self.cmd_topic, self._on_cmd, 10)
        self.create_subscription(Odometry, self.gt_topic, self._on_gt, 10)
        self.path_pub = self.create_publisher(Path, self.path_topic, 10)

        self._pose = [0.0, 0.0, 0.0] 
        self._last_time = None

        # Ground truth storage
        self._gt_pose = None

        # Path message
        self._path = Path()
        self._path.header.frame_id = self.frame_id

    def _on_cmd(self, msg: TwistStamped):
        now = self.get_clock().now().nanoseconds * 1e-9

        if self._last_time is None:
            self._last_time = now
            return

        dt = now - self._last_time
        self._last_time = now

        v = msg.twist.linear.x
        w = msg.twist.angular.z

        self._integrate_motion(v, w, dt)
        self._publish_path(msg.header.stamp)

    def _on_gt(self, msg: Odometry):
        pos = msg.pose.pose.position
        ori = msg.pose.pose.orientation

        yaw = math.atan2(
            2.0 * (ori.w * ori.z + ori.x * ori.y),
            1.0 - 2.0 * (ori.y * ori.y + ori.z * ori.z),
        )

        self._gt_pose = (pos.x, pos.y, yaw)

    def _integrate_motion(self, v, w, dt):
        x, y, theta = self._pose

        x += v * math.cos(theta) * dt
        y += v * math.sin(theta) * dt
        theta += w * dt

        # Normalize angle
        theta = math.atan2(math.sin(theta), math.cos(theta))

        self._pose = [x, y, theta]

    def _publish_path(self, stamp):
        x, y, theta = self._pose

        pose_msg = PoseStamped()
        pose_msg.header.stamp = stamp
        pose_msg.header.frame_id = self.frame_id

        pose_msg.pose.position.x = x
        pose_msg.pose.position.y = y

        qz, qw = self._yaw_to_quaternion(theta)
        pose_msg.pose.orientation.z = qz
        pose_msg.pose.orientation.w = qw

        self._path.header.stamp = stamp
        self._path.poses.append(pose_msg)

        if len(self._path.poses) > self.max_poses:
            self._path.poses.pop(0)

        self.path_pub.publish(self._path)

    @staticmethod
    def _yaw_to_quaternion(yaw):
        return math.sin(yaw / 2.0), math.cos(yaw / 2.0)


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