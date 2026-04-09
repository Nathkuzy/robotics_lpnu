"""Shared command-line parsing for TF2 lab demos (joint configuration)."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence, Tuple

try:
    from rclpy.utilities import remove_ros_args
except ImportError:

    def remove_ros_args(args: list[str]) -> list[str]:  # type: ignore[misc]
        """Fallback when ``rclpy`` is not installed (e.g. host-side pytest)."""
        return list(args)


def parse_rtr_configuration(
    argv: Sequence[str] | None = None,
) -> Tuple[float, float, float, float, float]:
    """Parse ``theta_1 theta_2 theta_3 [l2] [l3]`` after stripping ROS arguments.

    ``theta_1``, ``theta_2``, ``theta_3`` are in radians (``theta_2`` is the
    prismatic joint coordinate in metres). ``l2``, ``l3`` are link lengths in
    metres (default 0.9 and 1.0).

    Returns:
        (theta_1, theta_2, theta_3, l2, l3)
    """
    raw = list(sys.argv if argv is None else argv)
    argv = list(remove_ros_args(raw))
    argv.pop(0)  # program name

    parser = argparse.ArgumentParser(
        description=(
            'RTR configuration: theta_1 theta_2 theta_3 [l2] [l3] '
            '(rad, rad, rad, m, m)'
        ),
        prog='tf2_*_demo',
    )
    parser.add_argument('theta_1', type=float, help='Base yaw (rad)')
    parser.add_argument(
        'theta_2',
        type=float,
        help='Prismatic joint / vertical coordinate (m)',
    )
    parser.add_argument('theta_3', type=float, help='Elbow angle (rad)')
    parser.add_argument(
        'l2',
        type=float,
        nargs='?',
        default=0.9,
        help='Upper arm length (m)',
    )
    parser.add_argument(
        'l3',
        type=float,
        nargs='?',
        default=1.0,
        help='Forearm length (m)',
    )
    ns = parser.parse_args(argv)
    return (ns.theta_1, ns.theta_2, ns.theta_3, ns.l2, ns.l3)
