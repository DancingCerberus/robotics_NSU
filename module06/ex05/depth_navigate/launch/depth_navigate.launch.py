import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node
from launch.actions import TimerAction


def generate_launch_description():
    pkg_desk_share = FindPackageShare(package='depth_navigate').find('depth_navigate')
    pkg_gz_share = FindPackageShare(package='ros_gz_sim').find('ros_gz_sim')

    xacro_file_path = os.path.join(pkg_desk_share, 'urdf/robot.urdf.xacro')
    robot_desc = ParameterValue(Command(['xacro ', xacro_file_path]), value_type=str)

    bridge_config_path = os.path.join(pkg_desk_share, 'config/robot_bridge.yaml')
    world_config_path = os.path.join(pkg_desk_share, 'config/world.sdf')
    # rviz_config_path = os.path.join(pkg_desk_share, 'rviz/robot.rviz')
    rviz_config_path = os.path.join(pkg_desk_share, 'rviz/temp.rviz')

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gz_share, "launch", "gz_sim.launch.py")),
        # launch_arguments={"gz_args": "-r gpu_lidar_sensor.sdf"}.items(),
        launch_arguments={"gz_args": "-r empty.sdf"}.items(),
        # launch_arguments={"gz_args": world_config_path}.items(),
    )

    create = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-name', 'robot',
                   '-topic', 'robot_description',
                   '-x', '0.0',
                   '-y', '0.0',
                   '-z', '0.1',
                ],
        output='screen',
    )

    tf2 = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_transform_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'robot/odom', 'robot/chassis'],
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[
            {'robot_description': robot_desc},
            {'frame_prefix': "robot/"}
        ]
    )

    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'robot_description': ParameterValue(Command(['xacro ', xacro_file_path]), value_type=str)}],
    )

    joint_state_publisher_gui = Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
    )

    rviz = Node(
       package='rviz2',
       executable='rviz2',
       arguments=['-d', rviz_config_path]
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': os.path.join(pkg_desk_share, 'config', 'robot_bridge.yaml'),
            'qos_overrides./tf_static.publisher.durability': 'transient_local',
        }],
        output='screen'
    )

    move = Node(
        package='depth_navigate',
        executable='depth_navigate',
        name='depth_navigate',
        parameters=[
        ]
    )

    return LaunchDescription([
        tf2,
        robot_state_publisher,
        # joint_state_publisher,
        rviz,
        gz_sim,
        bridge,
        TimerAction(
            period=5.0,
            actions=[create]),
        move
    ])
