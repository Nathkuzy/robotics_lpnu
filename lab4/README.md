# Lab 4: Dead Reckoning

## Learning Goals

- Integrate velocity commands to estimate pose (dead reckoning)
- Compare with Gazebo ground truth
- Understand drift

**Reference:** [Motion Model for Differential Drive](https://www.roboticsbook.org/S52_diffdrive_actions.html)

---

## Setup

```bash
cd /opt/ws
colcon build --packages-select lab3 lab4
source install/setup.bash
```

---

## Task

### 1. Implement dead reckoning

Edit `lab4/dead_reckoning.py` — implement the TODO. Use the reference above for the pose update from `(v, ω)`.

### 2. Launch TurtleBot3

**Terminal 1:**
```bash
ros2 launch lab4 dead_reckoning_bringup.launch.py
```

### 3. Run circle trajectory

**Terminal 2:**
```bash
ros2 run lab3 circle_path
```

### 4. Observe

RViz shows two paths: odom (ground truth) and dead reckoning. Terminal logs error.

---

## Deliverables

1. Implemented `dead_reckoning.py`
2. Screenshot of both paths in RViz
3. Brief answer: Why does dead reckoning drift?
