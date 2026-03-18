"""Launch Gazebo, bridges, odom_path_publisher, and optionally RViz2."""
import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory


def launch_setup(context):
    robot_world = '/opt/ws/src/code/lab3/worlds/robot.sdf'
    pkg_share = get_package_share_directory('lab3')
    rviz_config = os.path.join(pkg_share, 'rviz', 'trajectory.rviz')
    use_rviz = LaunchConfiguration('rviz', default='true').perform(context) == 'true'

    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', robot_world],
        output='screen'
    )

    bridge_cmd_vel = ExecuteProcess(
        cmd=['ros2', 'run', 'ros_gz_bridge', 'parameter_bridge',
             '/cmd_vel@geometry_msgs/msg/TwistStamped@gz.msgs.Twist'],
        output='screen'
    )

    bridge_odom = ExecuteProcess(
        cmd=['ros2', 'run', 'ros_gz_bridge', 'parameter_bridge',
             '/model/vehicle_blue/odometry@nav_msgs/msg/Odometry@gz.msgs.Odometry'],
        output='screen'
    )

    odom_path = ExecuteProcess(
        cmd=['ros2', 'run', 'lab3', 'odom_path_publisher'],
        output='screen'
    )

    actions = [gazebo, bridge_cmd_vel, bridge_odom, odom_path]
    if use_rviz:
        rviz = ExecuteProcess(
            cmd=['rviz2', '-d', rviz_config],
            output='screen'
        )
        actions.append(rviz)

    return actions


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('rviz', default_value='true', description='Launch RViz2'),
        OpaqueFunction(function=launch_setup),
    ])
