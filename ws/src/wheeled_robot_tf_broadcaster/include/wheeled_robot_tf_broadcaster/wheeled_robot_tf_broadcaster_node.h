#pragma once

#include <memory>
#include <string>

#include <rclcpp/rclcpp.hpp>
#include <gz/transport.hh>
#include <gz/msgs/pose_v.pb.h>
#include <tf2_ros/transform_broadcaster.h>

namespace wheeled_robot_tf_broadcaster {
class wheeled_robot_tf_broadcaster_node : public rclcpp::Node
{
  public:
    wheeled_robot_tf_broadcaster_node();

  private:
    void _on_poses_callback(const gz::msgs::Pose_V& msg);
    std::shared_ptr<gz::transport::Node> _gz_node;
    std::unique_ptr<tf2_ros::TransformBroadcaster> _tf_broadcaster;
    const std::string _gz_poses_topic_name = "/world/Moving_robot/dynamic_pose/info";
};

} //namespace wheeled_robot_tf_broadcaster