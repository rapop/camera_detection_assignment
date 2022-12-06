# camera_detection_assignment

Bounding box object detection in ROS2 and Gazebo from the [Bounding Box Camera Sensor plugin](https://github.com/AmrElsersy/ign-sensors/blob/BoundingBox/tutorials/04_boundingbox_camera.md).

![](miscellaneous/object_detection_far.gif)
![](miscellaneous/object_detection_near.gif)

## Prerequisites
Developed and tested in an Ubuntu 20.04 environment.
- Install [ros2-rolling](https://docs.ros.org/en/rolling/Installation.html).
- Install [Gazebo garden](https://gazebosim.org/docs/garden/getstarted).
- Other ros package might be required.

## Run instructions
- Build the ROS work space (see ROS tutorials).
- Run the launch file.
	- `ros2 launch object_detection_visual object_detection_visual.launch.py`