"""RTR model with ros2_control mock hardware, joint_state_broadcaster, and forward commands.

Command positions (rad for revolute joints, meters for prismatic ``joint_theta2``), e.g.:

  ros2 topic pub --once /forward_position_controller/commands std_msgs/msg/Float64MultiArray \\
    "{data: [0.2, 0.6, 0.4]}"
"""

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

    controllers = os.path.join(get_package_share_directory("lab7"), "config", "rtr_controllers.yaml")

    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            {"robot_description": robot_description},
            controllers,
        ],
        output="screen",
    )

    rsp = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description}],
    )

    jsb_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
        output="screen",
    )

    fwd_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["forward_position_controller", "--controller-manager", "/controller_manager"],
        output="screen",
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
            control_node,
            rsp,
            TimerAction(period=3.0, actions=[jsb_spawner, fwd_spawner]),
            TimerAction(period=4.0, actions=[rviz]),
        ]
    )
