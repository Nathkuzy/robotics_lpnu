"""Launch Gazebo with 4-wheel mobile robot."""
from launch import LaunchDescription
from launch.actions import ExecuteProcess


def generate_launch_description():
    robot_world = '/opt/ws/src/code/lab3/worlds/robot.sdf'

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

    return LaunchDescription([
        gazebo,
        bridge_cmd_vel,
        bridge_odom,
    ])
