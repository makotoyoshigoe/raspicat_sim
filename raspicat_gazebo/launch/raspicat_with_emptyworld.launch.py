# Copyright 2023 RT Corporation
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

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    this_launch_dir = os.path.join(
        get_package_share_directory('raspicat_gazebo'), 'launch')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    raspicat_bringup_launch_dir = os.path.join(
        get_package_share_directory('raspicat_bringup'), 'launch')

    gui = LaunchConfiguration('gui', default='true')
    world = LaunchConfiguration('world')
    x_pose = LaunchConfiguration('x_pose', default='0.0')
    y_pose = LaunchConfiguration('y_pose', default='0.0')
    yaw_pose = LaunchConfiguration('yaw_pose', default='0.0')

    declare_verbose = DeclareLaunchArgument(
        'verbose', default_value='false',
        description='Set "true" to increase messages written to terminal'
    )
    declare_world = DeclareLaunchArgument(
        'gui', default_value='true',
        description='Set to "false" to run headless.'
    )
    declare_world = DeclareLaunchArgument(
        'world', default_value=os.path.join(
            get_package_share_directory('raspicat_gazebo'),
            'worlds',
            'empty.world'),
        description='world configuration file path'
    )
    # declare_x_position = DeclareLaunchArgument(
    #     'x_pose', default_value='0.0',
    #     description='x position of robot')
    # declare_y_position = DeclareLaunchArgument(
    #     'y_pose', default_value='0.0',
    #     description='y position of robot')
    # declare_yaw_position = DeclareLaunchArgument(
    #     'yaw_pose', default_value='0.0',
    #     description='yaw position of robot')

    gzserver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world}.items()
    )

    gzclient = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        ),
        condition=IfCondition(gui)
    )

    robot_state_publisher = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(raspicat_bringup_launch_dir,
                         'robot_state_publisher.launch.py')
        ),
        launch_arguments={
            'use_joint_state_publisher': 'False'}.items()
    )

    spawn_raspicat = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(this_launch_dir, 'spawn_raspicat.launch.py')
        ),
        launch_arguments={
            'x_pose': x_pose,
            'y_pose': y_pose, 
            'yaw_pose': yaw_pose
        }.items()
    )

    raspicat_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(this_launch_dir, 'raspicat_simulation.launch.py')
        )
    )

    ld = LaunchDescription()

    ld.add_action(declare_verbose)
    ld.add_action(declare_world)
    # ld.add_action(declare_x_position)
    # ld.add_action(declare_y_position)
    # ld.add_action(declare_yaw_position)

    ld.add_action(gzserver)
    ld.add_action(gzclient)
    ld.add_action(robot_state_publisher)
    ld.add_action(spawn_raspicat)
    ld.add_action(raspicat_sim)

    return ld
