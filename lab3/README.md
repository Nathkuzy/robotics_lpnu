# Lab 3: Moving Mobile Robots in Simulation

## Learning Goals

- Differential drive kinematics and velocity commands
- Odometry feedback for path following
- RViz2 trajectory visualization

**Further reading:**
- 

[Calculating Wheel Odometry for a Differential Drive Robot](https://automaticaddison.com/calculating-wheel-odometry-for-a-differential-drive-robot/)

[Wheel Odometry Model for Differential Drive Robotics](https://medium.com/@nahmed3536/wheel-odometry-model-for-differential-drive-robotics-91b85a012299)
- [URDF](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/URDF-Main.html) — robot description (links, joints)
- [Xacro](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/Using-Xacro-to-Clean-Up-a-URDF-File.html) — URDF with macros and properties


---

## Setup
**Copy your `robot.sdf` from previous labs to the `worlds` folder, then:**

**TurtleBot3:** The Dockerfile includes TurtleBot3 packages. After pulling, rebuild it to pick up these changes:
```bash
./scripts/cmd build-docker
```
Or install manually inside the container:
```bash
sudo apt update && sudo apt install -y ros-jazzy-turtlebot3 ros-jazzy-turtlebot3-simulations
```

```bash
cd /opt/ws
colcon build --packages-select lab3
source install/setup.bash
```
---

## Launch

**Custom 4-wheel robot:**
```bash
ros2 launch lab3 bringup.launch.py
```
If the robot gets stuck on obstacles, you may need to push them away manually in the SDF (edit `worlds/robot.sdf`).

**TurtleBot3** (you also need to run this—no creative task here; it will be used in the next lab):
```bash
ros2 launch lab3 turtlebot3_room_bringup.launch.py
```
TurtleBot3 runs in an 8×8 m room with walls. It has a **lidar** ([LaserScan](https://docs.ros.org/en/jazzy/api/sensor_msgs/msg/LaserScan.html) `/scan` topic). Use `/cmd_vel` and `/odom`. Path nodes need `-p odom_topic:=/odom`.

---

## Inspect

- **RViz:** Add displays for Path (`/path`), Odometry, LaserScan (`/scan`). Set Fixed Frame to `odom`. [RViz2](https://docs.ros.org/en/jazzy/How-To-Guides/Using-RViz2.html)
- **Xacro:** See `turtlebot3/xacro/simple_diff_drive.urdf.xacro`—properties, macros, link/joint structure.
- **URDF:** See `turtlebot3/urdf/README.md` for TurtleBot3 description location.
- **Room world:** `turtlebot3/worlds/room.sdf`. [SDF](https://gazebosim.org/docs/latest/sdf.html) — Gazebo world format.

---

## Base Code

**Square** (`square_path.py`): Odometry-based, move forward + turn 90°, repeat 4 times.

**Circle** (`circle_path.py`): Timed motion, constant linear + angular velocity for one full circle.

See [TurtleBot3 README](turtlebot3/README.md) for launch and path commands.

**Velocity publisher** (`velocity_publisher`): Publish constant (v, w), prints wheel speeds from `diff_drive_math`.

**Odom path publisher** (`odom_path_publisher`): Subscribes to odometry, publishes `/path` for RViz2.

---

## Parameters (tune for your robot)

| Parameter | Default | Description |
|-----------|---------|-------------|
| side_length | 2.0 | Square side length (m) |
| linear_speed | 0.4 | Forward speed (m/s) |
| angular_speed | 0.8 | Turn rate (rad/s) |
| odom_topic | /model/vehicle_blue/odometry | Odometry topic (use /odom for TurtleBot3) |

```bash
ros2 run lab3 square_path --ros-args -p side_length:=2.5
ros2 run lab3 square_path --ros-args -p odom_topic:=/odom   # TurtleBot3
```

---

## Tasks

### Task 1: Run square and circle

You must also run the **TurtleBot3** setup (no creative task for it here; it will be used in the next lab). See [TurtleBot3 README](turtlebot3/README.md) for launch and path commands.

```bash
ros2 run lab3 square_path
ros2 run lab3 circle_path
```

### Task 2: Implement figure-8

You have `square_path.py` and `circle_path.py`. Implement `figure_8_path.py`:
- Figure-8 = two circles: first left (w>0), then right (w<0)
- Use the same timed motion as `circle_path` (no odometry needed)
- **Run it on both robots:** 4-wheel (`bringup.launch.py`) and TurtleBot3 (`turtlebot3_room_bringup.launch.py`)


### Task 3: RViz2 visualization

Launch bringup, then run a path. RViz2 shows the trajectory on `/path`.


---

## Deliverables

1. Implemented `figure_8_path.py`
2. Screenshot of trajectory from RViz2
3. Best parameters for square path
4. Brief answers: What is differential drive? Why might the square drift?

---

## Troubleshooting

**RViz shows no path:** Fixed Frame must be `odom`. Add Path display, topic `/path`.

## Code Structure

```
lab3/
├── lab3/
│   ├── diff_drive_math.py
│   ├── velocity_publisher.py
│   ├── odom_path_publisher.py
│   ├── square_path.py
│   ├── circle_path.py
│   └── figure_8_path.py        # Student task
├── launch/
│   ├── gazebo.launch.py
│   ├── bringup.launch.py
│   ├── turtlebot3_room.launch.py
│   └── turtlebot3_room_bringup.launch.py
├── turtlebot3/
│   ├── worlds/room.sdf
│   ├── urdf/README.md
│   ├── xacro/simple_diff_drive.urdf.xacro
│   └── README.md
├── rviz/
│   └── trajectory.rviz
└── worlds/
    └── robot.sdf
```
