import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
# from launch.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import ExecuteProcess

from launch_ros.actions import Node


def generate_launch_description():
    model = os.path.join(get_package_share_directory(
    'object_detection_visual'), 'models', 'wheeled_robot.sdf')

    rviz = Node(
       package='rviz2',
       executable='rviz2',
       arguments=['wheeled_robot.rviz']
    )

    tf2 = Node(
      package = 'tf2_ros',
      executable = 'static_transform_publisher', 
      arguments=['0', '0', '0', '0', '0', '0', 'map', 'base_link']
      )

    gz = ExecuteProcess(
            cmd=['gz','sim', '-r', model],
            output='screen')

    object_detection_visual_node = Node(
       package='object_detection_visual',
       executable='object_detection_visual')

    return LaunchDescription([
        gz,
        tf2,
        rviz,
        object_detection_visual_node
        
    ])
