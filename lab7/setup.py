import os
from glob import glob

from setuptools import find_packages, setup

package_name = "lab7"

setup(
    name=package_name,
    version="0.0.1",
    packages=find_packages(exclude=["tests"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*launch*.py")),
        (os.path.join("share", package_name, "urdf"), glob("urdf/*.xacro")),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
        (os.path.join("share", package_name, "rviz"), glob("rviz/*.rviz")),
        (os.path.join("share", package_name, "docs", "images"), glob("docs/images/*")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Instructor",
    maintainer_email="instructor@lpnu.ua",
    description="Lab 7: TF2 and URDF for RTR manipulator",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "tf2_broadcaster_demo = lab7.tf2_broadcaster_demo:main",
            "tf2_listener_demo = lab7.tf2_listener_demo:main",
        ],
    },
)
