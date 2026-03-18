# TurtleBot3

TurtleBot3 is added for you to use in this lab and future labs (dead reckoning, obstacle avoidance). It has a **lidar** ([LaserScan](https://docs.ros.org/en/jazzy/api/sensor_msgs/msg/LaserScan.html) `/scan` topic).

**Links:** [URDF](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/URDF-Main.html) · [Xacro](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/Using-Xacro-to-Clean-Up-a-URDF-File.html)

## Structure

| Path | Contents |
|------|----------|
| `worlds/room.sdf` | 8×8 m room with walls |
| `urdf/README.md` | Where TurtleBot3 URDF lives (`turtlebot3_description`) |
| `xacro/simple_diff_drive.urdf.xacro` | Minimal xacro example—properties, macros, links, joints |

## Inspect

- **RViz:** Add LaserScan (`/scan`), Path (`/path`), Odometry. Set Fixed Frame to `odom`.
- **Xacro:** Open `simple_diff_drive.urdf.xacro`—see how properties and macros work.
- **URDF:** See `urdf/README.md` for TurtleBot3 description files.

## Launch

```bash
ros2 launch lab3 turtlebot3_room_bringup.launch.py
```

## Path nodes

```bash
ros2 run lab3 square_path --ros-args -p odom_topic:=/odom
ros2 run lab3 circle_path
```
