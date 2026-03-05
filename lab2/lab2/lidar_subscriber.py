#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class LidarSubscriber(Node):
    def __init__(self):
        super().__init__('lidar_subscriber')
        
        # TODO: Create subscriber for /lidar topic
        # Hint: self.create_subscription(MessageType, 'topic', callback, queue_size)
        self.subscription = self.create_subscription(
            LaserScan,
            '/lidar',
            self.lidar_callback,
            10
        )
        
        self.get_logger().info('LiDAR Subscriber started - listening to /lidar')

    def lidar_callback(self, msg):
        """Called automatically whenever a new LiDAR message arrives"""
        
        # TODO: Process the LiDAR data
        # msg.ranges is a list of distances (in meters)
        # msg.range_min and msg.range_max define valid range
        
        # Filter out invalid readings (too close or too far)
        valid_ranges = [
            r for r in msg.ranges 
            if msg.range_min < r < msg.range_max
        ]
        
        if valid_ranges:
            # TODO: Calculate statistics
            min_distance = min(valid_ranges)
            max_distance = max(valid_ranges)
            avg_distance = sum(valid_ranges) / len(valid_ranges)
            
            self.get_logger().info(
                f'LiDAR: min={min_distance:.2f}m, '
                f'max={max_distance:.2f}m, '
                f'avg={avg_distance:.2f}m, '
                f'points={len(valid_ranges)}/{len(msg.ranges)}'
            )
            
            # TODO: Add obstacle detection
            # Warn if obstacle is very close
            if min_distance < 1.0:
                self.get_logger().warn(
                    f'Obstacle detected at {min_distance:.2f}m!'
                )
        else:
            self.get_logger().info('No valid LiDAR data')


def main(args=None):
    rclpy.init(args=args)
    node = LidarSubscriber()
    
    try:
        rclpy.spin(node)  # Keep node running
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()