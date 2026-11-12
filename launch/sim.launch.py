"""ADORA NANO for an external physics simulator (Gazebo / MuJoCo / Isaac / webots).

This launch only publishes the description + joint states and a TF tree; the
simulator itself is a separate, site-specific package:

  * Gazebo (gz sim / ros_gz): spawn `urdf/adora_nano.urdf` into the world, then
      ros2 launch adora_nano_description sim.launch.py use_sim_time:=true
  * MuJoCo: `mujoco` does not consume xacro; load the PLAIN urdf:
        python -m mujoco.viewer --mjcf=<pkg>/urdf/adora_nano.urdf
      (or the convenience copy work/urdf/adora_nano.urdf)
  * PyBullet:  p.loadURDF("<pkg>/urdf/adora_nano.urdf", useFixedBase=True)
  * Isaac Sim: import urdf/adora_nano.urdf, set articulation root = base_link

Run with:
    ros2 launch adora_nano_description sim.launch.py
    ros2 launch adora_nano_description sim.launch.py use_sim_time:=true fixed_base:=true
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

    use_sim_time = LaunchConfiguration("use_sim_time")
    fixed_base = LaunchConfiguration("fixed_base")

    return LaunchDescription([
        DeclareLaunchArgument("use_sim_time", default_value="false"),
        DeclareLaunchArgument("fixed_base", default_value="true"),
        DeclareLaunchArgument("prefix", default_value=""),
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            output="screen",
            parameters=[{
                "use_sim_time": ParameterValue(use_sim_time, value_type=bool),
                "robot_description": ParameterValue(
                    Command(["xacro ", xacro_file,
                             " prefix:=", LaunchConfiguration("prefix"),
                             " use_sim:=true",
                             " fixed_base:=", fixed_base]),
                    value_type=str),
            }],
        ),
        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            output="screen",
            parameters=[{"use_sim_time": ParameterValue(use_sim_time, value_type=bool)}],
        ),
    ])
