"""Launch TurtleBot3 + odom path + dead reckoning. Run circle_path in another terminal."""
import os
from launch import LaunchDescription
from launch.actions import (
    SetEnvironmentVariable,
    IncludeLaunchDescription,
    ExecuteProcess,
    DeclareLaunchArgument,
    OpaqueFunction,
    AppendEnvironmentVariable,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory


def launch_setup(context):
    lab3_share = get_package_share_directory("lab3")
    lab4_share = get_package_share_directory("lab4")
    turtlebot3_gazebo_share = get_package_share_directory("turtlebot3_gazebo")
    ros_gz_sim_share = get_package_share_directory("ros_gz_sim")

    rviz_config = os.path.join(lab4_share, "rviz", "dead_reckoning.rviz")
    use_rviz = LaunchConfiguration("rviz", default="true").perform(context) == "true"

    world = os.path.join(lab3_share, "turtlebot3", "worlds", "room.sdf")

    gzserver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, "launch", "gz_sim.launch.py")
        ),
        launch_arguments={
            "gz_args": ["-r -s -v2 ", world],
            "on_exit_shutdown": "true",
        }.items(),
    )

    gzclient = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, "launch", "gz_sim.launch.py")
        ),
        launch_arguments={"gz_args": "-g -v2 "}.items(),
    )

    robot_state_publisher = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(turtlebot3_gazebo_share, "launch", "robot_state_publisher.launch.py")
        ),
        launch_arguments={"use_sim_time": "true"}.items(),
    )

    spawn_turtlebot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(turtlebot3_gazebo_share, "launch", "spawn_turtlebot3.launch.py")
        ),
        launch_arguments={"x_pose": "0.0", "y_pose": "0.0"}.items(),
    )

    odom_path = ExecuteProcess(
        cmd=[
            "ros2",
            "run",
            "lab3",
            "odom_path_publisher",
            "--ros-args",
            "-p",
            "odom_topic:=/odom",
        ],
        output="screen",
    )

    dead_reckoning = ExecuteProcess(
        cmd=[
            "ros2",
            "run",
            "lab4",
            "dead_reckoning",
            "--ros-args",
            "-p",
            "ground_truth_topic:=/odom",
        ],
        output="screen",
    )

    actions = [
        gzserver,
        gzclient,
        spawn_turtlebot,
        robot_state_publisher,
        odom_path,
        dead_reckoning,
    ]
    if use_rviz:
        rviz = ExecuteProcess(cmd=["rviz2", "-d", rviz_config], output="screen")
        actions.append(rviz)

    return actions


def generate_launch_description():
    turtlebot3_gazebo_share = get_package_share_directory("turtlebot3_gazebo")

    return LaunchDescription([
        SetEnvironmentVariable(name="TURTLEBOT3_MODEL", value="burger"),
        AppendEnvironmentVariable(
            name="GZ_SIM_RESOURCE_PATH",
            value=os.path.join(turtlebot3_gazebo_share, "models"),
        ),
        DeclareLaunchArgument("rviz", default_value="true", description="Launch RViz2"),
        OpaqueFunction(function=launch_setup),
    ])
