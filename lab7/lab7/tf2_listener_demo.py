#!/usr/bin/env python3
"""TF listener: same CLI joints as the broadcaster; checks TF vs analytic pose.

Run the broadcaster in another terminal with the **same** five numbers
``theta_1 theta_2 theta_3 [l2] [l3]``. Expected pose comes from
:func:`lab7.rtr_kinematics.rtr_end_effector_transform` and is compared to
``lookup_transform(world, rtr_ee_demo)``.
"""

from __future__ import annotations

import sys

import rclpy
from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from tf2_ros import TransformException

from lab7.rtr_kinematics import rtr_end_effector_transform
from lab7.tf2_demo_cli import parse_rtr_configuration


class RtrTfListenerDemo(Node):
    """Compares analytic RTR end-effector pose to the TF tree."""

    def __init__(
        self,
        theta_1: float,
        theta_2: float,
        theta_3: float,
        l2: float,
        l3: float,
    ) -> None:
        super().__init__('rtr_tf2_listener_demo')
        self._target = 'world'
        self._source = 'rtr_ee_demo'
        self._theta_1 = theta_1
        self._theta_2 = theta_2
        self._theta_3 = theta_3
        self._l2 = l2
        self._l3 = l3
        self._pos_tol = 1e-4
        self._quat_dot_tol = 1e-4
        self._buffer = Buffer(cache_time=Duration(seconds=10.0))
        self._listener = TransformListener(self._buffer, self)
        self._timer = self.create_timer(0.5, self._on_timer)

    def _on_timer(self) -> None:
        exp_x, exp_y, exp_z, exp_qx, exp_qy, exp_qz, exp_qw = (
            rtr_end_effector_transform(
                self._theta_1,
                self._theta_2,
                self._theta_3,
                self._l2,
                self._l3,
            )
        )

        try:
            if not self._buffer.can_transform(
                self._target,
                self._source,
                Time(),
                timeout=Duration(seconds=0, nanoseconds=200_000_000),
            ):
                self.get_logger().warn(
                    f'waiting for transform {self._target} <- {self._source}…',
                )
                return
            t = self._buffer.lookup_transform(self._target, self._source, Time())
        except TransformException as exc:
            self.get_logger().warn(f'lookup failed: {exc}')
            return

        px = t.transform.translation.x
        py = t.transform.translation.y
        pz = t.transform.translation.z
        rx = t.transform.rotation.x
        ry = t.transform.rotation.y
        rz = t.transform.rotation.z
        rw = t.transform.rotation.w

        dx = abs(px - exp_x)
        dy = abs(py - exp_y)
        dz = abs(pz - exp_z)
        pos_ok = dx <= self._pos_tol and dy <= self._pos_tol and dz <= self._pos_tol

        quat_dot = abs(
            rx * exp_qx + ry * exp_qy + rz * exp_qz + rw * exp_qw,
        )
        ori_ok = quat_dot > (1.0 - self._quat_dot_tol)

        if pos_ok and ori_ok:
            self.get_logger().info(
                'TF matches analytic RTR pose '
                f'(pos err max {max(dx, dy, dz):.2e} m, |q·q_exp|={quat_dot:.6f}).',
            )
        else:
            self.get_logger().error(
                'Mismatch: analytic '
                f'({exp_x:.4f},{exp_y:.4f},{exp_z:.4f}) '
                f'q=({exp_qx:.4f},…,{exp_qw:.4f}) '
                f'vs TF ({px:.4f},{py:.4f},{pz:.4f}) q=({rx:.4f},…,{rw:.4f}) '
                f'pos_ok={pos_ok} ori_ok={ori_ok}',
            )


def main(argv: list[str] | None = None) -> None:
    argv = argv if argv is not None else sys.argv
    rclpy.init(args=argv)
    t1, t2, t3, l2, l3 = parse_rtr_configuration(argv)
    node = RtrTfListenerDemo(t1, t2, t3, l2, l3)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
