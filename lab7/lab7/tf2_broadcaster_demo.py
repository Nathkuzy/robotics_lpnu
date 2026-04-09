#!/usr/bin/env python3
"""TF broadcaster: one fixed RTR configuration from the command line.

Publishes ``world`` -> ``rtr_ee_demo`` at 10 Hz so listeners can buffer the
transform. Joint values are ``theta_1``, ``theta_2``, ``theta_3`` plus optional
``l2``, ``l3`` (see ``tf2_demo_cli.parse_rtr_configuration``).

Pose math is implemented in :func:`lab7.rtr_kinematics.rtr_end_effector_transform`.
"""

from __future__ import annotations

import sys

import rclpy
from geometry_msgs.msg import TransformStamped
from rclpy.node import Node
from tf2_ros.transform_broadcaster import TransformBroadcaster

from lab7.rtr_kinematics import rtr_end_effector_transform
from lab7.tf2_demo_cli import parse_rtr_configuration


class RtrTfBroadcasterDemo(Node):
    """Broadcasts a constant end-effector pose for one RTR configuration."""

    def __init__(
        self,
        theta_1: float,
        theta_2: float,
        theta_3: float,
        l2: float,
        l3: float,
    ) -> None:
        super().__init__('rtr_tf2_broadcaster_demo')
        self._tf_broadcaster = TransformBroadcaster(self)
        self._theta_1 = theta_1
        self._theta_2 = theta_2
        self._theta_3 = theta_3
        self._l2 = l2
        self._l3 = l3
        self._timer = self.create_timer(0.1, self._on_timer)

    def _on_timer(self) -> None:
        tx, ty, tz, qx, qy, qz, qw = rtr_end_effector_transform(
            self._theta_1,
            self._theta_2,
            self._theta_3,
            self._l2,
            self._l3,
        )
        msg = TransformStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'world'
        msg.child_frame_id = 'rtr_ee_demo'
        msg.transform.translation.x = float(tx)
        msg.transform.translation.y = float(ty)
        msg.transform.translation.z = float(tz)
        msg.transform.rotation.x = float(qx)
        msg.transform.rotation.y = float(qy)
        msg.transform.rotation.z = float(qz)
        msg.transform.rotation.w = float(qw)
        self._tf_broadcaster.sendTransform(msg)


def main(argv: list[str] | None = None) -> None:
    """Parse joint CLI, spin broadcaster, shut down."""
    argv = argv if argv is not None else sys.argv
    rclpy.init(args=argv)
    t1, t2, t3, l2, l3 = parse_rtr_configuration(argv)
    node = RtrTfBroadcasterDemo(t1, t2, t3, l2, l3)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
