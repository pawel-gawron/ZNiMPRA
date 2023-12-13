# Copyright 2023 Amadeusz Szymko
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.actions import OpaqueFunction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def launch_setup(context, *args, **kwargs):
    pkg_prefix = FindPackageShare('cartographer_demo')

    config_dir = PathJoinSubstitution(pkg_prefix, 'config').perform(context)

    cartographer_node = Node(
        package='cartographer_node',
        executable='cartographer_node_exe',
        name='cartographer_node',
        parameters=[
            {'use_sim_time': True}
        ],
        output='screen',
        remappings=[
                ("imu", "/sensing/imu_corrector/imu"),
                ("odom", "/localization/kinematic_state"),
                ("scan", "/sensing/lidar/scan")
                ],
        arguments=['--ros-args', '--log-level', 'info', '--enable-stdout-logs',
        '--configuration_directory', config_dir,
        '--configuration_basename', 'mapping.lua'],
    )

    cartographer_occupancy_grid_node = Node(
        package='cartographer_occupancy_grid_node',
        executable='cartographer_occupancy_grid_node_exe',
        name='cartographer_occupancy_grid_node',
        parameters=[
            {'use_sim_time': True},
            {'use_sim_time': True},
            {'resolution': 0.05}
        ],
        output='screen',
        arguments=['--ros-args', '--log-level', 'info', '--enable-stdout-logs'],
    )
    return [
        cartographer_node,
        cartographer_occupancy_grid_node
    ]


def generate_launch_description():
    declared_arguments = []

    def add_launch_arg(name: str, default_value: str = None):
        declared_arguments.append(
            DeclareLaunchArgument(name, default_value=default_value)
        )
    # Tools
    add_launch_arg('rviz', 'true')
    add_launch_arg('rviz_config', 'cartographer.rviz')
    # Localization
    # TODO: add args

    return LaunchDescription([
        *declared_arguments,
        OpaqueFunction(function=launch_setup)
    ])