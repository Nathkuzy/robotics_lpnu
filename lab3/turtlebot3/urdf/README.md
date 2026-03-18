# TurtleBot3 URDF

TurtleBot3 robot description is in the `turtlebot3_description` package.

**Links:** [URDF tutorial](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/URDF-Main.html) · [Xacro](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/Using-Xacro-to-Clean-Up-a-URDF-File.html)

**Location:**
```bash
$(ros2 pkg prefix turtlebot3_description)/share/turtlebot3_description/urdf/
```

**Key files:** `turtlebot3_burger.urdf.xacro`, `turtlebot3_common.urdf.xacro`, `turtlebot3_burger.gazebo.xacro`

**Inspect in RViz:** Launch TurtleBot3, then `ros2 run rviz2 rviz2` — add RobotModel, set Fixed Frame to `base_footprint`.
