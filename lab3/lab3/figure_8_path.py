"""Figure-8 path - STUDENT TASK.

You have square_path.py and circle_path.py as base.
Implement a figure-8: two circles, first turning left, then turning right.

Hint: A figure-8 = circle left + circle right. Use the same timed motion
as circle_path (linear.x + angular.z for duration = 2*pi/|w|).
"""
import rclpy
from rclpy.node import Node


class Figure8Path(Node):
    def __init__(self):
        super().__init__('figure_8_path')

        self.get_logger().info("Figure-8 path - TODO: implement using circle_path logic")
        self.get_logger().info("Hint: run circle left (w>0), then circle right (w<0)")
        self.destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = Figure8Path()
    rclpy.shutdown()
