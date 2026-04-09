"""RTR end-effector transform, TF matcher, and CLI parsing tests."""

import math

from lab7.rtr_kinematics import (
    forward_position,
    reference_ee_orientation,
    rtr_end_effector_transform,
    tf_pose_matches_rtr_analytical,
)
from lab7.tf2_demo_cli import parse_rtr_configuration


def test_rtr_end_effector_transform_matches_components() -> None:
    """``rtr_end_effector_transform`` equals position + orientation helpers."""
    for t1, t2, t3 in [
        (0.0, 0.0, 0.0),
        (0.3, 0.25, -0.4),
        (1.1, 0.8, 0.9),
        (-0.5, 1.0, math.pi / 4),
    ]:
        l2, l3 = 0.9, 1.0
        tx, ty, tz, qx, qy, qz, qw = rtr_end_effector_transform(
            t1, t2, t3, l2, l3,
        )
        fx, fy, fz = forward_position(t1, t2, t3, l2, l3)
        assert abs(tx - fx) < 1e-12
        assert abs(ty - fy) < 1e-12
        assert abs(tz - fz) < 1e-12
        rx, ry, rz, rw = reference_ee_orientation(t1, t3)
        assert abs(qx - rx) < 1e-12
        assert abs(qy - ry) < 1e-12
        assert abs(qz - rz) < 1e-12
        assert abs(qw - rw) < 1e-12


def test_reference_orientation_unit_quaternion() -> None:
    """``reference_ee_orientation`` must yield a unit quaternion."""
    for t1, t3 in [(0.0, 0.0), (0.7, -0.2), (2.1, 1.5)]:
        qx, qy, qz, qw = reference_ee_orientation(t1, t3)
        n = math.sqrt(qx * qx + qy * qy + qz * qz + qw * qw)
        assert abs(n - 1.0) < 1e-12


def test_tf_pose_matcher_accepts_exact_analytic_snapshot() -> None:
    """Matcher accepts a pose identical to the closed-form RTR solution."""
    t1, t2, t3, l2, l3 = 0.2, 0.5, 0.35, 0.9, 1.0
    pose = rtr_end_effector_transform(t1, t2, t3, l2, l3)
    tx, ty, tz, qx, qy, qz, qw = pose
    assert tf_pose_matches_rtr_analytical(
        tx, ty, tz, qx, qy, qz, qw, t1, t2, t3, l2, l3,
    )


def test_tf_pose_matcher_rejects_shifted_translation() -> None:
    """Matcher rejects a translation biased away from analytic position."""
    t1, t2, t3, l2, l3 = 0.2, 0.5, 0.35, 0.9, 1.0
    pose = rtr_end_effector_transform(t1, t2, t3, l2, l3)
    tx, ty, tz, qx, qy, qz, qw = pose
    assert not tf_pose_matches_rtr_analytical(
        tx + 0.01,
        ty,
        tz,
        qx,
        qy,
        qz,
        qw,
        t1,
        t2,
        t3,
        l2,
        l3,
        pos_tol=1e-4,
    )


def test_parse_rtr_configuration_defaults() -> None:
    """Three joint arguments pick default link lengths."""
    out = parse_rtr_configuration(['ignored', '0.1', '0.2', '0.3'])
    assert out == (0.1, 0.2, 0.3, 0.9, 1.0)


def test_parse_rtr_configuration_custom_lengths() -> None:
    """Optional ``l2`` and ``l3`` override defaults."""
    out = parse_rtr_configuration(['ignored', '0', '0', '0', '0.5', '0.6'])
    assert out == (0.0, 0.0, 0.0, 0.5, 0.6)
