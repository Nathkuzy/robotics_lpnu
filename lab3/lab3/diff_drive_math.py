"""Differential drive kinematics helpers."""


def twist_to_wheel_speeds(v: float, w: float, wheel_radius: float, wheel_separation: float) -> tuple[float, float]:
    """Convert (v, w) to (left_omega, right_omega) in rad/s."""
    v_left = v - (w * wheel_separation / 2.0)
    v_right = v + (w * wheel_separation / 2.0)
    return (v_left / wheel_radius, v_right / wheel_radius)


def curve_radius(v: float, w: float) -> float:
    """Curve radius in m. Returns inf for straight (w=0)."""
    if abs(w) < 1e-9:
        return float("inf")
    return v / w
