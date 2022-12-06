import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import ExecuteProcess

from launch_ros.actions import Node


def generate_launch_description():

    world = os.path.join(get_package_share_directory(
    'object_detection_visual'), 'models', 'world.sdf')

    robot = os.path.join(get_package_share_directory(
    'object_detection_visual'), 'models', 'wheeled_robot.urdf')

    rviz = Node(
       package='rviz2',
       executable='rviz2',
       arguments=['wheeled_robot.rviz']
    )

    robot_state_publisher = Node(
       package='robot_state_publisher',
       executable='robot_state_publisher',
       arguments=[robot]
    )

    tf = Node(
      package = 'tf2_ros',
      executable = 'static_transform_publisher', 
      arguments=['0', '0', '0', '-1.5708', '0', '1.5708', 'camera', 'kitti_camera'] #yaw pitch roll 
      )

    tf2 = Node(
      package = 'tf2_ros',
      executable = 'static_transform_publisher', 
      arguments=['0', '0', '0', '0', '0', '0', 'wheeled_robot', 'chassis']
      )

    gz = ExecuteProcess(
            cmd=['gz','sim', '-r', world],
            output='screen')

    spawn_robot = ExecuteProcess(
            cmd=['gz','service', '-s', '/world/Moving_robot/create', '--reqtype', 'gz.msgs.EntityFactory', '--reptype', 'gz.msgs.Boolean',
            '--timeout', '1', '-r', 'sdf_filename: "'+ robot + '"' + "pose: {position: {x:-3.5 y:0 z:0.4}}"],
            output='screen')


    object_detection_visual_node = Node(
       package='object_detection_visual',
       executable='object_detection_visual')

    spawn_robot_delay = TimerAction(
            period=3.0,
            actions=[spawn_robot])

    wheeled_robot_tf_broadcaster_node = Node(
       package='wheeled_robot_tf_broadcaster',
       executable='wheeled_robot_tf_broadcaster')

    return LaunchDescription([
        robot_state_publisher,
        gz,
        spawn_robot_delay,
        tf2,
        tf,
        rviz,
        object_detection_visual_node,
        wheeled_robot_tf_broadcaster_node
        
    ])
