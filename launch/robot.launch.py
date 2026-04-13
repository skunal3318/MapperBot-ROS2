import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    pkg_path = get_package_share_directory('diff_robot')

    urdf_file_path = os.path.join(pkg_path, 'urdf', 'diff_robot.urdf')
    rviz_config_file_path = os.path.join(pkg_path, 'urdf', 'rviz.rviz')
    world_file_path = os.path.join(pkg_path, 'world', 'maze.world')

    
    with open(urdf_file_path, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([

       
        DeclareLaunchArgument('model', default_value=urdf_file_path),
        DeclareLaunchArgument('rvizconfig', default_value=rviz_config_file_path),
        DeclareLaunchArgument('world', default_value=world_file_path),

        DeclareLaunchArgument('x', default_value='0.0'),
        DeclareLaunchArgument('y', default_value='0.0'),
        DeclareLaunchArgument('z', default_value='0.15'),

        
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

    
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[
                {'robot_description': robot_desc},
                {'use_sim_time': True}
            ]
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', LaunchConfiguration('rvizconfig')],
            output='screen'
        ),

    ])