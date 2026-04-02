# Lab 5: Obstacle Avoidance

**Replicate and understand the obstacle avoidance approach from the tutorial.**

- [Potential Fields – Lecture](https://www.youtube.com/watch?v=FT5DQ-SGYL4)
- [Obstacle Avoidance – Lecture](https://www.youtube.com/watch?v=NkhlJlSBKHU)
- [Path Planning Using Potential Field Algorithm](https://medium.com/@rymshasiddiqui/path-planning-using-potential-field-algorithm-a30ad12bdb08)

---

## Learning Goals

- Implement obstacle avoidance for TurtleBot3
- Use lidar (`/scan`) and odometry (`/odom`) to navigate to a goal
- Publish velocity commands (`/cmd_vel`)

---

## Setup

```bash
cd /opt/ws
colcon build --packages-select lab3 lab5
source install/setup.bash
```

---

## Task

### 1. Add obstacles to the room

Edit `lab3/turtlebot3/worlds/room.sdf`. Add obstacles (boxes, cylinders, walls) so the robot has something to avoid. See [SDF](https://gazebosim.org/docs/latest/sdf.html) for model syntax. Example: a few cylinders as pillars, or walls with gaps as a maze.

### 2. Implement obstacle avoidance

Edit `lab5/obstacle_avoidance.py`:

- Subscribe to `/scan` (LaserScan) — obstacle distances
- Subscribe to `/odom` (Odometry) — robot pose
- Publish to `/cmd_vel` (Twist or TwistStamped) — velocity commands

Drive the robot from start (0, 0) toward a goal (e.g. 3, 3) while avoiding obstacles. The node runs continuously until the goal is reached or you stop it.

### 3. Launch and test

```bash
ros2 launch lab5 obstacle_avoidance_bringup.launch.py
```

TurtleBot3 spawns at (0, 0) in the room. Your node should drive it toward the goal without colliding.

### 4. Tune parameters

Use `goal_x`, `goal_y` and your algorithm parameters. Example:

```bash
ros2 run lab5 obstacle_avoidance --ros-args -p goal_x:=2.0 -p goal_y:=-2.0
```

---

## Deliverables

1. **Implemented** `obstacle_avoidance.py` together with any additioanl logic (potential fields or chosen algorithm)
2. **Screenshots** of the robot reaching the goal while avoiding obstacles
3. **Brief description** of your algorithm, parameters, and any issues
