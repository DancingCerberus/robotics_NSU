ros2 launch robot_bringup diff_drive_launch.py

*In opened window:*
robot/cmd_vel
___

ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=robot/cmd_vel