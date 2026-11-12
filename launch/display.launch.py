"""RViz display of ADORA NANO (no simulator).

    ros2 launch adora_nano_description display.launch.py
    ros2 launch adora_nano_description display.launch.py fixed_base:=true
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    share = get_package_share_directory("adora_nano_description")
    xacro_file = os.path.join(share, "urdf", "adora_nano.urdf.xacro")
    rviz_file = os.path.join(share, "config", "rviz", "display.rviz")

    prefix = LaunchConfiguration("prefix")
    use_sim = LaunchConfiguration("use_sim")
    fixed_base = LaunchConfiguration("fixed_base")

    return LaunchDescription([
        DeclareLaunchArgument("prefix", default_value=""),
        DeclareLaunchArgument("use_sim", default_value="false"),
        DeclareLaunchArgument("fixed_base", default_value="false"),
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            output="screen",
            parameters=[{
                "robot_description": ParameterValue(
                    Command(["xacro ", xacro_file,
                             " prefix:=", prefix,
                             " use_sim:=", use_sim,
                             " fixed_base:=", fixed_base]),
                    value_type=str),
            }],
        ),
        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            output="screen",
        ),
        Node(package="rviz2", executable="rviz2", output="screen",
             arguments=["-d", rviz_file]),
    ])
