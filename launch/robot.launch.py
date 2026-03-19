import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    # File paths
    urdf_file_path = '/home/kunal-humble/ros2_ws/src/diff_robot/urdf/diff_robot.urdf'
    rviz_config_file_path = '/home/kunal-humble/ros2_ws/src/diff_robot/urdf/rviz.rviz'
    world_file_path = '/home/kunal-humble/ros2_ws/src/diff_robot/world/maze.world'
    map_file = '/home/kunal-humble/ros2_ws/src/diff_robot/map/map.yaml'

    # Load robot description
    with open(urdf_file_path, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([

        # Launch arguments
        DeclareLaunchArgument(
            name='model',
            default_value=urdf_file_path
        ),

        DeclareLaunchArgument(
            name='rvizconfig',
            default_value=rviz_config_file_path
        ),

        DeclareLaunchArgument(
            name='world',
            default_value=world_file_path
        ),

        DeclareLaunchArgument(name='x', default_value='0.0'),
        DeclareLaunchArgument(name='y', default_value='0.0'),
        DeclareLaunchArgument(name='z', default_value='0.15'),

        # Gazebo
        ExecuteProcess(
            cmd=[
                'gazebo',
                '--verbose',
                '-s',
                'libgazebo_ros_factory.so',
                LaunchConfiguration('world')
            ],
            output='screen'
        ),

        # Spawn robot
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-file', LaunchConfiguration('model'),
                '-entity', 'diff_robot',
                '-x', LaunchConfiguration('x'),
                '-y', LaunchConfiguration('y'),
                '-z', LaunchConfiguration('z')
            ],
            output='screen'
        ),

        # Robot state publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[
                {'robot_description': robot_desc},
                {'use_sim_time': True}
            ]
        ),

        # Map Server
        # Node(
        #     package='nav2_map_server',
        #     executable='map_server',
        #     name='map_server',
        #     output='screen',
        #     parameters=[
        #         {'yaml_filename': map_file},
        #         {'use_sim_time': True}
        #     ]
        # ),

        # # AMCL
        # Node(
        #     package='nav2_amcl',
        #     executable='amcl',
        #     name='amcl',
        #     output='screen',
        #     parameters=[
        #         {'use_sim_time': True}
        #     ]
        # ),

        # # Lifecycle Manager (VERY IMPORTANT)
        # Node(
        #     package='nav2_lifecycle_manager',
        #     executable='lifecycle_manager',
        #     name='lifecycle_manager_localization',
        #     output='screen',
        #     parameters=[{
        #         'use_sim_time': True,
        #         'autostart': True,
        #         'node_names': ['map_server', 'amcl']
        #     }]
        # ),

        # RViz

        Node( package='slam_toolbox', executable='async_slam_toolbox_node', name='slam_toolbox', output='screen', parameters=[ '/home/kunal-humble/ros2_ws/src/diff_robot/map/slam_params.yaml', {'use_sim_time': True} ] ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', LaunchConfiguration('rvizconfig')],
            output='screen'
        ),

    ])