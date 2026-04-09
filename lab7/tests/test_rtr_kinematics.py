"""Unit tests for RTR forward kinematics (no ROS runtime required)."""

from lab7.rtr_kinematics import forward_position


def test_forward_kinematics_zero_config() -> None:
    """At theta=(0,0,0), horizontal reach is l2+l3 along +x."""
    l2, l3 = 0.9, 1.0
    x, y, z = forward_position(0.0, 0.0, 0.0, l2=l2, l3=l3)
    assert abs(x - (l2 + l3)) < 1e-9
    assert abs(y) < 1e-9
    assert abs(z) < 1e-9


def test_forward_kinematics_bent_elbow() -> None:
    """theta3 = pi/2: x = l2, z = l3 + theta2."""
    l2, l3 = 0.9, 1.0
    import math

    x, y, z = forward_position(0.0, 0.3, math.pi / 2, l2=l2, l3=l3)
    assert abs(x - l2) < 1e-9
    assert abs(y) < 1e-9
    assert abs(z - (l3 + 0.3)) < 1e-9
