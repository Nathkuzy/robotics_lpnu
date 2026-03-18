"""Launch TurtleBot3 in room world (8x8m with walls)."""
import os
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable, IncludeLaunchDescription, AppendEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    lab3_share = get_package_share_directory('lab3')
    turtlebot3_gazebo_share = get_package_share_directory('turtlebot3_gazebo')
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')

    world = os.path.join(lab3_share, 'turtlebot3', 'worlds', 'room.sdf')

    gzserver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': ['-r -s -v2 ', world], 'on_exit_shutdown': 'true'}.items()
    )

    gzclient = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-g -v2 '}.items()
    )

    robot_state_publisher = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(turtlebot3_gazebo_share, 'launch', 'robot_state_publisher.launch.py')
        ),
        launch_arguments={'use_sim_time': 'true'}.items()
    )

    spawn_turtlebot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(turtlebot3_gazebo_share, 'launch', 'spawn_turtlebot3.launch.py')
        ),
        launch_arguments={'x_pose': '0.0', 'y_pose': '0.0'}.items()
    )

    return LaunchDescription([
        SetEnvironmentVariable(name='TURTLEBOT3_MODEL', value='burger'),
        AppendEnvironmentVariable(
            name='GZ_SIM_RESOURCE_PATH',
            value=os.path.join(turtlebot3_gazebo_share, 'models')
        ),
        gzserver,
        gzclient,
        spawn_turtlebot,
        robot_state_publisher,
    ])
