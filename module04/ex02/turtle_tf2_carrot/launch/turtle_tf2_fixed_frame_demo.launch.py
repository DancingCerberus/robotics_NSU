import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():
    demo_nodes = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('turtle_tf2_carrot'), 'launch'),
            '/turtle_tf2_demo.launch.py']),
            launch_arguments={'target_frame': 'carrot1'}.items(),
        )

    return LaunchDescription([
        demo_nodes,
        Node(
            package='turtle_tf2_carrot',
            executable='fixed_frame_tf2_broadcaster',
            name='fixed_broadcaster',
        ),
    ])