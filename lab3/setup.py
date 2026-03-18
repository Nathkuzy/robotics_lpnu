from setuptools import setup, find_packages
import os
from glob import glob

package_name = 'lab3'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
         glob(os.path.join('launch', '*launch.[pxy]*'))),
        (os.path.join('share', package_name, 'rviz'),
         glob(os.path.join('rviz', '*.rviz'))),
        (os.path.join('share', package_name, 'turtlebot3', 'worlds'),
         glob(os.path.join('turtlebot3', 'worlds', '*.sdf'))),
        (os.path.join('share', package_name, 'turtlebot3', 'urdf'),
         glob(os.path.join('turtlebot3', 'urdf', '*.md'))),
        (os.path.join('share', package_name, 'turtlebot3', 'xacro'),
         glob(os.path.join('turtlebot3', 'xacro', '*.xacro'))),
        (os.path.join('share', package_name, 'turtlebot3'),
         glob(os.path.join('turtlebot3', 'README.md'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Instructor',
    maintainer_email='instructor@lpnu.ua',
    description='Lab 3: Moving Mobile Robots in Simulation',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'velocity_publisher = lab3.velocity_publisher:main',
            'odom_path_publisher = lab3.odom_path_publisher:main',
            'square_path = lab3.square_path:main',
            'circle_path = lab3.circle_path:main',
            'figure_8_path = lab3.figure_8_path:main',
        ],
    },
)
