import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    pkg_path = get_package_share_directory('diff_robot')

    urdf_file_path = os.path.join(pkg_path, 'urdf', 'diff_robot.urdf')
    rviz_config_file_path = os.path.join(pkg_path, 'urdf', 'rviz.rviz')
    world_file_path = os.path.join(pkg_path, 'world', 'maze.world')
    params_file = os.path.join(pkg_path, 'map', 'nav2_params.yaml')

    with open(urdf_file_path, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([

        DeclareLaunchArgument('model', default_value=urdf_file_path),
        DeclareLaunchArgument('rvizconfig', default_value=rviz_config_file_path),
        DeclareLaunchArgument('world', default_value=world_file_path),

        DeclareLaunchArgument('x', default_value='0.0'),
        DeclareLaunchArgument('y', default_value='0.0'),
        DeclareLaunchArgument('z', default_value='0.15'),

        # Gazebo
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory('gazebo_ros'),
                    'launch',
                    'gazebo.launch.py'
                )
            ),
            launch_arguments={
                'world': LaunchConfiguration('world')
            }.items(),
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
            output='screen',
            parameters=[
                {'robot_description': robot_desc},
                {'use_sim_time': True}
            ]
        ),

        # ---------------- LOCALIZATION ---------------- #

        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[{
                'yaml_filename': '/home/kunal-humble/ros2_ws/src/diff_robot/map/map.yaml',
                'use_sim_time': True
            }]
        ),

        Node(
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[params_file]
        ),

        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_localization',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'autostart': True,
                'node_names': ['map_server', 'amcl']
            }]
        ),

        # ---------------- NAVIGATION ---------------- #

        Node(
            package='nav2_controller',
            executable='controller_server',
            name='controller_server',
            output='screen',
            parameters=[params_file]
        ),

        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            output='screen',
            parameters=[params_file]
        ),

        Node(
            package='nav2_behaviors',
            executable='behavior_server',
            name='behavior_server',
            output='screen',
            parameters=[params_file]
        ),

        Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            output='screen',
            parameters=[params_file]
        ),

        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_navigation',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'autostart': True,
                'node_names': [
                    'controller_server',
                    'planner_server',
                    'behavior_server',
                    'bt_navigator'
                ]
            }]
        ),

        # RViz
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', LaunchConfiguration('rvizconfig')],
            output='screen'
        ),
    ])