import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    radius_arg = DeclareLaunchArgument(
        'radius',
        default_value='3.0'
    )

    rotate_direct = DeclareLaunchArgument(
        'direction_of_rotation',
        default_value='-1'
    )

    demo_nodes = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('turtle_tf2_carrot'), 'launch'),
            '/turtle_tf2_demo.launch.py']),
        launch_arguments={'target_frame': 'carrot1'}.items(),
    )

    dynamic_broadcaster_node = Node(
        package='turtle_tf2_carrot',
        executable='dynamic_frame_tf2_broadcaster',
        name='dynamic_broadcaster',
        parameters=[
            {'radius': LaunchConfiguration('radius')},
            {'direction_of_rotation': LaunchConfiguration('direction_of_rotation')}
        ]
    )

    return LaunchDescription([
        radius_arg,
        rotate_direct,
        demo_nodes,
        dynamic_broadcaster_node,
    ])
