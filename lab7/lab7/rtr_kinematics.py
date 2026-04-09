"""Forward kinematics for the RTR (Revolute–Translational–Revolute) manipulator.

Joint variables: theta_1 (revolute, base yaw), theta_2 (prismatic, vertical),
theta_3 (revolute, elbow). Link lengths l2 and l3 are in metres; defaults match
the laboratory URDF (0.9 m and 1.0 m).
"""

from __future__ import annotations

import math
from typing import Tuple


def forward_position(
    theta_1: float,
    theta_2: float,
    theta_3: float,
    l2: float = 0.9,
    l3: float = 1.0,
) -> Tuple[float, float, float]:
    """End-effector position (x, y, z) in the base (world) frame.

    Horizontal reach is l3*cos(theta_3)+l2, rotated by theta_1 in XY; z is
    theta_2 + l3*sin(theta_3). See the laboratory README for the vector form.
    """
    # Horizontal reach: forearm in the plane + upper arm.
    horizontal_reach = l3 * math.cos(theta_3) + l2
    x = math.cos(theta_1) * horizontal_reach
    y = math.sin(theta_1) * horizontal_reach
    z = l3 * math.sin(theta_3) + theta_2
    return (x, y, z)


def reference_ee_orientation(theta_1: float, theta_3: float) -> Tuple[float, float, float, float]:
    """Unit quaternion (x, y, z, w) for R = Rz(theta_1) * Ry(theta_3).

    Half-angle construction; same components as the TF lab demos.
    """
    half_yaw = 0.5 * theta_1
    half_pitch = 0.5 * theta_3
    c_yaw = math.cos(half_yaw)
    s_yaw = math.sin(half_yaw)
    c_pitch = math.cos(half_pitch)
    s_pitch = math.sin(half_pitch)
    qx = s_yaw * s_pitch
    qy = s_yaw * c_pitch
    qz = c_yaw * s_pitch
    qw = c_yaw * c_pitch
    return (qx, qy, qz, qw)


def rtr_end_effector_transform(
    theta_1: float,
    theta_2: float,
    theta_3: float,
    l2: float = 0.9,
    l3: float = 1.0,
) -> Tuple[float, float, float, float, float, float, float]:
    """Pose of the RTR end-effector for TF: translation + quaternion.

    Returns ``(tx, ty, tz, qx, qy, qz, qw)`` in the base frame. Shared by
    ``tf2_broadcaster_demo`` and ``tf2_listener_demo``.
    """
    tx, ty, tz = forward_position(theta_1, theta_2, theta_3, l2, l3)
    qx, qy, qz, qw = reference_ee_orientation(theta_1, theta_3)
    return (tx, ty, tz, qx, qy, qz, qw)


def tf_pose_matches_rtr_analytical(
    trans_x: float,
    trans_y: float,
    trans_z: float,
    rot_x: float,
    rot_y: float,
    rot_z: float,
    rot_w: float,
    theta_1: float,
    theta_2: float,
    theta_3: float,
    l2: float = 0.9,
    l3: float = 1.0,
    pos_tol: float = 1e-4,
    quat_dot_tol: float = 1e-4,
) -> bool:
    """Return True if a TF snapshot matches closed-form RTR pose for the given joints."""
    ex, ey, ez = forward_position(theta_1, theta_2, theta_3, l2, l3)
    if (
        abs(trans_x - ex) > pos_tol
        or abs(trans_y - ey) > pos_tol
        or abs(trans_z - ez) > pos_tol
    ):
        return False
    exx, eyy, ezz, eww = reference_ee_orientation(theta_1, theta_3)
    dot = abs(
        rot_x * exx + rot_y * eyy + rot_z * ezz + rot_w * eww,
    )
    return dot > (1.0 - quat_dot_tol)
