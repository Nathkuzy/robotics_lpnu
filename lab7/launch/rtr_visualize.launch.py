"""Visualize the RTR URDF with interactive joint sliders and RViz2."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import TimerAction
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    pkg = FindPackageShare("lab7")
    urdf_path = PathJoinSubstitution([pkg, "urdf", "rtr_manipulator.xacro"])
    robot_description = ParameterValue(Command(["xacro ", urdf_path]), value_type=str)

    rsp = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description}],
    )

    jsp_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        output="screen",
        parameters=[{"robot_description": robot_description}],
    )

    rviz_cfg = os.path.join(get_package_share_directory("lab7"), "rviz", "rtr.rviz")
    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", rviz_cfg],
        output="screen",
    )

    return LaunchDescription(
        [
            rsp,
            jsp_gui,
            TimerAction(period=1.0, actions=[rviz]),
        ]
    )
